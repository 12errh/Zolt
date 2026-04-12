"""
Shared pytest fixtures and configuration.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """
    Reset the global state store between tests so tests don't bleed state.
    """
    from pyui.state.store import store
    store.reset()
    yield  # type: ignore[misc]
    store.reset()
