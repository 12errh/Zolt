"""CTA + Footer — pure Zolt, HLS video."""

from pyui import Flex, Link, Section, Text, VideoBg

MUX_CTA = "https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8"


class CtaFooter:
    def compose(self) -> None:
        with Section(min_height=700, bg="#000"):
            VideoBg(src=MUX_CTA, hls=True, fade_height=160)

            # CTA content
            with Flex(direction="col", align="center", justify="center", gap=8).className(
                "relative z-10 w-full min-h-[600px] text-center py-24 px-8"
            ):
                Text("Your next website starts here.").className(
                    "font-heading text-white leading-none "
                    "text-5xl md:text-6xl lg:text-7xl "
                    "max-w-3xl mx-auto"
                )

                Text(
                    "Book a free strategy call. See what AI-powered design "
                    "can do. No commitment, no pressure. Just possibilities."
                ).className(
                    "text-white/60 font-body font-light text-sm md:text-base max-w-md mx-auto"
                ).paragraph()

                with Flex(direction="row", align="center", justify="center", gap=4):
                    Link("Book a Call", href="#").style("glass")
                    Link("View Pricing", href="#").style("primary")

            # Footer bar
            with Flex(direction="row", align="center", justify="between").className(
                "relative z-10 w-full px-8 py-8 border-t border-white/10"
            ):
                Text("© 2026 Studio. All rights reserved.").className(
                    "text-white/40 text-xs font-body"
                )
                with Flex(direction="row", align="center", gap=6):
                    for label in ["Privacy", "Terms", "Contact"]:
                        Link(label, href="#").style("footer")
