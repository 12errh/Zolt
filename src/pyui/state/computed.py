"""
Computed values — reactive values derived from other reactive values.

Usage::

    from pyui.state.reactive import reactive
    from pyui.state.computed import computed

    count = reactive(3)
    doubled = computed(lambda: count.get() * 2)

    doubled.get()  # → 6
    count.set(5)
    doubled.get()  # → 10
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from pyui.state.reactive import _REACTIVE_CONTEXT, ReactiveVar

T = TypeVar("T")


class ComputedVar(ReactiveVar[T]):
    """
    A read-only :class:`~pyui.state.reactive.ReactiveVar` whose value
    is derived from a computation function.

    Automatically tracks dependencies: any ``ReactiveVar`` accessed
    via ``.get()`` during the computation is registered as a dependency,
    and this var will update whenever they do.
    """

    def __init__(self, fn: Callable[[], T]) -> None:
        self._fn = fn
        self._dependencies: set[ReactiveVar[Any]] = set()
        self._unsubscribers: list[Callable[[], None]] = []

        # Initial run to capture dependencies
        _REACTIVE_CONTEXT.append(set())
        try:
            val = fn()
            deps = _REACTIVE_CONTEXT.pop()
        except Exception:
            _REACTIVE_CONTEXT.pop()
            raise

        super().__init__(val)
        self._dependencies = deps
        self._setup_subscriptions()

    def get(self) -> T:
        """Return the cached value and report access for dependency tracking."""
        from pyui.state.reactive import _report_access

        _report_access(self)
        return self._value

    def set(self, value: T) -> None:
        """Computed vars are read-only. Raises ``AttributeError``."""
        raise AttributeError("Cannot set a computed value directly.")

    def invalidate(self) -> None:
        """
        Recompute the value and notify subscribers if it changed.
        Also refreshes dependency subscriptions if the execution path changed.
        """
        _REACTIVE_CONTEXT.append(set())
        try:
            new_val = self._fn()
            new_deps = _REACTIVE_CONTEXT.pop()
        except Exception:
            _REACTIVE_CONTEXT.pop()
            raise

        old_val = self._value
        self._value = new_val

        # If dependencies changed (e.g. conditional logic), update subscriptions
        if new_deps != self._dependencies:
            self._dependencies = new_deps
            self._setup_subscriptions()

        if old_val != new_val:
            self._notify()

    def _setup_subscriptions(self) -> None:
        """Clear existing subscriptions and create new ones for current dependencies."""
        for unsub in self._unsubscribers:
            unsub()
        self._unsubscribers.clear()

        for dep in self._dependencies:
            # When a dependency changes, trigger invalidation
            unsub = dep.subscribe(lambda _: self.invalidate())
            self._unsubscribers.append(unsub)

    def __repr__(self) -> str:
        return f"ComputedVar(value={self._value!r}, deps={len(self._dependencies)})"


def computed(fn: Callable[[], T]) -> ComputedVar[T]:
    """
    Create a :class:`ComputedVar` from a zero-argument callable.

    Automatically tracks accessed reactive variables::

        count   = reactive(1)
        doubled = computed(lambda: count.get() * 2)

        doubled.get() # → 2
        count.set(10)
        doubled.get() # → 20 (auto-updated)
    """
    return ComputedVar(fn)
