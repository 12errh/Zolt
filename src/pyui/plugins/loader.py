"""
Plugin loader — instantiates and calls on_load for all plugins on an App.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pyui.exceptions import PluginError
from pyui.utils.logging import get_logger

if TYPE_CHECKING:
    from pyui.app import App
    from pyui.plugins.base import PyUIPlugin

log = get_logger(__name__)


def load_plugins(app_class: type[App]) -> list[PyUIPlugin]:
    """
    Load all plugins declared on *app_class*.

    Calls :meth:`~pyui.plugins.base.PyUIPlugin.on_load` for each plugin
    in ``app_class.plugins``.

    Parameters
    ----------
    app_class : type[App]

    Returns
    -------
    list[PyUIPlugin]
        The list of loaded plugin instances.

    Raises
    ------
    PluginError
        If any plugin's ``on_load`` raises.
    """
    plugins: list[PyUIPlugin] = list(getattr(app_class, "plugins", []))

    for plugin in plugins:
        try:
            plugin.on_load(app_class)
            log.debug("Plugin loaded", name=plugin.name, version=plugin.version)
        except Exception as exc:
            raise PluginError(f"Plugin {plugin.name!r} failed during on_load: {exc}") from exc

    return plugins
