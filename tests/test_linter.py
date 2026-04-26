"""Phase 6 — Linter tests."""

from __future__ import annotations


def test_clean_app_no_warnings() -> None:
    from pyui import App, Button, Page, Text
    from pyui.linter import lint_app

    class CleanApp(App):
        home = Page(title="Home", route="/")
        home.add(Text("Hello"), Button("Go").style("primary"))

    assert lint_app(CleanApp) == []


def test_image_missing_alt_warns() -> None:
    from pyui import App, Image, Page
    from pyui.linter import lint_app

    class ImgApp(App):
        home = Page(title="Home", route="/")
        home.add(Image(src="photo.jpg", alt=""))

    warnings = lint_app(ImgApp)
    assert any("alt" in w["message"] for w in warnings)
    assert all(w["level"] == "warning" for w in warnings)


def test_image_with_alt_no_warning() -> None:
    from pyui import App, Image, Page
    from pyui.linter import lint_app

    class ImgApp(App):
        home = Page(title="Home", route="/")
        home.add(Image(src="photo.jpg", alt="A scenic mountain view"))

    warnings = lint_app(ImgApp)
    assert not any("alt" in w["message"] for w in warnings)


def test_empty_page_warns() -> None:
    from pyui import App, Page
    from pyui.linter import lint_app

    class EmptyApp(App):
        home = Page(title="Home", route="/")

    warnings = lint_app(EmptyApp)
    assert any("no components" in w["message"] for w in warnings)


def test_duplicate_routes_error() -> None:
    from pyui import App, Page, Text
    from pyui.linter import lint_app

    class DupApp(App):
        home = Page(title="Home", route="/")
        home.add(Text("A"))
        also_home = Page(title="Also Home", route="/")
        also_home.add(Text("B"))

    warnings = lint_app(DupApp)
    assert any(w["level"] == "error" and "Duplicate route" in w["message"] for w in warnings)


def test_unknown_variant_warns() -> None:
    from pyui import App, Button, Page
    from pyui.linter import lint_app

    class BadVariantApp(App):
        home = Page(title="Home", route="/")
        home.add(Button("Go").style("nonexistent_variant"))

    warnings = lint_app(BadVariantApp)
    assert any("unknown variant" in w["message"] for w in warnings)


def test_valid_variant_no_warning() -> None:
    from pyui import App, Button, Page
    from pyui.linter import lint_app

    class GoodApp(App):
        home = Page(title="Home", route="/")
        home.add(Button("Go").style("primary"))

    warnings = lint_app(GoodApp)
    assert not any("unknown variant" in w["message"] for w in warnings)


def test_hot_reload_script_in_page() -> None:
    """Rendered page must include the hot-reload WebSocket script."""
    from pyui import Page
    from pyui.renderers.web import render_page

    html = render_page(Page(title="T", route="/"))
    assert "/pyui-api/ws" in html
    assert "WebSocket" in html


def test_error_overlay_in_page() -> None:
    """Rendered page must include the error overlay handler."""
    from pyui import Page
    from pyui.renderers.web import render_page

    html = render_page(Page(title="T", route="/"))
    assert "__pyui_error_overlay" in html
