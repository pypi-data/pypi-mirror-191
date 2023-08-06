"""File-info module."""
import dataclasses
import typing as t


@dataclasses.dataclass(frozen=True)
class FileInfo:
    """FileInfo dataclass yielded from storage.ls() calls.

    Path is unique and relative to the storage prefix. Slots minimize memory
    usage to allow storing large number of FileInfo instances at once.
    """

    __slots__ = ("path", "size", "hash", "created", "modified")

    path: str
    size: int
    hash: t.Optional[str]
    created: t.Optional[t.Union[int, float]]
    modified: t.Optional[t.Union[int, float]]

    def asdict(self) -> dict:  # pragma: no cover
        """Return as a dictionary."""
        # TODO performance-test this and improve as needed
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        """Return the path string."""
        return self.path  # pragma: no cover
