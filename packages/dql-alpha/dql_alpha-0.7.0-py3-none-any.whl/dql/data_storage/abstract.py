import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)

from dql.node import AnyNode, Node, NodeWithPath
from dql.storage import Storage

if TYPE_CHECKING:
    from dql.dataset import DatasetRecord

DB_FILE_NAME = "db"


logger = logging.getLogger("dql")


class AbstractDataStorage(ABC):
    @abstractmethod
    def clone(self, uri: Optional[str]) -> "AbstractDataStorage":
        """Clones DataStorage implementation for some Storage input"""

    @abstractmethod
    def init_db(self, prefix: str = "", is_new: bool = True):
        """Initializes database tables for data storage"""

    @abstractmethod
    def create_shadow_dataset(self, name: str) -> None:
        """Creates shadow database table if doesn't exist"""

    @abstractmethod
    def insert_into_shadow_dataset(
        self, name: str, uri: str, path: str, recursive: bool = False
    ) -> None:
        """Inserts data to shadow dataset based on bucket uri and glob path"""

    @abstractmethod
    def update_dataset(self, dataset_name: str, **kwargs) -> None:
        """Updates dataset fields"""

    @abstractmethod
    def get_dataset(self, name: str) -> Optional["DatasetRecord"]:
        """Finds dataset by name"""

    @abstractmethod
    def remove_dataset(self, name: str) -> None:
        """Removes dataset by name and it's corresponding entries"""

    @abstractmethod
    async def insert_entry(self, entry: Dict[str, Any]) -> int:
        """
        Inserts file or directory node into the database
        and returns the id of the newly added node
        """

    @abstractmethod
    async def insert_entries(self, entries: List[Dict[str, Any]]) -> None:
        """Inserts file or directory nodes into the database"""

    @abstractmethod
    async def insert_root(self) -> int:
        """
        Inserts root directory and returns the id of the newly added root
        """

    @abstractmethod
    def get_nodes_by_parent_id(
        self,
        parent_id: int,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterable[Node]:
        """Gets nodes from database by parent_id, with optional filtering"""

    @abstractmethod
    def create_storage_if_not_registered(self, uri: str) -> None:
        """
        Saves new storage if it doesn't exist in database
        """

    @abstractmethod
    def register_storage_for_indexing(
        self,
        uri: str,
        force_update: bool,
        prefix: str = "",
    ) -> Tuple[Storage, bool, bool, bool]:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        It returns:
            - storage, prepared for indexing
            - boolean saying if indexing is needed
            - boolean saying if indexing is currently pending (running)
            - boolean saying if this storage is newly created
        """

    @abstractmethod
    def mark_storage_indexed(
        self,
        uri: str,
        status: int,
        ttl: int,
        end_time: Optional[datetime] = None,
        prefix: str = "",
    ) -> None:
        """
        Marks storage as indexed.
        This method should be called when index operation is finished
        """

    @abstractmethod
    def get_storage_all(self) -> Iterator[Storage]:
        pass

    @abstractmethod
    def get_storage(self, uri: str) -> Optional[Storage]:
        """
        Gets storage representation from database.
        E.g if s3 is used as storage this would be s3 bucket data
        """

    @abstractmethod
    def size(self, node: Node) -> Tuple[int, int]:
        """
        Calculates size of some node (and subtree below node).
        Returns size in bytes as int and total files as int
        """

    @abstractmethod
    def get_node_by_path(self, path: str) -> NodeWithPath:
        """Gets node that correspond to some path"""

    @abstractmethod
    def expand_path(self, path: str) -> List[NodeWithPath]:
        """Simulates Unix-like shell expansion"""

    @abstractmethod
    def walk_subtree(
        self,
        node: AnyNode,
        sort: Union[List[str], str, None] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterable[NodeWithPath]:
        """
        Returns all directory and file nodes that are "below" some node.
        Nodes can be sorted or filtered as well.
        """

    @abstractmethod
    def get_latest_files_by_parent_node(self, parent_node: Node) -> Iterable[Node]:
        """
        Gets latest-version file nodes from the provided parent node
        """

    @abstractmethod
    def find(self, node: AnyNode, jmespath="", **conds) -> Iterable[NodeWithPath]:
        """
        Tries to find nodes that match certain criteria like name or jmespath,
        only looks for latest nodes under the passed node.
        """

    @abstractmethod
    def update_annotation(self, node: Node, annotation_content: str) -> None:
        """Updates annotation of a specific node in database"""

    @abstractmethod
    def update_checksum(self, node: Node, checksum: str) -> None:
        """Updates checksum of specific node in database"""

    @abstractmethod
    def get_datasets(
        self, shadow_only: Optional[bool] = None
    ) -> Iterator["DatasetRecord"]:
        """Get dataset records"""
