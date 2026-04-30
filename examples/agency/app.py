"""
Zolt Example — AI Agency Landing Page

A dark, premium single-page landing page showcasing:
- Liquid glass (glassmorphism) effects via custom CSS
- HLS video backgrounds (Section + VideoBg components)
- Word-by-word blur-in headline (BlurHeading component)
- Fixed glassmorphism navbar (FloatingNav component)
- Custom fonts (Instrument Serif + Barlow)

Run with:
    zolt run examples/agency/app.py

"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from sections.cta_footer import CtaFooter  # noqa: E402
from sections.features_chess import FeaturesChess  # noqa: E402
from sections.features_grid import FeaturesGrid  # noqa: E402
from sections.hero import HeroSection  # noqa: E402
from sections.navbar import Navbar  # noqa: E402
from sections.start import StartSection  # noqa: E402
from sections.stats import StatsSection  # noqa: E402
from sections.testimonials import Testimonials  # noqa: E402
from styles import AGENCY_CSS  # noqa: E402

from pyui import App, Flex, Page  # noqa: E402

_HLS_CDN = "https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"


class LandingPage(Page):
    title = "Studio — AI-Powered Web Design"
    route = "/"
    layout = "full-width"

    def compose(self) -> None:
        with Flex(direction="col").className("bg-black min-h-screen"):
            Navbar().compose()
            HeroSection().compose()
            with Flex(direction="col").className("bg-black"):
                FeaturesChess().compose()
                FeaturesGrid().compose()
                StartSection().compose()
                StatsSection().compose()
                Testimonials().compose()
                CtaFooter().compose()


class AgencyApp(App):
    name = "Studio — AI Web Design"
    description = "Stunning design. Blazing performance. Built by AI."
    theme = {
        "color.background": "#000000",
        "color.text": "#ffffff",
        "color.primary": "#ffffff",
        "color.surface": "#0a0a0a",
        "color.border": "rgba(255,255,255,0.2)",
    }
    extra_css = AGENCY_CSS
    head_scripts = [_HLS_CDN]
    home = LandingPage()
