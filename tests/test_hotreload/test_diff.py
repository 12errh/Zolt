"""Phase 6 — IR diff tests."""

from __future__ import annotations

from pyui.compiler.ir import IRNode


def _node(type: str, props: dict, children: list = None, variant: str | None = None) -> IRNode:
    if children is None:
        children = []
    return IRNode(
        type=type,
        props=props,
        children=children,
        events={},
        reactive_bindings=[],
        reactive_props={},
        style_variant=variant,
        theme_tokens={},
    )


def test_diff_identical_nodes_empty_patch() -> None:
    from pyui.hotreload.diff import diff_ir

    node = _node("button", {"label": "OK"}, variant="primary")
    assert diff_ir(node, node) == []


def test_diff_detects_prop_change() -> None:
    from pyui.hotreload.diff import diff_ir

    old = _node("text", {"content": "Hello"})
    new = _node("text", {"content": "World"})
    patches = diff_ir(old, new)
    assert len(patches) == 1
    assert patches[0]["op"] == "update_prop"
    assert patches[0]["key"] == "content"
    assert patches[0]["value"] == "World"


def test_diff_detects_variant_change() -> None:
    from pyui.hotreload.diff import diff_ir

    old = _node("button", {"label": "Go"}, variant="primary")
    new = _node("button", {"label": "Go"}, variant="danger")
    patches = diff_ir(old, new)
    ops = [p["op"] for p in patches]
    assert "update_variant" in ops


def test_diff_type_change_replaces_node() -> None:
    from pyui.hotreload.diff import diff_ir

    old = _node("text", {"content": "Hi"})
    new = _node("heading", {"text": "Hi", "level": 1})
    patches = diff_ir(old, new)
    assert len(patches) == 1
    assert patches[0]["op"] == "replace_node"


def test_diff_added_child() -> None:
    from pyui.hotreload.diff import diff_ir

    child = _node("text", {"content": "new"})
    old = _node("flex", {})
    new = _node("flex", {}, children=[child])
    patches = diff_ir(old, new)
    ops = [p["op"] for p in patches]
    assert "add_child" in ops


def test_diff_removed_child() -> None:
    from pyui.hotreload.diff import diff_ir

    child = _node("text", {"content": "bye"})
    old = _node("flex", {}, children=[child])
    new = _node("flex", {})
    patches = diff_ir(old, new)
    ops = [p["op"] for p in patches]
    assert "remove_child" in ops


def test_diff_no_change_on_same_props() -> None:
    from pyui.hotreload.diff import diff_ir

    old = _node("button", {"label": "Save", "type": "button"}, variant="primary")
    new = _node("button", {"label": "Save", "type": "button"}, variant="primary")
    assert diff_ir(old, new) == []


def test_diff_pages_title_change_triggers_reload() -> None:
    from pyui.compiler.ir import IRPage
    from pyui.hotreload.diff import diff_pages

    old_page = IRPage(route="/", title="Old", layout="default", children=[])
    new_page = IRPage(route="/", title="New", layout="default", children=[])
    patches = diff_pages(old_page, new_page)
    assert any(p["op"] == "reload_page" for p in patches)


def test_diff_pages_no_change_empty() -> None:
    from pyui.compiler.ir import IRPage
    from pyui.hotreload.diff import diff_pages

    page = IRPage(route="/", title="Home", layout="default", children=[])
    assert diff_pages(page, page) == []
