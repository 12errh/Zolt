"""Hot reload package — file watcher and IR diff."""

from pyui.hotreload.diff import diff_ir
from pyui.hotreload.watcher import FileWatcher

__all__ = ["FileWatcher", "diff_ir"]
