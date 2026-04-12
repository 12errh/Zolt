"""PyUI exception hierarchy."""

from __future__ import annotations


class PyUIError(Exception):
    """Base exception for all PyUI errors."""


class CompilerError(PyUIError):
    """Raised when the PyUI compiler encounters an error."""


class ComponentError(PyUIError):
    """Raised when a component is configured or used incorrectly."""


class ThemeError(PyUIError):
    """Raised when themes or design tokens are invalid."""


class PluginError(PyUIError):
    """Raised when a plugin fails to load or raises during a lifecycle hook."""
