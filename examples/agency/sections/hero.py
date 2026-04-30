"""Hero — pure Zolt, no RawHTML."""

from pyui import (
    BlurHeading,
    Flex,
    Link,
    Section,
    Text,
    VideoBg,
)

HERO_VIDEO = (
    "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/"
    "hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4"
)
PARTNERS = ["Stripe", "Vercel", "Linear", "Notion", "Figma"]


class HeroSection:
    def compose(self) -> None:
        with Section(min_height=700, bg="#000").className("h-screen"):
            # Background video
            VideoBg(
                src=HERO_VIDEO,
                hls=False,
                fade_height=300,
                poster="/images/hero_bg.jpeg",
            )

            # Dark overlay for text readability
            Flex().className("absolute inset-0 bg-black/30")

            # ── Content — centered, pushed below navbar ───────────────────
            with (
                Flex(direction="col", align="center", justify="start", gap=0)
                .className("absolute inset-0 text-center px-6")
                .inlineStyle("padding-top:clamp(6rem,14vh,10rem);z-index:10;")
            ):
                # Badge — white text on glass, always visible
                with Flex(direction="row", align="center", gap=2).className(
                    "liquid-glass rounded-full px-1 py-1 inline-flex mb-7"
                ):
                    Text("New").className(
                        "bg-white text-black rounded-full px-3 py-1 text-xs font-semibold font-body"
                    )
                    Text("Introducing AI-powered web design.").className(
                        "text-white text-sm font-body font-medium pr-3"
                    ).inlineStyle("text-shadow:0 1px 4px rgba(0,0,0,0.6);")

                # Animated headline
                BlurHeading(
                    "The Website Your Brand Deserves",
                    level=1,
                    delay_ms=100,
                ).className("text-white max-w-3xl mx-auto mb-6")

                # Subtext
                Text(
                    "Stunning design. Blazing performance. "
                    "Built by AI, refined by experts. "
                    "This is web design, wildly reimagined."
                ).className(
                    "blur-in blur-in-delay-1 font-body font-light "
                    "text-base leading-relaxed max-w-md mx-auto mb-8"
                ).inlineStyle(
                    "color:rgba(255,255,255,0.9);text-shadow:0 1px 6px rgba(0,0,0,0.7);"
                ).paragraph()

                # CTA buttons
                with Flex(direction="row", align="center", justify="center", gap=4).className(
                    "blur-in blur-in-delay-2"
                ):
                    Link("Get Started", href="#").style("glass").icon("arrow-up-right")
                    Link("Watch the Film", href="#").style("nav").icon("play", position="left")

            # ── Partners bar — absolute bottom ────────────────────────────
            with (
                Flex(direction="col", align="center", gap=5)
                .className("absolute bottom-0 left-0 right-0 text-center pb-10")
                .inlineStyle("z-index:10;")
            ):
                Text("Trusted by the teams behind").className(
                    "liquid-glass rounded-full px-3.5 py-1 "
                    "text-xs font-medium font-body inline-block"
                ).inlineStyle("color:rgba(255,255,255,0.7);")

                with Flex(
                    direction="row", align="center", justify="center", gap=0, wrap=True
                ).className("gap-x-12 md:gap-x-16"):
                    for partner in PARTNERS:
                        Text(partner).className("font-heading text-white text-2xl md:text-3xl")
