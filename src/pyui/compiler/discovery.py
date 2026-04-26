"""
App class discovery — import a user module and return the App subclass.

This is Step 1 of the PyUI compilation pipeline.

Usage::

    from pyui.compiler.discovery import discover_app

    AppClass = discover_app("path/to/app.py")
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pyui.exceptions import AppNotFoundError, ModuleImportError, PyUIError

if TYPE_CHECKING:
    from pyui.app import App


def discover_app(module_path: str) -> type[App]:
    """
    Import the Python module at *module_path* and return the first
    :class:`~pyui.app.App` subclass found.

    Parameters
    ----------
    module_path : str
        Absolute or relative path to the ``.py`` file containing the App.

    Returns
    -------
    type[App]
        The discovered App subclass.

    Raises
    ------
    PyUIError
        If the file cannot be imported or no ``App`` subclass is found.
    FileNotFoundError
        If *module_path* does not exist.
    """
    from pyui.app import App  # import here to avoid circular at startup

    path = Path(module_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"App file not found: {path}")

    # Add the file's parent directory to sys.path so relative imports work
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)

    module_name = f"_pyui_user_app_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise ModuleImportError(f"Cannot create module spec for {path}")

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ModuleImportError(
            f"Error importing '{path}': {exc}\n"
            f"  Check that the file is valid Python and all imports are available."
        ) from exc

    candidates: list[type[App]] = []
    for _name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, App) and obj is not App and obj.__module__ == module_name:
            candidates.append(obj)

    if not candidates:
        raise AppNotFoundError(
            f"No App subclass found in '{path}'.\n"
            f"  Create a class that inherits from pyui.App:\n\n"
            f"    from pyui import App\n"
            f"    class MyApp(App):\n"
            f"        name = 'My App'\n"
            f"        home = HomePage()"
        )

    if len(candidates) > 1:
        names = [c.__name__ for c in candidates]
        # Take the first one, warn about ambiguity
        import warnings

        warnings.warn(
            f"Multiple App subclasses found: {names}. "
            f"Using '{names[0]}'. Add an 'app' attribute to disambiguate.",
            stacklevel=2,
        )

    return candidates[0]
