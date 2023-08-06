import logging
import os
import os.path
import posixpath
import shutil
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import yaml
from dvc_data.hashfile.db.local import LocalHashFileDB
from dvc_objects.fs.local import LocalFileSystem
from tqdm import tqdm

from dql.client import Client
from dql.data_storage import AbstractDataStorage
from dql.dataset import DatasetRecord
from dql.listing import Listing
from dql.node import NodeWithPath
from dql.storage import Status, Storage
from dql.utils import DQLDir, dql_paths_join

logger = logging.getLogger("dql")

DEFAULT_DATASET_DIR = "dataset"
DATASET_FILE_SUFFIX = ".dql"

TTL_INT = 4 * 60 * 60


class PendingIndexingError(Exception):
    pass


class DataSource:
    def __init__(self, listing, node):
        self.listing = listing
        self.node = node

    def get_full_path(self):
        return posixpath.join(self.listing.storage.uri, self.node.full_path)

    def get_node_full_path(self, node):
        return posixpath.join(self.listing.storage.uri, node.full_path)


@dataclass
class NodeGroup:
    """Class for a group of nodes from the same source"""

    listing: Listing
    nodes: List[NodeWithPath]

    # The source path within the bucket
    # (not including the bucket name or s3:// prefix)
    source_path: str = ""


def check_output_dataset_file(
    output: str,
    force: bool = False,
    dataset_filename: Optional[str] = None,
    skip_check_output: bool = False,
    skip_check_dql: bool = False,
) -> str:
    """
    Checks the output directory and dataset filename for existence or if they
    should be force-overwritten.
    """
    if not skip_check_output:
        if os.path.exists(output):
            if force:
                shutil.rmtree(output)
            else:
                raise RuntimeError(f"Output directory already exists: {output}")

    dataset_file = (
        dataset_filename if dataset_filename else output + DATASET_FILE_SUFFIX
    )
    if not skip_check_dql:
        if os.path.exists(dataset_file):
            if force:
                os.remove(dataset_file)
            else:
                raise RuntimeError(
                    f"Output dataset file already exists: {dataset_file}"
                )
    return dataset_file


def parse_dql_file(filename: str) -> List[Dict[str, Any]]:
    with open(filename, encoding="utf-8") as f:
        contents = yaml.safe_load(f)

    if not isinstance(contents, list):
        contents = [contents]

    for entry in contents:
        if not isinstance(entry, dict):
            raise ValueError(
                "Failed parsing DQL file, "
                "each data source entry must be a dictionary"
            )
        if "data-source" not in entry or "files" not in entry:
            raise ValueError(
                "Failed parsing DQL file, "
                "each data source entry must contain the "
                '"data-source" and "files" keys'
            )

    return contents


def prepare_output_for_cp(
    node_groups: List[NodeGroup],
    output: str,
    force: bool = False,
    dql_only: bool = False,
    no_dql_file: bool = False,
) -> Tuple[bool, Optional[str]]:
    total_node_count = 0
    for node_group in node_groups:
        if not node_group.nodes:
            raise FileNotFoundError(
                f"No such file or directory: {node_group.source_path}"
            )
        total_node_count += len(node_group.nodes)

    always_copy_dir_contents = False
    copy_to_filename = None

    if dql_only:
        return always_copy_dir_contents, copy_to_filename

    if not os.path.isdir(output):
        if total_node_count == 1:
            first_node: NodeWithPath = node_groups[0].nodes[0]
            if first_node.is_dir:
                if os.path.exists(output):
                    if force:
                        os.remove(output)
                    else:
                        raise FileExistsError(f"Path already exists: {output}")
                always_copy_dir_contents = True
                os.mkdir(output)
            else:  # Is a File
                if os.path.exists(output):
                    if force:
                        os.remove(output)
                    else:
                        raise FileExistsError(f"Path already exists: {output}")
                copy_to_filename = output
        else:
            raise FileNotFoundError(f"Is not a directory: {output}")

    if copy_to_filename and not no_dql_file:
        raise RuntimeError("File to file cp not supported with .dql files!")

    return always_copy_dir_contents, copy_to_filename


def collect_nodes_for_cp(
    node_groups: Iterable[NodeGroup],
    recursive: bool = False,
) -> Tuple[int, int]:
    total_size: int = 0
    total_files: int = 0

    # Collect all nodes to process
    for node_group in node_groups:
        listing: Listing = node_group.listing
        valid_nodes: List[NodeWithPath] = []
        for node in node_group.nodes:
            if node.is_dir:
                if not recursive:
                    print(f"{node.full_path} is a directory (not copied).")
                    continue
                add_size, add_files = listing.du(node)
                total_size += add_size
                total_files += add_files
                valid_nodes.append(node)
            else:
                # This node is a file
                total_size += node.size
                total_files += 1
                valid_nodes.append(node)

        node_group.nodes = valid_nodes

    return total_size, total_files


def download_node_groups(
    node_groups: Iterable[NodeGroup],
    cache: LocalHashFileDB,
    bar_format: str,
    total_size: int,
    recursive: bool = False,
):
    download_progress_bar = tqdm(
        desc="Downloading files: ",
        unit="B",
        bar_format=bar_format,
        unit_scale=True,
        unit_divisor=1000,
        total=total_size,
    )

    # Download these nodes
    for node_group in node_groups:
        if not node_group.nodes:
            continue
        listing: Listing = node_group.listing

        updated_nodes: List[NodeWithPath] = listing.download_nodes(
            node_group.nodes,
            cache,
            total_size,
            recursive=recursive,
            shared_progress_bar=download_progress_bar,
        )

        # This assert is hopefully not necessary, but is here mostly to
        # ensure this functionality stays consistent (and catch any bugs)
        assert len(node_group.nodes) == len(updated_nodes)

        node_group.nodes = updated_nodes

    download_progress_bar.close()


def instantiate_node_groups(
    node_groups: Iterable[NodeGroup],
    cache: LocalHashFileDB,
    output: str,
    bar_format: str,
    total_files: int,
    force: bool = False,
    recursive: bool = False,
    virtual_only: bool = False,
    always_copy_dir_contents: bool = False,
    copy_to_filename: Optional[str] = None,
) -> List[Dict[str, Any]]:
    instantiate_progress_bar = (
        None
        if virtual_only
        else tqdm(
            desc=f"Instantiating {output}: ",
            unit=" f",
            bar_format=bar_format,
            unit_scale=True,
            unit_divisor=1000,
            total=total_files,
        )
    )

    metafile_data = []

    # Instantiate these nodes
    for node_group in node_groups:
        if not node_group.nodes:
            continue
        listing: Listing = node_group.listing
        source_path: str = node_group.source_path
        metafile_group = {
            "data-source": listing.storage.to_dict(source_path),
            "files": [],
        }
        output_dir = output
        if copy_to_filename:
            output_dir = os.path.dirname(output)
            if not output_dir:
                output_dir = "."
            node_group.nodes = [
                node._replace(path=[], name=os.path.basename(output))  # type: ignore [call-arg] # noqa: E501
                for node in node_group.nodes
            ]
        instantiated_nodes = listing.instantiate_nodes(
            node_group.nodes,
            output_dir,
            cache,
            total_files,
            recursive=recursive,
            copy_dir_contents=always_copy_dir_contents or source_path.endswith("/"),
            force=force,
            virtual_only=virtual_only,
            relative_path=source_path,
            shared_progress_bar=instantiate_progress_bar,
        )

        for node in instantiated_nodes:
            if not node.is_dir:
                metafile_group["files"].append(node.get_metafile_data())
        if metafile_group["files"]:
            metafile_data.append(metafile_group)

    if instantiate_progress_bar:
        instantiate_progress_bar.close()

    return metafile_data


def trim_node_path(node: NodeWithPath) -> NodeWithPath:
    return node._replace(path=node.path[:-1])  # type: ignore[call-arg,attr-defined]


def find_column_to_str(node: NodeWithPath, src: DataSource, column: str) -> str:
    if column == "du":
        return str(src.listing.du(node)[0])
    if column == "name":
        return node.name or ""
    if column == "owner":
        return node.owner_name or ""
    if column == "path":
        return posixpath.join(src.get_full_path(), node.full_path)
    if column == "size":
        return str(node.size)
    if column == "type":
        return "d" if node.is_dir else "f"
    return ""


class Catalog:
    def __init__(
        self,
        data_storage: AbstractDataStorage,
        cache_dir=None,
        tmp_dir=None,
    ):
        dql_dir = DQLDir(cache=cache_dir, tmp=tmp_dir)
        self.data_storage = data_storage
        self.cache = LocalHashFileDB(
            LocalFileSystem(),
            dql_dir.cache,
            tmp_dir=dql_dir.tmp,
        )

    def enlist_source(
        self,
        source: str,
        ttl: int,
        force_update=False,
        skip_indexing=False,
        to_fetch=True,
        client_config=None,
    ) -> Tuple[Listing, str]:
        if force_update and skip_indexing:
            raise ValueError(
                "Both force_update and skip_indexing flags"
                " cannot be True at the same time"
            )

        client_config = client_config or {}
        client, path = Client.parse_url(source, **client_config)
        prefix = posixpath.dirname(path)
        source_data_storage = self.data_storage.clone(uri=client.uri)

        if skip_indexing:
            source_data_storage.create_storage_if_not_registered(client.uri)
            storage = source_data_storage.get_storage(client.uri)
            assert storage
            return (
                Listing(storage, source_data_storage, client),
                path,
            )

        (
            storage,
            need_index,
            in_progress,
            is_new,
        ) = source_data_storage.register_storage_for_indexing(
            client.uri, force_update, prefix
        )
        if in_progress:
            raise PendingIndexingError(f"Pending indexing operation: uri={storage.uri}")

        lst = Listing(storage, source_data_storage, client)

        if not need_index:
            logger.debug(  # type: ignore[unreachable]
                f"Using cached listing {storage.uri}."
                + f" Valid till: {storage.expires_to_local}"
            )
            # Listing has to have correct version of data storage
            # initialized with correct Storage
            return lst, path

        if to_fetch:
            try:
                source_data_storage.init_db(prefix, is_new)
                lst.fetch(prefix)
                source_data_storage.mark_storage_indexed(
                    storage.uri,
                    Status.PARTIAL if prefix else Status.COMPLETE,
                    ttl,
                    prefix=prefix,
                )
            except:  # noqa: E722,B001
                source_data_storage.mark_storage_indexed(
                    storage.uri, Status.FAILED, ttl, prefix=prefix
                )
                raise
            lst.storage = storage
        else:
            source_data_storage.init_db()
        return lst, path

    def enlist_sources(
        self,
        sources: List[str],
        ttl: int,
        update: bool,
        skip_indexing=False,
        client_config=None,
    ) -> List["DataSource"]:
        enlisted_sources = []
        for src in sources:  # Opt: parallel
            listing, file_path = self.enlist_source(
                src,
                ttl,
                update,
                skip_indexing=skip_indexing,
                client_config=client_config,
            )
            enlisted_sources.append((listing, file_path))

        dsrc_all = []
        for listing, file_path in enlisted_sources:
            nodes = listing.expand_path(file_path)
            for node in nodes:
                dsrc_all.append(DataSource(listing, node))

        return dsrc_all

    def enlist_sources_grouped(
        self,
        sources: List[str],
        ttl: int,
        update: bool,
        no_glob: bool = False,
        client_config=None,
    ) -> List[NodeGroup]:
        enlisted_sources: List[Tuple[bool, Any]] = []
        for src in sources:  # Opt: parallel
            if src.endswith(DATASET_FILE_SUFFIX) and os.path.isfile(src):
                # TODO: Also allow using DQL files from cloud locations?
                dql_data = parse_dql_file(src)
                indexed_sources = []
                for ds in dql_data:
                    listing, source_path = self.enlist_source(
                        ds["data-source"]["uri"],
                        ttl,
                        update,
                        client_config=client_config,
                    )
                    paths = dql_paths_join(
                        source_path, (f["name"] for f in ds["files"])
                    )
                    indexed_sources.append((listing, source_path, paths))
                enlisted_sources.append((True, indexed_sources))
            else:
                listing, source_path = self.enlist_source(
                    src, ttl, update, client_config=client_config
                )
                enlisted_sources.append((False, (listing, source_path)))

        node_groups = []
        nodes: List[NodeWithPath] = []
        for is_dql, payload in enlisted_sources:  # Opt: parallel
            if is_dql:
                for listing, source_path, paths in payload:
                    nodes = [trim_node_path(listing.resolve_path(p)) for p in paths]
                    node_groups.append(NodeGroup(listing, nodes, source_path))
            else:
                listing, source_path = payload
                if no_glob:
                    nodes = [trim_node_path(listing.resolve_path(source_path))]
                else:
                    nodes = listing.expand_path(source_path)
                    if len(nodes) == 1 and not nodes[0].is_dir:
                        nodes = [trim_node_path(nodes[0])]

                node_groups.append(NodeGroup(listing, nodes, source_path))

        return node_groups

    def upsert_shadow_dataset(
        self,
        name: str,
        sources: List[str],
        client_config=None,
        recursive=False,
    ) -> None:
        """
        Creates shadow dataset in DB if it doesn't exist and updates it with
        entries from sources.
        Example of sources:
            s3://bucket_name/dir1/dir2/*
            s3://bucket_name/*
            s3://bucket_name/image_*
        """
        client_config = client_config or {}
        self.data_storage.create_shadow_dataset(name)
        for source in sources:
            client, path = Client.parse_url(source, **client_config)
            self.data_storage.insert_into_shadow_dataset(
                name, client.uri, path, recursive=recursive
            )

    def register(
        self,
        dataset_name: str,
        new_dataset_name: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ):
        dataset = self.data_storage.get_dataset(dataset_name)
        if not dataset:
            raise RuntimeError(f"Dataset with name: {dataset_name} doesn't exist")

        if not dataset.shadow:
            raise RuntimeError(f"Dataset is already registered: {dataset_name}")

        update_data = {
            "version": version or "1",
            "shadow": False,
            "description": description,
            "labels": labels,
        }

        if new_dataset_name:
            update_data["name"] = new_dataset_name

        self.data_storage.update_dataset(dataset_name, **update_data)

    def ls_datasets(self, shadow_only=None) -> Iterable[DatasetRecord]:
        yield from self.data_storage.get_datasets(shadow_only=shadow_only)

    def remove_dataset(self, name: str):
        self.data_storage.remove_dataset(name)

    def edit_dataset(
        self,
        name: str,
        new_name: Optional[str] = None,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ):
        update_data = {}
        if new_name:
            update_data["name"] = new_name
        if description:
            update_data["description"] = description
        if labels:
            update_data["labels"] = labels  # type: ignore[assignment]

        self.data_storage.update_dataset(name, **update_data)

    def ls(
        self,
        sources: List[str],
        ttl=TTL_INT,
        update=False,
        skip_indexing=False,
        *,
        client_config=None,
    ) -> Iterator[Tuple[DataSource, Iterator[NodeWithPath]]]:
        data_sources = self.enlist_sources(
            sources,
            ttl,
            update,
            skip_indexing=skip_indexing,
            client_config=client_config,
        )

        for source in data_sources:
            yield source, iter(source.listing.ls_path(source.node))

    def ls_storages(self) -> Iterator[Storage]:
        yield from self.data_storage.get_storage_all()

    def get(
        self,
        source,
        output,
        force=False,
        update=False,
        ttl=TTL_INT,
        *,
        client_config=None,
    ) -> None:
        listing, file_path = self.enlist_source(
            source, ttl, update, client_config=client_config
        )

        if not output:
            if file_path:
                output = os.path.basename(file_path.rstrip("/"))
            else:
                output = listing.storage.name

        dataset_file = check_output_dataset_file(output, force)

        node = listing.resolve_path(file_path)
        total_size, total_files = listing.du(node)
        listing.download_subtree(node, self.cache, total_size)
        listing.instantiate_subtree(node, output, self.cache, total_files)
        listing.metafile_for_subtree(file_path, node, dataset_file)

    def cp(
        self,
        sources: List[str],
        output: str,
        force: bool = False,
        update: bool = False,
        recursive: bool = False,
        dql_file: Optional[str] = None,
        dql_only: bool = False,
        no_glob: bool = False,
        no_dql_file: bool = False,
        create_dataset: bool = False,
        ttl: int = TTL_INT,
        *,
        client_config=None,
    ) -> List[Dict[str, Any]]:
        node_groups = self.enlist_sources_grouped(
            sources,
            ttl,
            update,
            no_glob,
            client_config=client_config,
        )

        always_copy_dir_contents, copy_to_filename = prepare_output_for_cp(
            node_groups, output, force, dql_only, no_dql_file
        )

        dataset_file = check_output_dataset_file(
            output, force, dql_file, True, no_dql_file
        )

        total_size, total_files = collect_nodes_for_cp(node_groups, recursive)

        if total_files == 0:
            # Nothing selected to cp
            return []

        desc_max_len = max(len(output) + 16, 19)
        bar_format = (
            "{desc:<"
            f"{desc_max_len}"
            "}{percentage:3.0f}%|{bar}| {n_fmt:>5}/{total_fmt:<5} "
            "[{elapsed}<{remaining}, {rate_fmt:>8}]"
        )

        if not dql_only:
            download_node_groups(
                node_groups, self.cache, bar_format, total_size, recursive
            )

        metafile_data = instantiate_node_groups(
            node_groups,
            self.cache,
            output,
            bar_format,
            total_files,
            force,
            recursive,
            dql_only,
            always_copy_dir_contents,
            copy_to_filename,
        )

        if create_dataset:
            self.upsert_shadow_dataset(
                output, sources, client_config, recursive=recursive
            )

        if not metafile_data or no_dql_file:
            # Don't write the metafile if nothing was copied (or skipped)
            return metafile_data

        print(f"Creating '{dataset_file}'")
        with open(dataset_file, "w", encoding="utf-8") as fd:
            yaml.dump(metafile_data, fd, sort_keys=False)

        return metafile_data

    def du(
        self,
        sources,
        depth=0,
        ttl=TTL_INT,
        update=False,
        *,
        client_config=None,
    ) -> Iterable[Tuple[str, float]]:
        sources = self.enlist_sources(
            sources,
            ttl,
            update,
            client_config=client_config,
        )

        def du_dirs(src, node, subdepth):
            if subdepth > 0:
                subdirs = src.listing.data_storage.get_nodes_by_parent_id(
                    node.id, type="dir"
                )
                for sd in subdirs:
                    yield from du_dirs(src, sd, subdepth - 1)
            yield (src.get_node_full_path(node), src.listing.du(node)[0])

        for src in sources:
            yield from du_dirs(src, src.node, depth)

    def find(
        self,
        sources,
        ttl=TTL_INT,
        update=False,
        names=None,
        inames=None,
        paths=None,
        ipaths=None,
        size=None,
        typ=None,
        jmespath=None,
        columns=None,
        *,
        client_config=None,
    ) -> Iterable[str]:
        sources = self.enlist_sources(
            sources,
            ttl,
            update,
            client_config=client_config,
        )
        if not columns:
            columns = ["path"]
        for src in sources:
            nodes = src.listing.find(
                src.node, names, inames, paths, ipaths, size, typ, jmespath
            )
            for node in nodes:
                yield "\t".join(
                    [find_column_to_str(node, src, column) for column in columns]
                )

    def index(
        self, sources, ttl=TTL_INT, update=False, *, client_config=None
    ) -> List["DataSource"]:
        root_sources = [
            src for src in sources if Client.get_implementation(src).is_root_url(src)
        ]
        non_root_sources = [
            src
            for src in sources
            if not Client.get_implementation(src).is_root_url(src)
        ]

        client_config = client_config or {}

        # for root sources (e.g s3://) we are just getting all buckets and
        # saving them as storages, without further indexing in each bucket
        for source in root_sources:
            for bucket in Client.get_implementation(source).ls_buckets(**client_config):
                client, _ = Client.parse_url(bucket.uri)
                print(f"Registering storage {client.uri}")
                self.data_storage.create_storage_if_not_registered(client.uri)

        return self.enlist_sources(
            non_root_sources,
            ttl,
            update,
            client_config=client_config,
        )
