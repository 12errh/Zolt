"""
Link component — semantic <a> hyperlink.

Example::

    from pyui.components.display.link import Link

    Link("Get Started", href="#").style("primary")
    Link("Home", href="/")
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class Link(BaseComponent):
    """
    A hyperlink (``<a>``) component.

    Parameters
    ----------
    text : str
        The visible link text.
    href : str
        The URL the link points to.
    external : bool
        If True, opens in a new tab (``target="_blank"``).

    Style variants
    --------------
    ``"primary"``  — white pill button style
    ``"ghost"``    — transparent with border
    ``"nav"``      — navigation link (no underline, hover colour)
    ``"footer"``   — muted small footer link
    """

    component_type = "link"

    def __init__(
        self,
        text: str = "",
        href: str = "#",
        external: bool = False,
    ) -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "text": text,
            "href": href,
            "external": external,
            "icon": None,
            "icon_position": "right",
        }

    def icon(self, name: str, position: str = "right") -> Link:
        """Attach a Lucide icon to the link."""
        self.props["icon"] = name
        self.props["icon_position"] = position
        return self

    def external(self, value: bool = True) -> Link:
        """Open in a new tab."""
        self.props["external"] = value
        return self

    def __repr__(self) -> str:
        return f"Link(text={self.props['text']!r}, href={self.props['href']!r})"
