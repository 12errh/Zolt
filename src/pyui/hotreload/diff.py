"""
IR diff — compare two IRNode trees and produce a minimal patch list.

Each patch operation is a plain dict::

    {"op": "update_prop",    "node_id": "...", "key": "content", "value": "..."}
    {"op": "update_variant", "node_id": "...", "value": "primary"}
    {"op": "add_child",      "node_id": "...", "index": 2,       "child": {...}}
    {"op": "remove_child",   "node_id": "...", "index": 2}
    {"op": "replace_node",   "node_id": "...", "node": {...}}

Usage::

    from pyui.hotreload.diff import diff_ir, diff_pages

    patches = diff_ir(old_node, new_node)
    page_patches = diff_pages(old_ir_page, new_ir_page)
"""

from __future__ import annotations

from typing import Any

from pyui.compiler.ir import IRNode, IRPage

# Props that are internal/non-serialisable and should be skipped in diffs
_SKIP_PROPS = {"render_fn", "class_name"}


def diff_ir(old: IRNode, new: IRNode) -> list[dict[str, Any]]:
    """
    Recursively diff two :class:`~pyui.compiler.ir.IRNode` trees.

    Returns a flat list of patch operations needed to transform *old* into
    *new*.  An empty list means the trees are identical.

    Parameters
    ----------
    old : IRNode
    new : IRNode

    Returns
    -------
    list[dict[str, Any]]
    """
    patches: list[dict[str, Any]] = []

    # If the type changed entirely, replace the whole node
    if old.type != new.type:
        patches.append({"op": "replace_node", "node_id": old.node_id, "node": _serialise(new)})
        return patches

    # Diff props
    for key, new_val in new.props.items():
        if key in _SKIP_PROPS:
            continue
        old_val = old.props.get(key)
        if _serialisable(new_val) and new_val != old_val:
            patches.append(
                {
                    "op": "update_prop",
                    "node_id": old.node_id,
                    "key": key,
                    "value": new_val,
                }
            )

    # Diff style variant
    if old.style_variant != new.style_variant:
        patches.append(
            {
                "op": "update_variant",
                "node_id": old.node_id,
                "value": new.style_variant,
            }
        )

    # Diff children
    old_children = old.children
    new_children = new.children

    # Removed children
    for i in range(len(old_children) - 1, len(new_children) - 1, -1):
        patches.append({"op": "remove_child", "node_id": old.node_id, "index": i})

    # Added children
    for i in range(len(old_children), len(new_children)):
        patches.append(
            {
                "op": "add_child",
                "node_id": old.node_id,
                "index": i,
                "child": _serialise(new_children[i]),
            }
        )

    # Recurse into shared children
    for old_child, new_child in zip(old_children, new_children, strict=False):
        patches.extend(diff_ir(old_child, new_child))

    return patches


def diff_pages(old: IRPage, new: IRPage) -> list[dict[str, Any]]:
    """
    Diff two :class:`~pyui.compiler.ir.IRPage` objects.

    Returns patch operations for all changed nodes across the page's
    top-level children.
    """
    patches: list[dict[str, Any]] = []

    # Page-level metadata changes trigger a full reload signal
    if old.title != new.title or old.layout != new.layout:
        patches.append({"op": "reload_page", "route": new.route})
        return patches

    # Diff top-level children pairwise
    for old_child, new_child in zip(old.children, new.children, strict=False):
        patches.extend(diff_ir(old_child, new_child))

    # Added/removed top-level children → full reload (simpler than DOM surgery)
    if len(old.children) != len(new.children):
        patches.append({"op": "reload_page", "route": new.route})

    return patches


# ── Helpers ───────────────────────────────────────────────────────────────────


def _serialisable(value: Any) -> bool:
    """Return True if *value* can be JSON-serialised safely."""
    return isinstance(value, (str, int, float, bool, type(None), list, dict))


def _serialise(node: IRNode) -> dict[str, Any]:
    """Shallow serialise an IRNode for patch payloads."""
    return {
        "node_id": node.node_id,
        "type": node.type,
        "props": {k: v for k, v in node.props.items() if _serialisable(v) and k not in _SKIP_PROPS},
        "style_variant": node.style_variant,
        "children": [_serialise(c) for c in node.children],
    }
