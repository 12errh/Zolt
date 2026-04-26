"""
PyUI linter — validates component trees and reports issues.

Checks performed:
- Images missing alt text
- Pages missing a route
- Duplicate routes
- Empty pages (no children)
- Components with unknown style variants (warning only)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyui.app import App

# Known valid style variants per component type
_VALID_VARIANTS: dict[str, set[str]] = {
    "button": {"primary", "secondary", "ghost", "danger", "success", "link", "gradient"},
    "badge": {"primary", "secondary", "success", "warning", "danger", "info"},
    "alert": {"info", "success", "warning", "danger"},
    "text": {"muted", "code", "lead", "small", "error", "success", "caption"},
    "heading": {"gradient", "muted", "display"},
}


def lint_app(app_class: type[App]) -> list[dict[str, Any]]:
    """
    Lint all pages and components in *app_class*.

    Returns
    -------
    list[dict]
        Each item has ``level`` (``"error"`` or ``"warning"``) and ``message``.
    """
    from pyui.compiler.ir import build_ir_tree

    warnings: list[dict[str, Any]] = []

    # Build IR to get resolved component trees
    try:
        ir = build_ir_tree(app_class)
    except Exception as exc:
        warnings.append({"level": "error", "message": f"Compiler error: {exc}"})
        return warnings

    # Check for duplicate routes
    routes: list[str] = [p.route for p in ir.pages]
    seen: set[str] = set()
    for route in routes:
        if route in seen:
            warnings.append(
                {
                    "level": "error",
                    "message": f"Duplicate route: '{route}' — each page must have a unique route.",
                }
            )
        seen.add(route)

    # Walk each page
    for page in ir.pages:
        prefix = f"Page '{page.title or page.route}'"

        if not page.route:
            warnings.append({"level": "error", "message": f"{prefix}: missing route."})

        if not page.children:
            warnings.append(
                {
                    "level": "warning",
                    "message": f"{prefix}: page has no components.",
                }
            )

        # Walk component tree
        _lint_nodes(page.children, prefix, warnings)

    return warnings


def _lint_nodes(
    nodes: list[Any],
    context: str,
    warnings: list[dict[str, Any]],
) -> None:
    for node in nodes:
        # Image missing alt
        if node.type == "image":
            alt = node.props.get("alt", "")
            if not alt or not str(alt).strip():
                warnings.append(
                    {
                        "level": "warning",
                        "message": (
                            f"{context} > Image: missing 'alt' text. "
                            "Add alt='' for decorative images or a descriptive string."
                        ),
                    }
                )

        # Unknown style variant
        valid = _VALID_VARIANTS.get(node.type)
        if valid and node.style_variant and node.style_variant not in valid:
            warnings.append(
                {
                    "level": "warning",
                    "message": (
                        f"{context} > {node.type.title()}: "
                        f"unknown variant '{node.style_variant}'. "
                        f"Valid variants: {sorted(valid)}."
                    ),
                }
            )

        # Recurse
        if node.children:
            _lint_nodes(node.children, f"{context} > {node.type}", warnings)
