"""
Section component — semantic <section> with relative positioning.

The foundation for video-background sections. Children are stacked
on top of the section via z-index.

Example::

    from pyui.components.layout.section import Section

    with Section(min_height=560):
        VideoSection(src="...", hls=True)
        Flex(direction="col", align="center").add(
            Heading("Title")
        )
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class Section(BaseComponent):
    """
    A semantic ``<section>`` wrapper with ``position:relative`` and
    ``overflow:hidden`` — the standard container for video-background layouts.

    Parameters
    ----------
    min_height : int
        Minimum height in pixels (default 400).
    bg : str | None
        Background colour (CSS value, e.g. ``"#000"``).
    """

    component_type = "section"

    def __init__(
        self,
        min_height: int = 400,
        bg: str | None = "#000",
    ) -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "min_height": min_height,
            "bg": bg,
        }

    def __repr__(self) -> str:
        return f"Section(min_height={self.props['min_height']!r})"
