"""
VideoBg component — full-cover background video with optional HLS support.

Designed to be placed inside a Section component. Renders absolutely
positioned, fills the parent, with optional top/bottom gradient fades.

Example::

    from pyui.components.media.video_bg import VideoBg

    with Section(min_height=560):
        VideoBg(
            src="https://stream.mux.com/...",
            hls=True,
            fade_height=160,
        )
        # content on top (z-index handled automatically)
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class VideoBg(BaseComponent):
    """
    Absolutely-positioned background video that fills its parent ``Section``.

    Parameters
    ----------
    src : str
        Video URL. For HLS streams use a ``.m3u8`` URL and set ``hls=True``.
    hls : bool
        If True, initialises hls.js for HLS stream playback.
    desaturate : bool
        If True, applies ``filter: saturate(0)`` (greyscale).
    fade_height : int
        Height in px of the top and bottom gradient fades (default 160).
        Set to 0 to disable fades.
    poster : str | None
        Poster image URL shown before the video loads.
    """

    component_type = "video_bg"

    def __init__(
        self,
        src: str = "",
        hls: bool = False,
        desaturate: bool = False,
        fade_height: int = 160,
        poster: str | None = None,
    ) -> None:
        super().__init__()
        self.props: dict[str, Any] = {
            "src": src,
            "hls": hls,
            "desaturate": desaturate,
            "fade_height": fade_height,
            "poster": poster,
        }

    def __repr__(self) -> str:
        return f"VideoBg(src={self.props['src']!r}, hls={self.props['hls']!r})"
