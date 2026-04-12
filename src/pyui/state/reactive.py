"""
ReactiveVar — a type-safe observable value.

Usage::

    from pyui.state.reactive import reactive

    count = reactive(0)
    count.subscribe(lambda v: print(f"count changed to {v}"))
    count.set(1)   # prints "count changed to 1"
    count.get()    # → 1
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar

# Registry to track all ReactiveVar instances and their names
REACTIVE_VAR_REGISTRY: dict[ReactiveVar[Any], str] = {}


def register_reactive_name(var: ReactiveVar[Any], name: str) -> None:
    """Register the name of a ReactiveVar (called by the App compiler)."""
    REACTIVE_VAR_REGISTRY[var] = name


def get_reactive_name(var: ReactiveVar[Any]) -> str | None:
    """Retrieve the name of a ReactiveVar."""
    return REACTIVE_VAR_REGISTRY.get(var)

T = TypeVar("T")


# Global stack for dependency tracking during evaluation (e.g., in computed or compiler)
_REACTIVE_CONTEXT: list[set[ReactiveVar[Any]]] = []


def _report_access(var: ReactiveVar[Any]) -> None:
    """Report that a ReactiveVar was accessed in the current context."""
    if _REACTIVE_CONTEXT:
        _REACTIVE_CONTEXT[-1].add(var)


class ReactiveVar(Generic[T]):
    """
    A reactive variable that notifies all subscribers when its value changes.

    Generic over the value type ``T``.

    Parameters
    ----------
    initial : T
        Starting value.
    """

    def __init__(self, initial: T, persist: bool = False) -> None:
        self._value: T = initial
        self._persist: bool = persist
        self._subscribers: list[Callable[[T], None]] = []

    # ── Core API ──────────────────────────────────────────────────────────────

    def get(self) -> T:
        """Return the current value."""
        _report_access(self)
        return self._value

    def set(self, value: T) -> None:
        """
        Set a new value. Notifies subscribers only if the value has changed
        (uses ``!=`` comparison).
        """
        old = self._value
        self._value = value
        if old != value:
            self._notify()

    # ── Subscriptions ─────────────────────────────────────────────────────────

    def subscribe(self, handler: Callable[[T], None]) -> Callable[[], None]:
        """
        Register a change listener.

        Returns an **unsubscribe** callable — call it to stop receiving updates::

            unsub = count.subscribe(my_handler)
            # later ...
            unsub()
        """
        self._subscribers.append(handler)

        def _unsubscribe() -> None:
            import contextlib

            with contextlib.suppress(ValueError):
                self._subscribers.remove(handler)

        return _unsubscribe

    def _notify(self) -> None:
        """Invoke all subscribers with the current value."""
        for sub in list(self._subscribers):  # copy to allow safe mutation during notify
            sub(self._value)

    # ── Arithmetic helpers (convenience) ──────────────────────────────────────

    def __add__(self, other: T) -> ReactiveVar[Any]:
        return ReactiveVar(self._value + other)  # type: ignore[operator]

    def __sub__(self, other: T) -> ReactiveVar[Any]:
        return ReactiveVar(self._value - other)  # type: ignore[operator]

    def __mul__(self, other: T) -> ReactiveVar[Any]:
        return ReactiveVar(self._value * other)  # type: ignore[operator]

    def __int__(self) -> int:
        return int(self._value)  # type: ignore[no-any-return, call-overload]

    def __float__(self) -> float:
        return float(self._value)  # type: ignore[arg-type]

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"ReactiveVar({self._value!r}, subscribers={len(self._subscribers)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ReactiveVar):
            return bool(self._value == other._value)
        return bool(self._value == other)

    def __hash__(self) -> int:
        return id(self)


def reactive(initial: T, persist: bool = False) -> ReactiveVar[T]:
    """
    Shorthand factory for :class:`ReactiveVar`.

    ::

        count = reactive(0)
        name  = reactive("PyUI")
        items = reactive([])
        token = reactive("", persist=True)
    """
    return ReactiveVar(initial, persist=persist)
