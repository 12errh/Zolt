"""
File watcher — monitors a directory for changes and fires a callback.

Uses watchdog under the hood. The callback receives the changed file path.

Usage::

    watcher = FileWatcher("/path/to/project", on_change=lambda p: print(p))
    watcher.start()
    # ... later ...
    watcher.stop()
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from pyui.utils.logging import get_logger

log = get_logger(__name__)

# File extensions that trigger a reload
_WATCHED_EXTENSIONS = {".py"}


class _ChangeHandler(FileSystemEventHandler):
    def __init__(self, on_change: Callable[[str], None]) -> None:
        super().__init__()
        self._on_change = on_change
        self._lock = threading.Lock()
        self._last_path: str | None = None

    def on_modified(self, event: FileSystemEvent) -> None:
        self._dispatch(event)

    def on_created(self, event: FileSystemEvent) -> None:
        self._dispatch(event)

    def _dispatch(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = str(event.src_path)
        if Path(path).suffix not in _WATCHED_EXTENSIONS:
            return
        # Debounce: skip duplicate events for the same path
        with self._lock:
            if path == self._last_path:
                return
            self._last_path = path

        log.debug("File changed", path=path)
        try:
            self._on_change(path)
        except Exception as exc:
            log.error("on_change callback raised", error=str(exc))

        # Reset debounce after a short delay
        def _reset() -> None:
            import time

            time.sleep(0.1)
            with self._lock:
                if self._last_path == path:
                    self._last_path = None

        threading.Thread(target=_reset, daemon=True).start()


class FileWatcher:
    """
    Watch a directory for Python file changes.

    Parameters
    ----------
    path : str
        Directory to watch (recursively).
    on_change : Callable[[str], None]
        Called with the changed file path whenever a ``.py`` file is
        modified or created.
    """

    def __init__(self, path: str, on_change: Callable[[str], None]) -> None:
        self._path = path
        self._handler = _ChangeHandler(on_change)
        self._observer = Observer()
        self._observer.schedule(self._handler, path, recursive=True)

    def start(self) -> None:
        """Start watching in a background thread."""
        self._observer.start()
        log.debug("FileWatcher started", path=self._path)

    def stop(self) -> None:
        """Stop the watcher and join the background thread."""
        self._observer.stop()
        self._observer.join()
        log.debug("FileWatcher stopped")

    def __enter__(self) -> FileWatcher:
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()
