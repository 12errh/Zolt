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

from pyui.exceptions import ThemeError
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
            raise ThemeError(
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
    Render a token dict as a CSS ``:root`` block with ``--pyui-*`` variables.

    Parameters
    ----------
    tokens : dict[str, str]
        Flat token dict (output of :func:`build_theme`).

    Returns
    -------
    str
        CSS string, e.g.::

            :root {
              --pyui-color-primary: #6C63FF;
              --pyui-font-family: Inter, system-ui, sans-serif;
              ...
            }
    """
    lines = [":root {"]
    for key, value in tokens.items():
        css_name = "--pyui-" + key.replace(".", "-")
        lines.append(f"  {css_name}: {value};")
    lines.append("}")
    return "\n".join(lines)


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
    if (stored === 'dark' || (!stored && prefersDark)) {
      document.documentElement.classList.add('dark');
    }
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
  function pyuiSetTheme(name) {{
    localStorage.setItem('pyui-theme', name);
    fetch('/pyui-api/theme/' + name, {{ method: 'POST' }})
      .then(r => r.json())
      .then(d => {{
        var style = document.getElementById('pyui-theme-vars');
        if (style) style.textContent = d.css;
        document.documentElement.classList.toggle('dark', name === 'dark');
      }});
  }}
</script>"""


def theme_swap_script() -> str:
    """Return the JS helper that calls the theme-swap API endpoint."""
    return _THEME_SWAP_JS
