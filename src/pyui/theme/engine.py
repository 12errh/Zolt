"""
Theme engine — build, validate, and export PyUI themes.

Public API::

    from pyui.theme.engine import build_theme, tokens_to_css_vars, tokens_to_figma

    theme = build_theme("dark")
    theme = build_theme({"color.primary": "#FF0000"})
    css   = tokens_to_css_vars(theme)
    figma = tokens_to_figma(theme)
"""

from __future__ import annotations

import json
from typing import Any

from pyui.exceptions import UnknownThemeError
from pyui.theme.tokens import BUILT_IN_THEMES, DEFAULT_TOKENS


def build_theme(theme: str | dict[str, str]) -> dict[str, str]:
    """
    Merge *theme* overrides on top of :data:`~pyui.theme.tokens.DEFAULT_TOKENS`.

    Parameters
    ----------
    theme : str | dict[str, str]
        A built-in theme name (``"light"``, ``"dark"``, ``"ocean"``,
        ``"sunset"``, ``"forest"``, ``"rose"``) **or** a dict of token
        overrides.  Any key not present in the override dict is inherited
        from ``DEFAULT_TOKENS``.

    Returns
    -------
    dict[str, str]
        Fully-resolved flat token dict.

    Raises
    ------
    ThemeError
        If *theme* is a string that is not a known built-in theme name.
    """
    base = dict(DEFAULT_TOKENS)

    if isinstance(theme, str):
        if theme not in BUILT_IN_THEMES:
            known = ", ".join(f'"{k}"' for k in BUILT_IN_THEMES)
            raise UnknownThemeError(
                f"Unknown theme {theme!r}. "
                f"Built-in themes are: {known}. "
                "Pass a dict of token overrides for a custom theme."
            )
        base.update(BUILT_IN_THEMES[theme])
    else:
        # Validate keys — warn on unknown tokens but don't hard-fail
        unknown = [k for k in theme if k not in DEFAULT_TOKENS]
        if unknown:
            import warnings

            warnings.warn(
                f"Unknown theme token(s): {unknown}. "
                "These will be included but may have no effect.",
                stacklevel=2,
            )
        base.update(theme)

    return base


def tokens_to_css_vars(tokens: dict[str, str]) -> str:
    """
    Render a token dict as a CSS ``:root`` block with ``--pyui-*`` variables,
    plus concrete CSS overrides so Tailwind-hardcoded classes pick up the theme.
    """
    lines = [":root {"]
    for key, value in tokens.items():
        css_name = "--pyui-" + key.replace(".", "-")
        lines.append(f"  {css_name}: {value};")
    lines.append("}")

    # ── Concrete overrides ────────────────────────────────────────────────────
    # Components use hardcoded Tailwind classes. We override the key ones so
    # the theme colours actually show up without touching component code.
    bg = tokens.get("color.background", "#FFFFFF")
    surf = tokens.get("color.surface", "#F9FAFB")
    text = tokens.get("color.text", "#111827")
    muted = tokens.get("color.text.muted", "#6B7280")
    bord = tokens.get("color.border", "#E5E7EB")
    prim = tokens.get("color.primary", "#6C63FF")
    prim_h = tokens.get("color.primary.hover", "#5A52E0")
    sec = tokens.get("color.secondary", "#F3F4F6")

    # Determine if this is a dark theme (dark background)
    is_dark = _is_dark_color(bg)

    overrides = f"""
/* PyUI theme overrides — applied over Tailwind defaults */
body {{
  background-color: {bg} !important;
  color: {text} !important;
}}
/* Surface / card backgrounds */
.bg-white, [class*="bg-white"] {{
  background-color: {surf} !important;
}}
/* Gray-50 / gray-100 surfaces */
.bg-gray-50 {{ background-color: {_blend(bg, surf, 0.5)} !important; }}
.bg-gray-100 {{ background-color: {sec} !important; }}
.bg-gray-900 {{ background-color: {_darken(bg, 0.15) if not is_dark else _lighten(bg, 0.08)} !important; }}
.bg-gray-950 {{ background-color: {prim} !important; }}
/* Text colours */
.text-gray-900, .text-gray-950 {{ color: {text} !important; }}
.text-gray-800 {{ color: {text} !important; }}
.text-gray-700 {{ color: {muted} !important; }}
.text-gray-600, .text-gray-500, .text-gray-400 {{ color: {muted} !important; }}
/* Borders */
.border-gray-100, .border-gray-200 {{ border-color: {bord} !important; }}
.border-gray-300 {{ border-color: {bord} !important; }}
/* Primary action colour (buttons, accents) */
.bg-gray-800:not([class*="hover"]) {{ background-color: {prim_h} !important; }}
/* Page wrapper */
#pyui-app {{ background-color: {bg}; }}
/* Sidebar / nav */
.bg-\\[\\#f7f7f8\\] {{ background-color: {_blend(bg, surf, 0.3)} !important; }}
"""
    return "\n".join(lines) + overrides


def _is_dark_color(hex_color: str) -> bool:
    """Return True if the hex colour is perceptually dark."""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        # Perceived luminance
        return (0.299 * r + 0.587 * g + 0.114 * b) < 128
    except Exception:
        return False


def _darken(hex_color: str, amount: float) -> str:
    """Darken a hex colour by *amount* (0–1)."""
    try:
        h = hex_color.lstrip("#")
        r = max(0, int(int(h[0:2], 16) * (1 - amount)))
        g = max(0, int(int(h[2:4], 16) * (1 - amount)))
        b = max(0, int(int(h[4:6], 16) * (1 - amount)))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _lighten(hex_color: str, amount: float) -> str:
    """Lighten a hex colour by *amount* (0–1)."""
    try:
        h = hex_color.lstrip("#")
        r = min(255, int(int(h[0:2], 16) + (255 - int(h[0:2], 16)) * amount))
        g = min(255, int(int(h[2:4], 16) + (255 - int(h[2:4], 16)) * amount))
        b = min(255, int(int(h[4:6], 16) + (255 - int(h[4:6], 16)) * amount))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _blend(c1: str, c2: str, t: float) -> str:
    """Linear blend between two hex colours at ratio *t* (0=c1, 1=c2)."""
    try:
        h1, h2 = c1.lstrip("#"), c2.lstrip("#")
        r = int(int(h1[0:2], 16) * (1 - t) + int(h2[0:2], 16) * t)
        g = int(int(h1[2:4], 16) * (1 - t) + int(h2[2:4], 16) * t)
        b = int(int(h1[4:6], 16) * (1 - t) + int(h2[4:6], 16) * t)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return c1


def tokens_to_figma(tokens: dict[str, str]) -> str:
    """
    Export a token dict as a Figma-compatible design tokens JSON string.

    Follows the W3C Design Tokens Community Group format so the output
    can be imported directly into Figma via the Tokens Studio plugin.

    Parameters
    ----------
    tokens : dict[str, str]
        Flat token dict (output of :func:`build_theme`).

    Returns
    -------
    str
        JSON string.
    """
    # Group tokens by their top-level namespace (color, font, space, …)
    groups: dict[str, Any] = {}
    for key, value in tokens.items():
        parts = key.split(".", 1)
        group = parts[0]
        rest = parts[1] if len(parts) > 1 else key
        if group not in groups:
            groups[group] = {}
        # Nested keys use dot notation → nested dicts
        _set_nested(
            groups[group], rest.split("."), {"$value": value, "$type": _infer_type(key, value)}
        )

    return json.dumps(groups, indent=2)


def _set_nested(d: dict[str, Any], keys: list[str], value: Any) -> None:
    """Recursively set a nested dict value from a list of keys."""
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def _infer_type(key: str, value: str) -> str:
    """Infer the W3C design token type from the key/value."""
    if key.startswith("color."):
        return "color"
    if key.startswith("font.size") or key.startswith("space.") or key.endswith("px"):
        return "dimension"
    if key.startswith("font.family"):
        return "fontFamily"
    if key.startswith("font.weight"):
        return "fontWeight"
    if key.startswith("shadow."):
        return "shadow"
    if key.startswith("radius."):
        return "borderRadius"
    if key.startswith("transition."):
        return "duration"
    return "other"


# ── Dark-mode auto-detection helper ──────────────────────────────────────────

_DARK_MODE_JS = """\
<script>
  (function() {
    var stored = localStorage.getItem('pyui-theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // If a theme is stored, load it immediately
    if (stored) {
      document.documentElement.classList.toggle('dark', stored === 'dark');
      // Fetch and apply the stored theme CSS vars
      fetch('/pyui-api/theme/' + stored, { method: 'POST' })
        .then(function(r) { return r.json(); })
        .then(function(d) {
          var style = document.getElementById('pyui-theme-vars');
          if (style) style.textContent = d.css;
        })
        .catch(function(e) {
          console.warn('[PyUI] Failed to load stored theme:', e);
        });
    } else if (prefersDark) {
      document.documentElement.classList.add('dark');
    }

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      if (!localStorage.getItem('pyui-theme')) {
        document.documentElement.classList.toggle('dark', e.matches);
      }
    });
  })();
</script>"""


def dark_mode_script() -> str:
    """Return the inline JS snippet that handles dark-mode auto-detection."""
    return _DARK_MODE_JS


# ── Runtime theme hot-swap ────────────────────────────────────────────────────

_THEME_SWAP_JS = """\
<script>
  function pyuiSetTheme(name) {
    localStorage.setItem('pyui-theme', name);
    fetch('/pyui-api/theme/' + name, { method: 'POST' })
      .then(function(r) { return r.json(); })
      .then(function(d) {
        // Reload so the server re-renders the page with the new theme tokens
        window.location.reload();
      });
  }
</script>"""


def theme_swap_script() -> str:
    """Return the JS helper that calls the theme-swap API endpoint."""
    return _THEME_SWAP_JS
