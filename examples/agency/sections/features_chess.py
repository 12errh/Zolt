"""FeaturesChess — alternating text/gif rows."""

from pyui import Flex, Image, Text

GIF_1 = "https://motionsites.ai/assets/hero-finlytic-preview-CV9g0FHP.gif"
GIF_2 = "https://motionsites.ai/assets/hero-wealth-preview-B70idl_u.gif"

ROWS = [
    {
        "reverse": False,
        "title": "Designed to convert. Built to perform.",
        "body": (
            "Every pixel is intentional. Our AI studies what works across "
            "thousands of top sites — then builds yours to outperform them all."
        ),
        "cta": "Learn more",
        "gif": GIF_1,
        "gif_alt": "Conversion-focused design preview",
    },
    {
        "reverse": True,
        "title": "It gets smarter. Automatically.",
        "body": (
            "Your site evolves on its own. AI monitors every click, scroll, "
            "and conversion — then optimizes in real time. "
            "No manual updates. Ever."
        ),
        "cta": "See how it works",
        "gif": GIF_2,
        "gif_alt": "AI optimization preview",
    },
]


class FeaturesChess:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            # Section header
            with Flex(direction="col", align="center", gap=4).className("text-center mb-16"):
                Text("Capabilities").className(
                    "liquid-glass rounded-full px-3.5 py-1 "
                    "text-xs font-medium text-white font-body "
                    "inline-block"
                )
                Text("Pro features. Zero complexity.").className(
                    "font-heading text-white tracking-tight "
                    "leading-none text-4xl md:text-5xl lg:text-6xl"
                )

            # Alternating rows
            for row in ROWS:
                direction = "row-reverse" if row["reverse"] else "row"
                with Flex(direction="row", align="center", gap=16).className(
                    f"flex-col md:flex-{direction} mb-24 gap-8 md:gap-16"
                ):
                    # Text side
                    with Flex(direction="col", align="start", gap=6).className("flex-1"):
                        Text(row["title"]).className(
                            "font-heading text-white tracking-tight "
                            "leading-tight text-3xl md:text-4xl"
                        )
                        Text(row["body"]).className(
                            "text-white/60 font-body font-light "
                            "text-sm md:text-base leading-relaxed"
                        ).paragraph()

                        with Flex(direction="row", align="center", gap=2).className(
                            "liquid-glass-strong rounded-full "
                            "px-5 py-2.5 cursor-pointer inline-flex"
                        ):
                            Text(row["cta"]).className("text-white text-sm font-body font-medium")
                            Text("↗").className("text-white text-sm")

                    # GIF side
                    with Flex().className("flex-1 liquid-glass rounded-2xl overflow-hidden"):
                        Image(
                            src=row["gif"],
                            alt=row["gif_alt"],
                        ).className("w-full h-auto")
