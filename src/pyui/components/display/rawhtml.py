"""
RawHTML component — inject arbitrary HTML into the DOM.

This is an escape hatch for advanced users who need to inject raw HTML,
CSS, or JavaScript that cannot be expressed through standard PyUI components.

Warning: Using this component with user-supplied data can lead to XSS attacks.
Always sanitize input if rendering dynamic content.

Example::

    from pyui import RawHTML

    RawHTML("<style>.custom {{ color: red; }}</style>")
    RawHTML("<div class='my-custom-component'>Hello</div>")
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class RawHTML(BaseComponent):
    """
    Renders raw, unescaped HTML content.

    Parameters
    ----------
    html : str
        Raw HTML string to inject into the DOM.

    Warning
    -------
    This component bypasses PyUI's safety mechanisms. Only use with
    trusted content to avoid XSS vulnerabilities.
    """

    component_type = "raw_html"

    def __init__(self, html: str = "") -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "html": html,
        }

    def __repr__(self) -> str:
        return f"RawHTML(html={self.props['html']!r})"
