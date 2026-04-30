"""Testimonials — 3-column quote cards."""

from pyui import Flex, Grid, Text

QUOTES = [
    {
        "quote": (
            "A complete rebuild in five days. The result outperformed "
            "everything we'd spent months building before."
        ),
        "name": "Sarah Chen",
        "role": "CEO, Luminary",
    },
    {
        "quote": (
            "Conversions up 4x. That's not a typo. The design just works "
            "differently when it's built on real data."
        ),
        "name": "Marcus Webb",
        "role": "Head of Growth, Arcline",
    },
    {
        "quote": (
            "They didn't just design our site. They defined our brand. "
            "World-class doesn't begin to cover it."
        ),
        "name": "Elena Voss",
        "role": "Brand Director, Helix",
    },
]


class Testimonials:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            # Section header
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("What They Say").className(
                    "liquid-glass rounded-full px-3.5 py-1 "
                    "text-xs font-medium text-white font-body "
                    "inline-block"
                )
                Text("Don't take our word for it.").className(
                    "font-heading text-white tracking-tight "
                    "leading-none text-4xl md:text-5xl lg:text-6xl"
                )

            # 3-column grid
            with Grid(cols=3, gap=6).className("grid-cols-1 md:grid-cols-3"):
                for q in QUOTES:
                    with Flex(direction="col", align="start", gap=6).className(
                        "liquid-glass rounded-2xl p-8"
                    ):
                        Text(f'"{q["quote"]}"').className(
                            "text-white/80 font-body font-light "
                            "text-sm italic leading-relaxed flex-1"
                        ).paragraph()

                        with Flex(direction="col", gap=1):
                            Text(q["name"]).className("text-white font-body font-medium text-sm")
                            Text(q["role"]).className("text-white/50 font-body font-light text-xs")
