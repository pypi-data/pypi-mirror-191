import hashlib
import json
import logging
import posixpath
import sqlite3
from datetime import datetime, timezone
from functools import partial, wraps
from time import sleep
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from dql.data_storage.abstract import AbstractDataStorage
from dql.dataset import DatasetRecord
from dql.error import DQLError
from dql.node import AnyNode, DirType, Node, NodeWithPath
from dql.storage import Status as StorageStatus
from dql.storage import Storage
from dql.utils import GLOB_CHARS, DQLDir, is_expired

from .query import Query, Schema

logger = logging.getLogger("dql")

RETRY_START_SEC = 0.01
RETRY_MAX_TIMES = 10
RETRY_FACTOR = 2


class NodeSchema(Schema):
    fields = [
        "id",
        "dir_type",
        "parent_id",
        "name",
        "checksum",
        "etag",
        "version",
        "is_latest",
        "last_modified",
        "size",
        "owner_name",
        "owner_id",
        "path_str",
        "anno",
    ]

    def lookup_type(self, query, _, value):
        if value in {"f", "file", "files"}:
            return query.compile_op("dir_type", "eq", DirType.FILE)
        elif value in {"d", "dir", "directory", "directories"}:
            return query.compile_op("dir_type", "ne", DirType.FILE)
        else:
            return None


DATASET_FIELDS = [
    "name",
    "shadow",
    "description",
    "version",
    "labels",
]
PATH_STR_INDEX = NodeSchema.fields.index("path_str")


class StorageSchema(Schema):
    table = "buckets"
    fields = ["uri", "timestamp", "expires", "status"]


class PartialSchema(Schema):
    fields = ["path_str", "timestamp", "expires"]


def get_retry_sleep_sec(retry_count: int) -> int:
    return RETRY_START_SEC * (RETRY_FACTOR**retry_count)


def retry_sqlite_locks(func):
    # This retries the database modification in case of concurrent access
    @wraps(func)
    def wrapper(*args, **kwargs):
        exc = None
        for retry_count in range(RETRY_MAX_TIMES):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as operror:
                exc = operror
                sleep(get_retry_sleep_sec(retry_count))
        raise exc

    return wrapper


def retry_sqlite_locks_async(func):
    # This retries the database modification in case of concurrent access
    # (For async code)
    @wraps(func)
    async def wrapper(*args, **kwargs):
        exc = None
        for retry_count in range(RETRY_MAX_TIMES):
            try:
                return await func(*args, **kwargs)
            except sqlite3.OperationalError as operror:
                exc = operror
                sleep(get_retry_sleep_sec(retry_count))
        raise exc

    return wrapper


class SQLiteDataStorage(AbstractDataStorage):
    """
    SQLite data storage uses SQLite3 for storing indexed data locally.
    This is currently used for the cli although could potentially support or
    be expanded for cloud storage as well.
    """

    LISTING_TABLE_NAME_PREFIX = "dsrc_"
    DATASET_TABLE_PREFIX = "ds_"
    TABLE_NAME_SHA_LIMIT = 12

    def __init__(self, db_file: Optional[str] = None, table_name: str = ""):
        self.table_name = table_name
        self.db_file = db_file if db_file else DQLDir.find().db

        try:
            if self.db_file == ":memory:":
                # Enable multithreaded usage of the same in-memory db
                self.db = sqlite3.connect("file::memory:?cache=shared", uri=True)
            else:
                self.db = sqlite3.connect(self.db_file)
            self.db.isolation_level = None  # Use autocommit mode
            self.db.execute("PRAGMA foreign_keys = ON")
            self.db.execute("PRAGMA cache_size = -102400")  # 100 MiB
            # Enable Write-Ahead Log Journaling
            self.db.execute("PRAGMA journal_mode = WAL")
            self.db.execute("PRAGMA synchronous = NORMAL")
            self.db.execute("PRAGMA case_sensitive_like = ON")

            self._init_storage_table()
            self._init_datasets_table()
        except RuntimeError:
            raise DQLError("Can't connect to SQLite DB")

    def _init_storage_table(self):
        """Initialize only tables related to storage, e.g s3"""
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS buckets
            (
                uri         TEXT PRIMARY KEY NOT NULL,
                timestamp   DATETIME,
                expires     DATETIME,
                status      INTEGER NOT NULL
            )
        """
        )

    def _init_datasets_table(self) -> None:
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets
            (
                id              INTEGER PRIMARY KEY,
                name            TEXT NOT NULL UNIQUE,
                description     TEXT,
                version         TEXT,
                labels          JSON DEFAULT('[]'),
                shadow          BOOL NOT NULL
            );
            """
        )

    def init_db(self, prefix: str = "", is_new: bool = True):
        # Note that an index on the primary key (id) is automatically created
        if not prefix or is_new:
            self.db.executescript(
                f"""
                DROP TABLE IF EXISTS {self.table_name};
                DROP TABLE IF EXISTS {self.table_name}_indexed;
                """
            )
        self.db.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}
            (
                id              INTEGER PRIMARY KEY,
                dir_type        INTEGER,
                parent_id       INTEGER,
                name            TEXT NOT NULL,
                checksum        TEXT,
                etag            TEXT,
                version         TEXT,
                is_latest       BOOL,
                last_modified   DATETIME,
                size            BIGINT NOT NULL,
                owner_name      TEXT,
                owner_id        TEXT,
                path_str        TEXT,
                anno            JSON
            );

            CREATE INDEX IF NOT EXISTS idx_dir_type_{self.table_name}
            ON {self.table_name} (dir_type);
            CREATE INDEX IF NOT EXISTS idx_parent_id_{self.table_name}
            ON {self.table_name} (parent_id);
            CREATE INDEX IF NOT EXISTS idx_name_{self.table_name}
            ON {self.table_name} (name);
            CREATE INDEX IF NOT EXISTS idx_path_str_{self.table_name}
            ON {self.table_name} (path_str);

            CREATE TABLE IF NOT EXISTS {self.table_name}_indexed
            (
                path_str    TEXT PRIMARY KEY NOT NULL,
                timestamp   DATETIME,
                expires     DATETIME
            );

            CREATE INDEX IF NOT EXISTS idx_path_str_{self.table_name}_indexed
            ON {self.table_name}_indexed (path_str);
        """
        )

    @classmethod
    def _table_name(cls, name, prefix) -> str:
        sha = hashlib.sha256(name.encode("utf-8")).hexdigest()
        return prefix + sha[: cls.TABLE_NAME_SHA_LIMIT]

    @classmethod
    def _listing_table_name(cls, uri) -> str:
        return cls._table_name(uri, cls.LISTING_TABLE_NAME_PREFIX)

    @classmethod
    def _dataset_table_name(cls, dataset_id: int) -> str:
        return cls.DATASET_TABLE_PREFIX + str(dataset_id)

    def clone(self, uri: Optional[str] = None) -> "SQLiteDataStorage":
        table_name = self._listing_table_name(uri) if uri else self.table_name
        return SQLiteDataStorage(db_file=self.db_file, table_name=table_name)

    # Query starters
    @property
    def nodes(self):
        def with_path(row, cut):
            path_str = row[PATH_STR_INDEX]
            assert path_str.startswith(cut)
            cut_path = path_str[len(cut) :].lstrip("/") if cut else path_str
            return NodeWithPath(*row, cut_path.split("/"))  # type: ignore [call-arg]

        q = Query(self.db, NodeSchema(), self.table_name, wrap=Node._make)
        q.with_path = lambda cut="": q.wrap(partial(with_path, cut=cut))
        return q

    @property
    def storages(self):
        return Query(self.db, StorageSchema(), wrap=Storage._make)

    @property
    def partials(self):
        return Query(self.db, PartialSchema(), f"{self.table_name}_indexed")

    def _get_nodes_by_glob_path_pattern(
        self, path_list: List[str], glob_name: str
    ) -> Iterable[NodeWithPath]:
        """Finds all Nodes that correspond to GLOB like path pattern."""
        node = self._get_node_by_path_list(path_list)
        if not node.is_dir:
            raise RuntimeError(f"Can't resolve name {'/'.join(path_list)}")

        def _with_path(row):
            return NodeWithPath(*row, path_list)  # type: ignore [call-arg]

        q = self.nodes.where(parent_id=node.id, is_latest=True, name__glob=glob_name)
        return q.wrap(_with_path).all()

    def _get_node_by_path_list(self, path_list: List[str]) -> NodeWithPath:
        """
        Gets node that correspond some path list, e.g ["data-lakes", "dogs-and-cats"]
        """
        path_str = "/".join(path_list)
        node = self.nodes.with_path().where(path_str=path_str, is_latest=True).get()
        if not node:
            raise FileNotFoundError(f"Unable to resolve path {path_str}")
        return node

    def _populate_nodes_by_path(
        self, path_list: List[str], num: int, res: List[NodeWithPath]
    ) -> None:
        """
        Puts all nodes found by path_list into the res input variable.
        Note that path can have GLOB like pattern matching which means that
        res can have multiple nodes as result.
        If there is no GLOB pattern, res should have one node as result that
        match exact path by path_list
        """
        if num >= len(path_list):
            res.append(self._get_node_by_path_list(path_list))
            return

        curr_name = path_list[num]
        if set(curr_name).intersection(GLOB_CHARS):
            nodes = self._get_nodes_by_glob_path_pattern(path_list[:num], curr_name)
            for node in nodes:
                if not node.is_dir:
                    res.append(node)
                else:
                    path = (
                        path_list[:num]
                        + [node.name or ""]
                        + path_list[num + 1 :]  # type: ignore [attr-defined]
                    )
                    self._populate_nodes_by_path(path, num + 1, res)
        else:
            self._populate_nodes_by_path(path_list, num + 1, res)
            return
        return

    @staticmethod
    def _prepare_node(d: Dict[str, Any]) -> Dict[str, Any]:
        if d.get("dir_type") is None:
            if d.get("is_root"):
                dir_type = DirType.ROOT
            elif d.get("is_dir"):
                dir_type = DirType.DIR
            else:
                dir_type = DirType.FILE
            d["dir_type"] = dir_type

        if not d.get("path_str"):
            if d.get("path"):
                path = d["path"]
                if isinstance(path, list):
                    d["path_str"] = "/".join(path)
                else:
                    d["path_str"] = path
            elif d.get("dir_type") == DirType.ROOT:
                d["path_str"] = ""
            else:
                raise RuntimeError(f"No Path for node data: {d}")

        d = {"name": "", "is_latest": True, "size": 0, **d}
        return {f: d.get(f) for f in NodeSchema.fields[1:]}

    def get_datasets(
        self, shadow_only: Optional[bool] = None
    ) -> Iterator["DatasetRecord"]:
        if shadow_only is None:
            cond = ""
        elif shadow_only:
            cond = "WHERE shadow"
        else:
            cond = "WHERE NOT shadow"
        for row in self.db.execute(
            f"""
            SELECT
                id,
                name,
                description,
                version,
                labels,
                shadow
            FROM datasets
            {cond}
            """,
        ).fetchall():
            yield DatasetRecord.parse(*row)

    def create_shadow_dataset(self, name: str) -> None:
        """Creates new shadow dataset if it doesn't exist yet"""
        with self.db:
            self.db.execute("begin")

            # adds entry into datasets table
            self.db.execute(
                """INSERT INTO datasets(name, shadow) VALUES (?, ?)
                ON CONFLICT(name) DO NOTHING
                """,
                [name, True],
            )
            dataset = self.get_dataset(name)
            assert dataset
            table_name = self._dataset_table_name(dataset.id)

            # creates special shadow dataset table to store entries
            self.db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name}
                (
                    id              INTEGER PRIMARY KEY,
                    source          TEXT NOT NULL,
                    path_str        TEXT,
                    dir_type        INTEGER,
                    parent_id       INTEGER,
                    name            TEXT NOT NULL,
                    checksum        TEXT,
                    etag            TEXT,
                    version         TEXT,
                    is_latest       BOOL,
                    last_modified   DATETIME,
                    size            BIGINT NOT NULL,
                    owner_name      TEXT,
                    owner_id        TEXT,
                    anno            JSON
                );
                """
            )

    def insert_into_shadow_dataset(
        self, name: str, uri: str, path: str, recursive=False
    ) -> None:
        dataset = self.get_dataset(name)
        assert dataset

        source_table_name = self._listing_table_name(uri)
        dataset_table_name = self._dataset_table_name(dataset.id)

        if recursive:
            if not path.endswith("*"):
                path = path.rstrip("/") + "/*"  # glob filter must end with /*
            nodes = self.nodes.where(path_str__glob=path, type="file")
        else:
            self.table_name = source_table_name  # needed for parent node
            parent = self.get_node_by_path(path.lstrip("/").rstrip("/*"))
            nodes = self.nodes.where(parent_id=parent.id, type="file")

        (
            where_sql,
            where_params,
        ) = nodes._compile_where()  # pylint: disable=protected-access
        insert_q = f"""
            INSERT into {dataset_table_name}
            (
                path_str,
                dir_type,
                parent_id,
                name,
                checksum,
                etag,
                version,
                is_latest,
                last_modified,
                size,
                owner_name,
                owner_id,
                anno,
                source
            )
            SELECT
                path_str,
                dir_type,
                parent_id,
                name,
                checksum,
                etag,
                version,
                is_latest,
                last_modified,
                size,
                owner_name,
                owner_id,
                anno,
                ? AS source
            FROM {source_table_name}
            {where_sql}
            """
        self.db.execute(
            insert_q,
            [uri] + where_params,
        )
        self.db.commit()

    def update_dataset(self, dataset_name: str, **kwargs) -> None:
        args = []
        fields = []
        for field, value in kwargs.items():
            if field in DATASET_FIELDS:
                fields.append(field)
                if field == "labels":
                    args.append(json.dumps(value))
                else:
                    args.append(value)

        if not fields:
            # Nothing to update
            return

        args.append(dataset_name)  # for WHERE part

        set_query = "SET " + ", ".join(f"{field} = ?" for field in fields)
        self.db.execute(f"UPDATE datasets {set_query} WHERE name = ?", args)

    def get_dataset(self, name: str) -> Optional[DatasetRecord]:
        res = self.db.execute(
            "SELECT * from datasets WHERE name = ?", [name]
        ).fetchall()
        if not res:
            return None

        assert len(res) == 1, f"Dataset duplication: {name}"
        return DatasetRecord.parse(*res[0])

    def remove_dataset(self, name: str) -> None:
        with self.db:
            self.db.execute("begin")
            dataset = self.get_dataset(name)
            assert dataset
            dataset_table_name = self._dataset_table_name(dataset.id)

            self.db.execute("DELETE FROM datasets WHERE id = ?", [dataset.id])
            self.db.execute(f"DROP TABLE {dataset_table_name}")

    @retry_sqlite_locks_async
    async def insert_entry(self, entry: Dict[str, Any]) -> int:
        return self.nodes.insert(self._prepare_node(entry))

    @retry_sqlite_locks_async
    async def insert_entries(self, entries: List[Dict[str, Any]]) -> None:
        self.nodes.insertmany(map(self._prepare_node, entries))

    async def insert_root(self) -> int:
        return await self.insert_entry({"dir_type": DirType.ROOT})

    def get_nodes_by_parent_id(
        self,
        parent_id: int,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterable[Node]:
        """Gets nodes from database by parent_id, with optional filtering"""
        return self.nodes.where(parent_id=parent_id, type=type).all()

    def get_storage_all(self) -> Iterator[Storage]:
        return self.storages.all()

    def get_storage(self, uri: str) -> Optional[Storage]:
        return self.storages.where(uri=uri).get()

    @retry_sqlite_locks
    def create_storage_if_not_registered(self, uri: str) -> None:
        self.storages.insert({"uri": uri, "status": StorageStatus.CREATED}, upsert=True)

    def register_storage_for_indexing(
        self,
        uri: str,
        force_update: bool = True,
        prefix: str = "",
    ) -> Tuple[Storage, bool, bool, bool]:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        It returns:
            - storage, prepared for indexing
            - boolean saying if indexing is needed
            - boolean saying if indexing is currently pending (running)
        """
        # This ensures that all calls to the DB are in a single transaction
        # and commit is automatically called once this function returns
        with self.db:
            self.db.execute("begin")

            # Create storage if it doesn't exist
            self.create_storage_if_not_registered(uri)
            saved_storage = self.get_storage(uri)

            assert (
                saved_storage is not None
            ), f"Unexpected error, storage for {uri} doesn't exist"
            storage: Storage = saved_storage

            if storage.status == StorageStatus.PENDING:
                return storage, False, True, False

            elif storage.is_expired:
                storage = self.mark_storage_pending(storage)
                return storage, True, False, False

            elif storage.status == StorageStatus.COMPLETE and not force_update:
                return storage, False, False, False

            elif (
                storage.status == StorageStatus.PARTIAL and prefix and not force_update
            ):
                if self.check_partial_index_valid(prefix):
                    return storage, False, False, False
                self.delete_partial_index(prefix)
                return storage, True, False, False

            else:
                is_new = storage.status == StorageStatus.CREATED
                storage = self.mark_storage_pending(storage)
                return storage, True, False, is_new

    def delete_partial_index(self, prefix: str):
        """
        Deletes the provided and any subdir indexed prefixes and nodes
        """
        dir_prefix = posixpath.join(prefix, "")
        self.partials.where(path_str__startswith=dir_prefix).delete()
        self.nodes.where(path_str__startswith=prefix).delete()

    def check_partial_index_valid(self, prefix: str):
        # This SQL statement finds all matching path_str entries that are
        # prefixes of the provided prefix, matching this or parent directories
        # that are indexed.
        dir_prefix = posixpath.join(prefix, "")
        expire_values = self.partials.where(path_str__startof=dir_prefix).col("expires")
        return not all(is_expired(expires) for expires in expire_values)

    @retry_sqlite_locks
    def mark_storage_pending(self, storage: Storage) -> Storage:
        # Update status to pending and dates
        updates = {"status": StorageStatus.PENDING, "timestamp": None, "expires": None}
        storage = storage._replace(**updates)  # type: ignore [arg-type]
        self.storages.where(uri=storage.uri).update(**updates)
        return storage

    @retry_sqlite_locks
    def mark_storage_indexed(
        self,
        uri: str,
        status: int,
        ttl: int,
        end_time: Optional[datetime] = None,
        prefix: str = "",
    ) -> None:
        if end_time is None:
            end_time = datetime.now(timezone.utc)
        expires = Storage.get_expiration_time(end_time, ttl)

        with self.db:
            self.db.execute("BEGIN")

            self.storages.where(uri=uri).update(
                timestamp=end_time,
                expires=expires,
                status=status,
            )

            if status in {StorageStatus.COMPLETE, StorageStatus.FAILED}:
                # Delete remaining partial index paths
                self.partials.delete()
            elif status == StorageStatus.PARTIAL:
                if not prefix:
                    raise RuntimeError("Partial indexing requires a prefix!")

                dirprefix = posixpath.join(prefix, "")
                row = {"path_str": dirprefix, "timestamp": end_time, "expires": expires}
                self.partials.insert(row)

    def get_node_by_path(self, path: str) -> NodeWithPath:
        conds: Dict[str, Any] = {"path_str": path.strip("/")}
        if path.endswith("/"):
            conds["dir_type__ne"] = DirType.FILE
        node = self.nodes.with_path().where(**conds).get()
        if not node:
            raise FileNotFoundError(f"Unable to resolve path {path}")
        return node

    def expand_path(self, path: str) -> List[NodeWithPath]:
        """Simulates Unix-like shell expansion"""
        clean_path = path.strip("/")
        path_list = clean_path.split("/") if clean_path != "" else []

        res: List[NodeWithPath] = []
        self._populate_nodes_by_path(path_list, 0, res)
        return res

    def get_latest_files_by_parent_node(self, parent_node: Node) -> Iterable[Node]:
        if not parent_node.is_dir:
            return [parent_node]

        return self.nodes.where(parent_id=parent_node.id, is_latest=True).all()

    def size(self, node: Node) -> Tuple[int, int]:
        if not node.is_dir:
            # Return node size if this is not a directory
            return node.size, 1

        sub_glob = posixpath.join(node.path_str, "*")
        size, count = self.nodes.where(path_str__glob=sub_glob, is_latest=True).get(
            "SUM(size)", "SUM(dir_type = 0)"
        )
        return size or 0, count or 0

    def walk_subtree(
        self,
        node: AnyNode,
        sort: Union[List[str], str, None] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        _conds: Dict[str, Any] = None,
    ) -> Iterable[NodeWithPath]:
        conds = _conds.copy() if _conds else {}

        if node.path_str:
            sub_glob = posixpath.join(node.path_str, "*")
            conds.setdefault("path_str__glob", []).append(sub_glob)

        conds = dict(
            conds,
            dir_type__ne=DirType.ROOT,
            is_latest=True,
        )
        if type is not None:
            conds["type"] = type

        q = self.nodes.with_path(cut=node.path_str).where(**conds)
        if sort:
            q = q.order_by(sort)
        results = q.all()

        if not results:
            raise FileNotFoundError(f"Unable to resolve path {node.path_str}")
        return results

    def find(self, node: AnyNode, jmespath="", **conds) -> Iterable[NodeWithPath]:
        if jmespath:
            raise NotImplementedError("jmespath queries not supported!")
        try:
            return self.walk_subtree(node, _conds=conds)
        except FileNotFoundError:
            return []

    @retry_sqlite_locks
    def update_annotation(self, node: Node, annotation_content: str) -> None:
        # TODO: This will likely need to be updated for annotation support
        img_exts = ["jpg", "jpeg", "png"]
        names = [node.name_no_ext + "." + ext for ext in img_exts]

        res = self.nodes.where(
            parent_id=node.parent_id, type="file", is_latest=True, name__ieq=names
        )

        if res is None or len(res) == 0:
            msg = f"no image file was found for annotation {node.name}"
            logger.warning(msg)
        elif res[0][0] > 1:
            msg = (
                f"multiple image files were updated for a single "
                f"annotation {node.name}"
            )
            logger.warning(msg)

    @retry_sqlite_locks
    def update_checksum(self, node: Node, checksum: str) -> None:
        self.nodes.where(id=node.id).update(checksum=checksum)
