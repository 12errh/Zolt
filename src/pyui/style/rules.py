"""
ZoltCSS Style Rules — The building blocks of the styling system.

StyleRule dataclass and helper functions for creating style declarations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StyleRule:
    """
    A single style rule declaration.
    
    Represents one CSS property:value pair with optional modifiers
    for responsive breakpoints, dark mode, and component states.
    
    Example:
        StyleRule(
            property="background-color",
            value="var(--color-primary)",
            breakpoint="md",  # only applies on medium screens and up
            dark_mode="var(--color-primary-hover)",  # different value in dark mode
            state="hover",  # only applies on hover
        )
    """
    
    property: str  # CSS property name (e.g., "background-color")
    value: str  # CSS value (e.g., "var(--color-primary)" or "#6C63FF")
    
    # Modifiers
    breakpoint: str | None = None  # "sm", "md", "lg", "xl", "2xl"
    dark_mode: str | None = None  # Alternative value for dark mode
    state: str | None = None  # "hover", "active", "focus", "disabled"
    
    # Metadata
    component: str | None = None  # Which component this rule belongs to
    variant: str | None = None  # Component variant (e.g., "primary", "ghost")
    
    def __hash__(self) -> int:
        """Make StyleRule hashable for deduplication."""
        return hash((
            self.property,
            self.value,
            self.breakpoint,
            self.dark_mode,
            self.state,
            self.component,
            self.variant,
        ))
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on all fields."""
        if not isinstance(other, StyleRule):
            return False
        return (
            self.property == other.property
            and self.value == other.value
            and self.breakpoint == other.breakpoint
            and self.dark_mode == other.dark_mode
            and self.state == other.state
            and self.component == other.component
            and self.variant == other.variant
        )
    
    def to_css_declaration(self) -> str:
        """Convert to CSS property: value string."""
        return f"{self.property}: {self.value};"
    
    def has_modifier(self) -> bool:
        """Check if this rule has any modifiers (breakpoint, dark_mode, or state)."""
        return bool(self.breakpoint or self.dark_mode or self.state)


def token(token_name: str) -> str:
    """
    Helper to reference a token value using CSS custom properties.
    
    Converts a token name like "color-primary" to "var(--color-primary)".
    
    Args:
        token_name: The token key from TOKENS dict
        
    Returns:
        CSS var() reference string
        
    Example:
        >>> token("color-primary")
        'var(--color-primary)'
        >>> token("space-4")
        'var(--space-4)'
    """
    return f"var(--{token_name})"


def rgb_from_hex(hex_color: str, alpha: float = 1.0) -> str:
    """
    Convert hex color to RGB(A) format.
    
    Useful for creating semi-transparent versions of colors.
    
    Args:
        hex_color: Hex color string (e.g., "#6C63FF")
        alpha: Alpha value from 0.0 to 1.0
        
    Returns:
        RGB or RGBA string
        
    Example:
        >>> rgb_from_hex("#6C63FF", 0.1)
        'rgba(108, 99, 255, 0.1)'
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    if alpha < 1.0:
        return f"rgba({r}, {g}, {b}, {alpha})"
    return f"rgb({r}, {g}, {b})"


# ── Pre-built Style Rule Collections ──────────────────────────────────────────


def create_base_rules(component: str, rules: list[tuple[str, str]]) -> list[StyleRule]:
    """
    Create a list of base style rules for a component.
    
    Args:
        component: Component name
        rules: List of (property, value) tuples
        
    Returns:
        List of StyleRule objects
    """
    return [
        StyleRule(property=prop, value=value, component=component)
        for prop, value in rules
    ]


def create_state_rules(
    component: str,
    state: str,
    rules: list[tuple[str, str]],
    variant: str | None = None,
) -> list[StyleRule]:
    """
    Create style rules that apply only in a specific state (hover, active, etc.).
    
    Args:
        component: Component name
        state: State name ("hover", "active", "focus", "disabled")
        rules: List of (property, value) tuples
        variant: Optional component variant
        
    Returns:
        List of StyleRule objects with state modifier
    """
    return [
        StyleRule(
            property=prop,
            value=value,
            component=component,
            state=state,
            variant=variant,
        )
        for prop, value in rules
    ]


def create_responsive_rules(
    component: str,
    breakpoint: str,
    rules: list[tuple[str, str]],
    variant: str | None = None,
) -> list[StyleRule]:
    """
    Create style rules that apply only at a specific breakpoint.
    
    Args:
        component: Component name
        breakpoint: Breakpoint name ("sm", "md", "lg", "xl", "2xl")
        rules: List of (property, value) tuples
        variant: Optional component variant
        
    Returns:
        List of StyleRule objects with breakpoint modifier
    """
    return [
        StyleRule(
            property=prop,
            value=value,
            component=component,
            breakpoint=breakpoint,
            variant=variant,
        )
        for prop, value in rules
    ]
