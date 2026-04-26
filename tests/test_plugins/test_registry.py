"""Phase 5 — Plugin system tests."""

from __future__ import annotations

import pytest


# ── Registry ──────────────────────────────────────────────────────────────────


def test_register_and_get_component() -> None:
    from pyui.components.base import BaseComponent
    from pyui.plugins.registry import clear_registry, get_component, register_component

    clear_registry()

    class MyWidget(BaseComponent):
        component_type = "my_widget"

    register_component("MyWidget", MyWidget)
    assert get_component("MyWidget") is MyWidget
    clear_registry()


def test_register_duplicate_same_class_is_idempotent() -> None:
    from pyui.components.base import BaseComponent
    from pyui.plugins.registry import clear_registry, register_component

    clear_registry()

    class MyWidget(BaseComponent):
        component_type = "my_widget2"

    register_component("MyWidget2", MyWidget)
    register_component("MyWidget2", MyWidget)  # same class — no error
    clear_registry()


def test_register_duplicate_different_class_raises() -> None:
    from pyui.components.base import BaseComponent
    from pyui.exceptions import PluginError
    from pyui.plugins.registry import clear_registry, register_component

    clear_registry()

    class WidgetA(BaseComponent):
        component_type = "widget_a"

    class WidgetB(BaseComponent):
        component_type = "widget_b"

    register_component("Conflict", WidgetA)
    with pytest.raises(PluginError, match="already registered"):
        register_component("Conflict", WidgetB)
    clear_registry()


def test_get_unregistered_returns_none() -> None:
    from pyui.plugins.registry import clear_registry, get_component

    clear_registry()
    assert get_component("DoesNotExist") is None


def test_list_components() -> None:
    from pyui.components.base import BaseComponent
    from pyui.plugins.registry import clear_registry, list_components, register_component

    clear_registry()

    class W(BaseComponent):
        component_type = "w"

    register_component("W", W)
    components = list_components()
    assert "W" in components
    clear_registry()


def test_unregister_component() -> None:
    from pyui.components.base import BaseComponent
    from pyui.plugins.registry import (
        clear_registry,
        get_component,
        register_component,
        unregister_component,
    )

    clear_registry()

    class W2(BaseComponent):
        component_type = "w2"

    register_component("W2", W2)
    unregister_component("W2")
    assert get_component("W2") is None


# ── PyUIPlugin base class ─────────────────────────────────────────────────────


def test_plugin_base_has_required_attrs() -> None:
    from pyui.plugins.base import PyUIPlugin

    p = PyUIPlugin()
    assert hasattr(p, "name")
    assert hasattr(p, "version")
    assert hasattr(p, "on_load")
    assert hasattr(p, "on_compile_start")
    assert hasattr(p, "on_compile_end")
    assert hasattr(p, "on_build")
    assert hasattr(p, "on_dev_start")


def test_plugin_lifecycle_hooks_are_callable() -> None:
    from pyui.plugins.base import PyUIPlugin

    p = PyUIPlugin()
    # All hooks must be callable and not raise with None args
    p.on_load(None)  # type: ignore[arg-type]
    p.on_compile_start(None)  # type: ignore[arg-type]
    p.on_compile_end(None)  # type: ignore[arg-type]
    p.on_build(None)  # type: ignore[arg-type]
    p.on_dev_start(None)


def test_plugin_subclass_on_load_called() -> None:
    from pyui.plugins.base import PyUIPlugin
    from pyui.plugins.registry import clear_registry, get_component, register_component
    from pyui.components.base import BaseComponent

    clear_registry()

    class FakeWidget(BaseComponent):
        component_type = "fake_widget"

    class TestPlugin(PyUIPlugin):
        name = "test-plugin"
        version = "1.0.0"
        loaded = False

        def on_load(self, app: object) -> None:
            TestPlugin.loaded = True
            register_component("FakeWidget", FakeWidget)

    plugin = TestPlugin()
    plugin.on_load(None)

    assert TestPlugin.loaded is True
    assert get_component("FakeWidget") is FakeWidget
    clear_registry()


# ── Loader ────────────────────────────────────────────────────────────────────


def test_load_plugins_calls_on_load() -> None:
    from pyui import App, Page
    from pyui.plugins.base import PyUIPlugin
    from pyui.plugins.loader import load_plugins

    calls: list[str] = []

    class TrackPlugin(PyUIPlugin):
        name = "track"
        version = "1.0.0"

        def on_load(self, app: object) -> None:
            calls.append("loaded")

    class SampleApp(App):
        plugins = [TrackPlugin()]
        home = Page(title="H", route="/")

    load_plugins(SampleApp)
    assert calls == ["loaded"]


def test_load_plugins_raises_on_error() -> None:
    from pyui import App, Page
    from pyui.exceptions import PluginError
    from pyui.plugins.base import PyUIPlugin
    from pyui.plugins.loader import load_plugins

    class BrokenPlugin(PyUIPlugin):
        name = "broken"
        version = "1.0.0"

        def on_load(self, app: object) -> None:
            raise RuntimeError("intentional failure")

    class SampleApp(App):
        plugins = [BrokenPlugin()]
        home = Page(title="H", route="/")

    with pytest.raises(PluginError, match="intentional failure"):
        load_plugins(SampleApp)


def test_load_plugins_empty_list() -> None:
    from pyui import App, Page
    from pyui.plugins.loader import load_plugins

    class SampleApp(App):
        plugins = []
        home = Page(title="H", route="/")

    result = load_plugins(SampleApp)
    assert result == []


# ── Public API exports ────────────────────────────────────────────────────────


def test_plugin_importable_from_pyui() -> None:
    from pyui import PyUIPlugin, register_component  # noqa: F401

    assert PyUIPlugin is not None
    assert register_component is not None
