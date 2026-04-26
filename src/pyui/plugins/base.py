"""
PyUIPlugin — base class for all PyUI plugins.

Third-party packages subclass this and register it via ``App.plugins``::

    from pyui.plugins import PyUIPlugin, register_component

    class ChartsPlugin(PyUIPlugin):
        name = "pyui-charts"
        version = "1.0.0"

        def on_load(self, app):
            register_component("LineChart", LineChartComponent)

    class MyApp(App):
        plugins = [ChartsPlugin()]
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyui.app import App
    from pyui.compiler.ir import IRTree


class PyUIPlugin:
    """
    Base class for PyUI plugins.

    Subclass this and override the lifecycle hooks you need.
    All hooks are optional — the default implementations are no-ops.

    Attributes
    ----------
    name : str
        Unique plugin identifier (e.g. ``"pyui-charts"``).
    version : str
        Plugin version string.
    """

    name: str = "unnamed-plugin"
    version: str = "0.0.0"

    # ── Lifecycle hooks ───────────────────────────────────────────────────────

    def on_load(self, app: type[App]) -> None:
        """Called once when the plugin is loaded by the App."""

    def on_compile_start(self, ir: IRTree) -> None:
        """Called before the compiler begins building the IR tree."""

    def on_compile_end(self, ir: IRTree) -> None:
        """Called after the IR tree is fully built."""

    def on_build(self, output_path: Path) -> None:
        """Called after ``pyui build`` writes output to disk."""

    def on_dev_start(self, server: Any) -> None:
        """Called when the dev server starts."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, version={self.version!r})"
