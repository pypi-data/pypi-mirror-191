"""Flywheel storage library."""
from importlib.metadata import version

from .errors import *  # pylint: disable=redefined-builtin
from .storage import Storage, create_storage_client, create_storage_config

__version__ = version(__name__)

# pylint: disable=duplicate-code
__all__ = [
    "FileExists",
    "FileNotFound",
    "IsADirectory",
    "NotADirectory",
    "PermError",
    "Storage",
    "StorageError",
    "create_storage_client",
    "create_storage_config",
]
