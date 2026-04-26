"""Plugin system package."""

from pyui.plugins.base import PyUIPlugin
from pyui.plugins.loader import load_plugins
from pyui.plugins.registry import get_component, list_components, register_component

__all__ = [
    "PyUIPlugin",
    "register_component",
    "get_component",
    "list_components",
    "load_plugins",
]
