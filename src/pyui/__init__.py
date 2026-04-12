"""
PyUI — Write Python. Render anywhere.

Web · Desktop · CLI from a single Python codebase.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "PyUI Core Team"
__license__ = "MIT"

# ── Core classes ────────────────────────────────────────────────────────────
from pyui.app import App
from pyui.page import Page

# ── State system ────────────────────────────────────────────────────────────
from pyui.state.reactive import ReactiveVar, reactive
from pyui.state.computed import computed
from pyui.state.store import Store, store

# ── Components ───────────────────────────────────────────────────────────────
from pyui.components.base import BaseComponent
from pyui.components.input.button import Button
from pyui.components.display.text import Text
from pyui.components.display.heading import Heading

# ── Exceptions ───────────────────────────────────────────────────────────────
from pyui.exceptions import (
    PyUIError,
    CompilerError,
    ComponentError,
    ThemeError,
    PluginError,
)

__all__ = [
    # Meta
    "__version__",
    # Core
    "App",
    "Page",
    # State
    "ReactiveVar",
    "reactive",
    "computed",
    "Store",
    "store",
    # Components
    "BaseComponent",
    "Button",
    "Text",
    "Heading",
    # Exceptions
    "PyUIError",
    "CompilerError",
    "ComponentError",
    "ThemeError",
    "PluginError",
]
