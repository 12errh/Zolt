"""Phase 5 — Theme engine tests."""

from __future__ import annotations

import pytest


def test_default_tokens_complete() -> None:
    from pyui.theme.tokens import DEFAULT_TOKENS

    required = [
        "color.primary",
        "color.background",
        "font.family",
        "space.4",
        "radius.md",
        "shadow.sm",
    ]
    for key in required:
        assert key in DEFAULT_TOKENS, f"Missing token: {key}"


def test_build_theme_light_returns_defaults() -> None:
    from pyui.theme.engine import build_theme
    from pyui.theme.tokens import DEFAULT_TOKENS

    theme = build_theme("light")
    assert theme["color.primary"] == DEFAULT_TOKENS["color.primary"]
    assert theme["color.background"] == DEFAULT_TOKENS["color.background"]


def test_build_theme_merges_with_defaults() -> None:
    from pyui.theme.engine import build_theme

    custom = {"color.primary": "#FF0000"}
    theme = build_theme(custom)
    assert theme["color.primary"] == "#FF0000"
    assert "color.background" in theme  # inherited from defaults


def test_build_theme_dark_has_dark_background() -> None:
    from pyui.theme.engine import build_theme

    theme = build_theme("dark")
    bg = theme["color.background"]
    r = int(bg[1:3], 16)
    assert r < 50  # very dark


def test_build_theme_all_builtins() -> None:
    from pyui.theme.engine import build_theme

    for name in ("light", "dark", "ocean", "sunset", "forest", "rose"):
        theme = build_theme(name)
        assert "color.primary" in theme
        assert "color.background" in theme


def test_build_theme_invalid_name_raises() -> None:
    from pyui.exceptions import ThemeError
    from pyui.theme.engine import build_theme

    with pytest.raises(ThemeError, match="Unknown theme"):
        build_theme("nonexistent-theme-xyz")


def test_build_theme_custom_dict_overrides() -> None:
    from pyui.theme.engine import build_theme

    theme = build_theme({"color.primary": "#ABCDEF", "radius.md": "99px"})
    assert theme["color.primary"] == "#ABCDEF"
    assert theme["radius.md"] == "99px"
    assert "font.family" in theme  # still has defaults


def test_tokens_to_css_vars_format() -> None:
    from pyui.theme.engine import build_theme, tokens_to_css_vars

    theme = build_theme("light")
    css = tokens_to_css_vars(theme)
    assert ":root {" in css
    assert "--pyui-color-primary" in css
    assert "--pyui-font-family" in css
    assert css.strip().endswith("}")


def test_tokens_to_css_vars_uses_pyui_prefix() -> None:
    from pyui.theme.engine import tokens_to_css_vars

    css = tokens_to_css_vars({"color.primary": "#123456"})
    assert "--pyui-color-primary: #123456;" in css


def test_tokens_to_figma_returns_json() -> None:
    import json

    from pyui.theme.engine import build_theme, tokens_to_figma

    theme = build_theme("light")
    figma_json = tokens_to_figma(theme)
    data = json.loads(figma_json)
    assert "color" in data
    assert "font" in data


def test_tokens_to_figma_color_type() -> None:
    import json

    from pyui.theme.engine import tokens_to_figma

    figma_json = tokens_to_figma({"color.primary": "#6C63FF"})
    data = json.loads(figma_json)
    assert data["color"]["primary"]["$type"] == "color"
    assert data["color"]["primary"]["$value"] == "#6C63FF"


def test_dark_mode_script_returns_string() -> None:
    from pyui.theme.engine import dark_mode_script

    script = dark_mode_script()
    assert "<script>" in script
    assert "prefers-color-scheme" in script
    assert "pyui-theme" in script


def test_theme_swap_script_returns_string() -> None:
    from pyui.theme.engine import theme_swap_script

    script = theme_swap_script()
    assert "pyuiSetTheme" in script
    assert "/pyui-api/theme/" in script


def test_build_theme_unknown_key_warns() -> None:
    import warnings

    from pyui.theme.engine import build_theme

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        theme = build_theme({"totally.unknown.key": "value"})
        assert len(w) == 1
        assert "Unknown theme token" in str(w[0].message)
    assert theme["totally.unknown.key"] == "value"


def test_web_renderer_uses_engine() -> None:
    """render_page must produce CSS vars from the theme engine."""
    from pyui import Page
    from pyui.renderers.web import render_page

    html = render_page(Page(title="T", route="/"))
    assert "--pyui-color-primary" in html


def test_dark_mode_script_in_rendered_page() -> None:
    """Rendered page must include the dark-mode detection script."""
    from pyui import Page
    from pyui.renderers.web import render_page

    html = render_page(Page(title="T", route="/"))
    assert "prefers-color-scheme" in html
