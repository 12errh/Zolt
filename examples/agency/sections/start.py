"""StartSection — pure Zolt, HLS video via VideoBg."""

from pyui import BlurHeading, Flex, Link, Section, Text, VideoBg

MUX_START = "https://stream.mux.com/9JXDljEVWYwWu01PUkAemafDugK89o01BR6zqJ3aS9u00A.m3u8"


class StartSection:
    def compose(self) -> None:
        with Section(min_height=560, bg="#000"):
            VideoBg(src=MUX_START, hls=True, fade_height=160)

            with Flex(direction="col", align="center", justify="center", gap=6).className(
                "relative z-10 w-full text-center min-h-[560px] py-24 px-8"
            ):
                Text("How It Works").className(
                    "liquid-glass rounded-full px-3.5 py-1 "
                    "text-xs font-medium text-white font-body inline-block"
                )

                BlurHeading(
                    "You dream it. We ship it.",
                    level=2,
                    delay_ms=120,
                ).className("text-white max-w-xl mx-auto")

                Text(
                    "Share your vision. Our AI handles the rest — "
                    "wireframes, design, code, launch. "
                    "All in days, not quarters."
                ).className(
                    "text-white/60 font-body font-light text-sm md:text-base max-w-md mx-auto"
                ).paragraph()

                Link("Get Started", href="#").style("glass").icon("arrow-up-right")
