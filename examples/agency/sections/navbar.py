"""Navbar — pure Zolt FloatingNav."""

from pyui import FloatingNav


class Navbar:
    def compose(self) -> None:
        FloatingNav(
            logo_src="/images/logo-icon.png",
            logo_alt="Studio",
            links=["Home", "Services", "Work", "Process"],
            cta_text="Get Started",
            cta_href="#",
        )
