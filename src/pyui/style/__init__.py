"""
ZoltCSS — Zolt's native styling engine.

This module replaces Tailwind CSS with a pure Python styling system.
All visual properties are expressed as Python methods; ZoltCSS compiles
them to optimized CSS at build time.

Zero external dependencies. Zero CDN. Zero CSS knowledge required.
"""

from __future__ import annotations

from pyui.style.tokens import TOKENS, DARK_TOKENS, BUILT_IN_THEMES
from pyui.style.rules import StyleRule, token
from pyui.style.resolver import StyleResolver
from pyui.style.css_generator import ZoltCSSGenerator
from pyui.style.qt_generator import QtStyleGenerator
from pyui.style.rich_generator import RichStyleGenerator
from pyui.style.theme import Theme, ThemeManager

__all__ = [
    # Tokens
    "TOKENS",
    "DARK_TOKENS",
    "BUILT_IN_THEMES",
    # Rules
    "StyleRule",
    "token",
    # Resolver
    "StyleResolver",
    # Generators
    "ZoltCSSGenerator",
    "QtStyleGenerator",
    "RichStyleGenerator",
    # Theme
    "Theme",
    "ThemeManager",
]