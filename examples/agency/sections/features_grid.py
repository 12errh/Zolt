"""FeaturesGrid — 4-column 'Why Us' cards."""

from pyui import Flex, Grid, Icon, Text

CARDS = [
    {
        "icon": "zap",
        "title": "Days, Not Months",
        "body": (
            "Concept to launch at a pace that redefines fast. Because waiting isn't a strategy."
        ),
    },
    {
        "icon": "palette",
        "title": "Obsessively Crafted",
        "body": (
            "Every detail considered. Every element refined. "
            "Design so precise, it feels inevitable."
        ),
    },
    {
        "icon": "bar-chart-3",
        "title": "Built to Convert",
        "body": (
            "Layouts informed by data. Decisions backed by performance. Results you can measure."
        ),
    },
    {
        "icon": "shield",
        "title": "Secure by Default",
        "body": (
            "Enterprise-grade protection comes standard. "
            "SSL, DDoS mitigation, compliance. All included."
        ),
    },
]


class FeaturesGrid:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            # Section header
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("Why Us").className(
                    "liquid-glass rounded-full px-3.5 py-1 "
                    "text-xs font-medium text-white font-body "
                    "inline-block"
                )
                Text("The difference is everything.").className(
                    "font-heading text-white tracking-tight "
                    "leading-none text-4xl md:text-5xl lg:text-6xl"
                )

            # 4-column grid
            with Grid(cols=4, gap=6).className("grid-cols-1 md:grid-cols-2 lg:grid-cols-4"):
                for card in CARDS:
                    with Flex(direction="col", align="start", gap=4).className(
                        "liquid-glass rounded-2xl p-6"
                    ):
                        # Icon circle
                        with Flex(align="center", justify="center").className(
                            "liquid-glass-strong rounded-full w-10 h-10"
                        ):
                            Icon(card["icon"]).className("text-white w-5 h-5")

                        Text(card["title"]).className("text-white font-body font-medium text-base")
                        Text(card["body"]).className(
                            "text-white/60 font-body font-light text-sm leading-relaxed"
                        ).paragraph()
