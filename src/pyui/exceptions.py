"""
PyUI exception hierarchy with structured error codes.

Error code format: PYUI-NNN
  PYUI-001 – PYUI-099  : Compiler errors
  PYUI-100 – PYUI-199  : Component errors
  PYUI-200 – PYUI-299  : Theme errors
  PYUI-300 – PYUI-399  : Plugin errors
  PYUI-400 – PYUI-499  : CLI / runtime errors
"""

from __future__ import annotations


class PyUIError(Exception):
    """Base exception for all PyUI errors."""

    code: str = "PYUI-000"

    def __init__(self, message: str, code: str | None = None) -> None:
        self.code = code or self.__class__.code
        super().__init__(f"[{self.code}] {message}")

    @property
    def message(self) -> str:
        """The error message without the error code prefix."""
        return str(self).replace(f"[{self.code}] ", "", 1)


# ── Compiler errors (001–099) ─────────────────────────────────────────────────


class CompilerError(PyUIError):
    """Raised when the PyUI compiler encounters an error."""

    code = "PYUI-001"


class AppNotFoundError(CompilerError):
    """No App subclass found in the user's module."""

    code = "PYUI-002"


class ModuleImportError(CompilerError):
    """The user's module could not be imported."""

    code = "PYUI-003"


class MissingRouteError(CompilerError):
    """A Page is missing a required route."""

    code = "PYUI-004"


class DuplicateRouteError(CompilerError):
    """Two pages share the same route."""

    code = "PYUI-005"


class IRBuildError(CompilerError):
    """Failed to build the IR tree from the component tree."""

    code = "PYUI-006"


# ── Component errors (100–199) ────────────────────────────────────────────────


class ComponentError(PyUIError):
    """Raised when a component is configured or used incorrectly."""

    code = "PYUI-100"


class InvalidPropError(ComponentError):
    """A component received an invalid prop value."""

    code = "PYUI-101"


class UnknownComponentError(ComponentError):
    """A component type is not registered in the renderer dispatch table."""

    code = "PYUI-102"


# ── Theme errors (200–299) ────────────────────────────────────────────────────


class ThemeError(PyUIError):
    """Raised when themes or design tokens are invalid."""

    code = "PYUI-200"


class UnknownThemeError(ThemeError):
    """A built-in theme name was not recognised."""

    code = "PYUI-201"


class InvalidTokenError(ThemeError):
    """A design token key or value is invalid."""

    code = "PYUI-202"


# ── Plugin errors (300–399) ───────────────────────────────────────────────────


class PluginError(PyUIError):
    """Raised when a plugin fails to load or raises during a lifecycle hook."""

    code = "PYUI-300"


class PluginConflictError(PluginError):
    """Two plugins attempt to register the same component name."""

    code = "PYUI-301"


# ── CLI / runtime errors (400–499) ───────────────────────────────────────────


class CLIError(PyUIError):
    """Raised for CLI-level errors (bad arguments, missing files, etc.)."""

    code = "PYUI-400"


class BuildError(CLIError):
    """The build pipeline failed."""

    code = "PYUI-401"
