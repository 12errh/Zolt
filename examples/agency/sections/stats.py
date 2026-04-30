"""Stats — pure Zolt, desaturated HLS video."""

from pyui import Flex, Grid, Section, Text, VideoBg

MUX_STATS = "https://stream.mux.com/NcU3HlHeF7CUL86azTTzpy3Tlb00d6iF3BmCdFslMJYM.m3u8"

STATS = [
    ("200+", "Sites launched"),
    ("98%", "Client satisfaction"),
    ("3.2x", "More conversions"),
    ("5 days", "Average delivery"),
]


class StatsSection:
    def compose(self) -> None:
        with Section(min_height=500, bg="#000"):
            VideoBg(src=MUX_STATS, hls=True, desaturate=True, fade_height=160)

            with (
                Flex(direction="col", align="center", justify="center").className(
                    "relative z-10 w-full min-h-[500px] py-24 px-8"
                ),
                Flex(direction="col").className(
                    "liquid-glass rounded-3xl p-12 md:p-16 w-full max-w-5xl mx-auto"
                ),
                Grid(cols=4, gap=8).className("grid-cols-2 md:grid-cols-4 text-center"),
            ):
                for value, label in STATS:
                    with Flex(direction="col", align="center", gap=2):
                        Text(value).className(
                            "font-heading text-white text-4xl md:text-5xl lg:text-6xl leading-none"
                        )
                        Text(label).className("text-white/60 font-body font-light text-sm")
