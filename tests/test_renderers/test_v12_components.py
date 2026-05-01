"""
Unit tests for v1.2 components:
  BlurHeading, Link, Section, VideoBg, FloatingNav
"""

from __future__ import annotations

import pytest

from pyui.renderers.web.generator import render_component

# ── BlurHeading ───────────────────────────────────────────────────────────────


class TestBlurHeading:
    def test_renders_h1_by_default(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("Hello World"))
        assert "<h1" in html
        assert "</h1>" in html

    def test_renders_correct_level(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        for level in range(1, 7):
            html = render_component(BlurHeading("Test", level=level))
            assert f"<h{level}" in html

    def test_splits_words_into_spans(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("The Website Deserves"))
        assert html.count("<span") == 3
        assert "The" in html
        assert "Website" in html
        assert "Deserves" in html

    def test_animation_delay_applied(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("A B C", delay_ms=150))
        assert "animation-delay:0ms" in html
        assert "animation-delay:150ms" in html
        assert "animation-delay:300ms" in html

    def test_always_has_font_heading_class(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("Test"))
        assert "font-heading" in html
        assert "word-reveal" in html

    def test_fluid_font_size_on_h1(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("Test", level=1))
        assert "clamp(3rem" in html

    def test_fluid_font_size_on_h2(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("Test", level=2))
        assert "clamp(2.25rem" in html

    def test_classname_not_duplicated(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        html = render_component(BlurHeading("Test").className("my-class"))
        # class_name injected once by post-processor — not duplicated
        assert html.count("my-class") == 1

    def test_invalid_level_raises(self) -> None:
        from pyui.components.display.blur_heading import BlurHeading

        with pytest.raises(ValueError):
            BlurHeading("Test", level=0)
        with pytest.raises(ValueError):
            BlurHeading("Test", level=7)


# ── Link ──────────────────────────────────────────────────────────────────────


class TestLink:
    def test_renders_anchor_tag(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Click me", href="/about"))
        assert "<a " in html
        assert 'href="/about"' in html
        assert "Click me" in html

    def test_default_href_is_hash(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Home"))
        assert 'href="#"' in html

    def test_external_adds_target_blank(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Ext", href="https://example.com", external=True))
        assert 'target="_blank"' in html
        assert 'rel="noopener noreferrer"' in html

    def test_internal_no_target_blank(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Int", href="/page"))
        assert "target" not in html

    def test_glass_variant(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Go").style("glass"))
        assert "liquid-glass-strong" in html

    def test_primary_variant_white_bg(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Go").style("primary"))
        assert "bg-white" in html
        assert "text-black" in html

    def test_footer_variant(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Privacy").style("footer"))
        assert "text-white/40" in html

    def test_icon_right_appended(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Go").style("glass").icon("arrow-up-right"))
        assert "arrow-up-right" in html
        # Icon appears after text
        assert html.index("Go") < html.index("arrow-up-right")

    def test_icon_left_prepended(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("Play").icon("play", position="left"))
        assert html.index("play") < html.index("Play")

    def test_text_escaped(self) -> None:
        from pyui.components.display.link import Link

        html = render_component(Link("<script>", href="#"))
        assert "<script>" not in html
        assert "&lt;script&gt;" in html


# ── Section ───────────────────────────────────────────────────────────────────


class TestSection:
    def test_renders_section_tag(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section())
        assert "<section" in html
        assert "</section>" in html

    def test_min_height_in_style(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section(min_height=560))
        assert "min-height:560px" in html

    def test_background_color_in_style(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section(bg="#000"))
        assert "background:#000" in html

    def test_position_relative_always_set(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section())
        assert "position:relative" in html

    def test_overflow_hidden_always_set(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section())
        assert "overflow:hidden" in html

    def test_inline_style_merged(self) -> None:
        from pyui.components.layout.section import Section

        html = render_component(Section().inlineStyle("z-index:10;"))
        assert "z-index:10" in html

    def test_children_rendered(self) -> None:
        from pyui import Text
        from pyui.components.layout.section import Section

        with Section() as s:
            Text("Inside section")
        html = render_component(s)
        assert "Inside section" in html


# ── VideoBg ───────────────────────────────────────────────────────────────────


class TestVideoBg:
    def test_renders_video_tag(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="https://example.com/video.mp4"))
        assert "<video" in html

    def test_mp4_source_tag(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="https://example.com/video.mp4", hls=False))
        assert "video.mp4" in html
        assert "<source" in html

    def test_hls_injects_script(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="https://stream.mux.com/test.m3u8", hls=True))
        assert "Hls.isSupported" in html
        assert "loadSource" in html
        assert "<source" not in html  # HLS uses JS, not <source>

    def test_desaturate_filter(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4", desaturate=True))
        assert "saturate(0)" in html

    def test_no_desaturate_by_default(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4"))
        assert "saturate(0)" not in html

    def test_fade_height_gradient(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4", fade_height=160))
        assert "height:160px" in html
        assert "linear-gradient" in html

    def test_zero_fade_no_gradient(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4", fade_height=0))
        assert "linear-gradient" not in html

    def test_poster_attribute(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4", poster="/images/poster.jpg"))
        assert 'poster="/images/poster.jpg"' in html

    def test_object_fit_cover(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4"))
        assert "object-fit:cover" in html

    def test_position_absolute(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4"))
        assert "position:absolute" in html

    def test_autoplay_loop_muted(self) -> None:
        from pyui.components.media.video_bg import VideoBg

        html = render_component(VideoBg(src="test.mp4"))
        assert "autoplay" in html
        assert "loop" in html
        assert "muted" in html


# ── FloatingNav ───────────────────────────────────────────────────────────────


class TestFloatingNav:
    def test_renders_nav_tag(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav())
        assert "<nav" in html
        assert "</nav>" in html

    def test_position_fixed(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav())
        assert "position:fixed" in html

    def test_logo_image_rendered(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(logo_src="/images/logo.png", logo_alt="Studio"))
        assert "<img" in html
        assert "/images/logo.png" in html
        assert 'alt="Studio"' in html

    def test_no_logo_when_not_set(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(logo_src=None))
        assert "<img" not in html

    def test_links_rendered(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(links=["Home", "About", "Contact"]))
        assert "Home" in html
        assert "About" in html
        assert "Contact" in html

    def test_links_as_tuples(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(links=[("Home", "/"), ("About", "/about")]))
        assert 'href="/"' in html
        assert 'href="/about"' in html

    def test_cta_button_rendered(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(cta_text="Get Started", cta_href="#cta"))
        assert "Get Started" in html
        assert 'href="#cta"' in html

    def test_no_cta_when_none(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(cta_text=None))
        # No CTA button — just nav links
        assert "bg-white" not in html

    def test_liquid_glass_pill(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(links=["Home"]))
        assert "liquid-glass" in html

    def test_cta_has_arrow_icon(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(cta_text="Go"))
        assert "arrow-up-right" in html

    def test_link_text_escaped(self) -> None:
        from pyui.components.navigation.floating_nav import FloatingNav

        html = render_component(FloatingNav(links=["<script>"]))
        assert "<script>" not in html
        assert "&lt;script&gt;" in html
