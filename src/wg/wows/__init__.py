"""World of Warships API client module."""

from .client import AttrDict, WargamingAPIClient

__version__ = "15.8.0"  # tracks WoWS game version
__all__ = [
    "__version__",
    "AttrDict",
    "WargamingAPIClient",
]
