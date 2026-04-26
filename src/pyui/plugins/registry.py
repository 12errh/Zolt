"""
Component registry — maps string names to component classes.

Third-party plugins call :func:`register_component` in their
:meth:`~pyui.plugins.base.PyUIPlugin.on_load` hook to make their
components available as first-class PyUI components.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyui.exceptions import PluginError

if TYPE_CHECKING:
    from pyui.components.base import BaseComponent

# Global registry: component_type_name → class
_REGISTRY: dict[str, type[BaseComponent]] = {}


def register_component(name: str, component_class: type[BaseComponent]) -> None:
    """
    Register a component class under *name*.

    Parameters
    ----------
    name : str
        The component type name (e.g. ``"LineChart"``).  Must be unique.
    component_class : type[BaseComponent]
        The component class to register.

    Raises
    ------
    PluginError
        If *name* is already registered by a different class.
    """
    existing = _REGISTRY.get(name)
    if existing is not None and existing is not component_class:
        raise PluginError(
            f"Component {name!r} is already registered by {existing!r}. "
            "Use a unique name or unregister the existing component first."
        )
    _REGISTRY[name] = component_class


def get_component(name: str) -> type[BaseComponent] | None:
    """Return the registered component class for *name*, or ``None``."""
    return _REGISTRY.get(name)


def list_components() -> dict[str, type[Any]]:
    """Return a copy of the full registry."""
    return dict(_REGISTRY)


def unregister_component(name: str) -> None:
    """Remove *name* from the registry. Useful in tests."""
    _REGISTRY.pop(name, None)


def clear_registry() -> None:
    """Clear all registered components. Useful in tests."""
    _REGISTRY.clear()
