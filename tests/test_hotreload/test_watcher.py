"""Phase 6 — FileWatcher tests."""

from __future__ import annotations

import time


def test_file_change_triggers_callback(tmp_path: object) -> None:
    """Writing a .py file must fire the on_change callback."""
    from pathlib import Path

    from pyui.hotreload.watcher import FileWatcher

    assert isinstance(tmp_path, Path)
    f = tmp_path / "app.py"
    f.write_text("# version 1", encoding="utf-8")

    called: list[str] = []
    watcher = FileWatcher(str(tmp_path), on_change=lambda p: called.append(p))
    watcher.start()
    time.sleep(0.15)

    f.write_text("# version 2", encoding="utf-8")
    time.sleep(0.6)

    watcher.stop()
    assert len(called) > 0


def test_non_py_file_does_not_trigger(tmp_path: object) -> None:
    """Changing a .txt file must NOT fire the callback."""
    from pathlib import Path

    from pyui.hotreload.watcher import FileWatcher

    assert isinstance(tmp_path, Path)
    f = tmp_path / "notes.txt"
    f.write_text("hello", encoding="utf-8")

    called: list[str] = []
    watcher = FileWatcher(str(tmp_path), on_change=lambda p: called.append(p))
    watcher.start()
    time.sleep(0.15)

    f.write_text("world", encoding="utf-8")
    time.sleep(0.4)

    watcher.stop()
    assert len(called) == 0


def test_watcher_context_manager(tmp_path: object) -> None:
    """FileWatcher must work as a context manager."""
    from pathlib import Path

    from pyui.hotreload.watcher import FileWatcher

    assert isinstance(tmp_path, Path)
    called: list[str] = []
    with FileWatcher(str(tmp_path), on_change=lambda p: called.append(p)):
        f = tmp_path / "test.py"
        f.write_text("x = 1", encoding="utf-8")
        time.sleep(0.4)
    # No assertion on called — just verifying no exception
