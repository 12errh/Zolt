"""
FloatingNav component — fixed-position glassmorphism navigation bar.

Renders as a fixed pill at the top of the viewport with a logo on the
left and navigation links + CTA on the right.

Example::

    from pyui.components.navigation.floating_nav import FloatingNav

    FloatingNav(
        logo_src="/images/logo.png",
        logo_alt="Studio",
        links=["Home", "Services", "Work", "Process"],
        cta_text="Get Started",
        cta_href="#",
    )
"""

from __future__ import annotations

from typing import Any

from pyui.components.base import BaseComponent


class FloatingNav(BaseComponent):
    """
    A fixed glassmorphism navigation bar.

    Parameters
    ----------
    logo_src : str | None
        Path to the logo image.
    logo_alt : str
        Alt text for the logo.
    links : list[str | tuple[str, str]]
        Navigation links. Each item is either a label string (href="#")
        or a ``(label, href)`` tuple.
    cta_text : str | None
        Text for the primary CTA button. If None, no CTA is shown.
    cta_href : str
        URL for the CTA button.
    """

    component_type = "floating_nav"

    def __init__(
        self,
        logo_src: str | None = None,
        logo_alt: str = "",
        links: list[str | tuple[str, str]] | None = None,
        cta_text: str | None = "Get Started",
        cta_href: str = "#",
    ) -> None:
        super().__init__()
        # Normalise links to (label, href) tuples
        normalised: list[tuple[str, str]] = []
        for item in links or []:
            if isinstance(item, str):
                normalised.append((item, "#"))
            else:
                normalised.append(tuple(item))  # type: ignore[arg-type]

        self.props: dict[str, Any] = {
            "logo_src": logo_src,
            "logo_alt": logo_alt,
            "links": normalised,
            "cta_text": cta_text,
            "cta_href": cta_href,
        }

    def __repr__(self) -> str:
        return f"FloatingNav(links={len(self.props['links'])})"
