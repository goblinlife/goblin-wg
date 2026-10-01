"""Wargaming API client library for Python (goblin-wg)."""

from . import wot, wows
from .core.client import BaseWargamingAPIClient

__version__ = "1.0.3"
__all__ = ["__version__", "wows", "wot", "BaseWargamingAPIClient"]
