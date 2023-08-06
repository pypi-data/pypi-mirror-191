import json
from dataclasses import dataclass
from typing import List, Optional, Sequence, Type, TypeVar

T = TypeVar("T", bound="DatasetRecord")


@dataclass
class DatasetRecord:
    id: int
    name: str
    description: Optional[str]
    version: Optional[str]
    labels: Sequence[str]
    shadow: bool

    @classmethod
    def parse(
        cls: Type[T],
        id: int,  # pylint: disable=redefined-builtin
        name: str,
        description: Optional[str],
        version: Optional[str],
        labels: str,
        shadow: int,
    ) -> T:
        labels_lst: List[str] = json.loads(labels)
        return cls(id, name, description, version, labels_lst, bool(shadow))
