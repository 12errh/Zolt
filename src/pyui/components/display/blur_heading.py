"""
BlurHeading component — animated word-by-word blur-reveal heading.

Each word animates from blurred/invisible to sharp/visible with a
staggered delay, triggered on page load.

Example::

    from pyui.components.display.blur_heading import BlurHeading

    BlurHeading("The Website Your Brand Deserves", level=1)
    BlurHeading("You dream it. We ship it.", level=2, delay_ms=100)
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class BlurHeading(BaseComponent):
    """
    An animated heading that reveals words one by one with a blur effect.

    Parameters
    ----------
    text : str
        The heading text. Words are split on spaces.
    level : int
        Heading level 1–6 (default 1).
    delay_ms : int
        Stagger delay between words in milliseconds (default 100).
    """

    component_type = "blur_heading"

    def __init__(
        self,
        text: str = "",
        level: int = 1,
        delay_ms: int = 100,
    ) -> None:
        super().__init__()
        if not 1 <= level <= 6:
            raise ValueError(f"Heading level must be 1–6, got {level!r}.")
        self.props: dict[str, Any] = {
            "text": text,
            "level": level,
            "delay_ms": delay_ms,
        }

    def __repr__(self) -> str:
        return f"BlurHeading(text={self.props['text']!r}, level={self.props['level']!r})"
