"""
Rich Style Generator — Converts StyleRules to Rich Terminal Styles.

Generates Rich library Style objects for CLI rendering from ZoltCSS StyleRules.
"""

from __future__ import annotations

from typing import Any

from pyui.style.rules import StyleRule
from pyui.style.tokens import TOKENS, BUILT_IN_THEMES


class RichStyleGenerator:
    """
    Generates Rich terminal styles from StyleRule collections.
    
    Maps CSS properties to Rich Style attributes for CLI rendering.
    """
    
    # Color name mapping (hex to Rich color names)
    HEX_TO_RICH_COLOR = {
        "#000000": "black",
        "#808080": "grey",
        "#C0C0C0": "white",
        "#FF0000": "red",
        "#00FF00": "green",
        "#0000FF": "blue",
        "#FFFF00": "yellow",
        "#00FFFF": "cyan",
        "#FF00FF": "magenta",
        "#FFFFFF": "white",
        "#111827": "grey93",
        "#6B7280": "grey50",
        "#9CA3AF": "grey60",
        "#EF4444": "red",
        "#10B981": "green",
        "#F59E0B": "yellow",
        "#3B82F6": "blue",
        "#6C63FF": "deep_pink3",
        "#F3F4F6": "grey94",
        "#E5E7EB": "grey80",
        "#D1D5DB": "grey70",
    }
    
    def __init__(self):
        self._rules: list[StyleRule] = []
        self._component_rules: dict[str, list[StyleRule]] = {}
    
    def register_rule(self, component: str, rule: StyleRule) -> None:
        """
        Register a style rule for a component.
        
        Args:
            component: Component name
            rule: StyleRule object
        """
        if component not in self._component_rules:
            self._component_rules[component] = []
        self._component_rules[component].append(rule)
        self._rules.append(rule)
    
    def _hex_to_rich_color(self, hex_color: str) -> str:
        """
        Convert hex color to Rich color name.
        
        Falls back to the hex value if no mapping exists.
        """
        return self.HEX_TO_RICH_COLOR.get(hex_color, hex_color)
    
    def _resolve_token(self, token_ref: str) -> str:
        """
        Resolve a token reference to its value.
        
        Args:
            token_ref: Token reference like "var(--color-primary)"
            
        Returns:
            Resolved value
        """
        if token_ref.startswith("var(--"):
            token_name = token_ref[6:-1]
            return TOKENS.get(token_name, token_ref)
        return token_ref
    
    def generate_style(
        self,
        component: str,
        state: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate Rich Style kwargs for a component.
        
        Args:
            component: Component name
            state: Optional state ("hover", "disabled", etc.)
            
        Returns:
            Dict of Rich Style constructor kwargs
        """
        rules = self._component_rules.get(component, [])
        
        # Filter by state
        if state:
            rules = [r for r in rules if r.state == state]
        else:
            rules = [r for r in rules if r.state is None]
        
        style_kwargs: dict[str, Any] = {}
        
        for rule in rules:
            value = self._resolve_token(rule.value)
            
            if rule.property == "color":
                style_kwargs["color"] = self._hex_to_rich_color(value)
            
            elif rule.property == "background-color":
                style_kwargs["bgcolor"] = self._hex_to_rich_color(value)
            
            elif rule.property == "font-weight":
                if value in ["700", "800", "900", "bold"]:
                    style_kwargs["bold"] = True
                elif value in ["400", "normal"]:
                    style_kwargs["bold"] = False
            
            elif rule.property == "text-decoration":
                if value == "underline":
                    style_kwargs["underline"] = True
                elif value == "none":
                    style_kwargs["underline"] = False
            
            elif rule.property == "font-style":
                if value == "italic":
                    style_kwargs["italic"] = True
            
            elif rule.property == "opacity":
                # Rich doesn't support opacity directly
                pass
        
        return style_kwargs
    
    def get_component_classes(self, component: str) -> list[str]:
        """
        Get all registered classes/variants for a component.
        
        Args:
            component: Component name
            
        Returns:
            List of variant/state names
        """
        rules = self._component_rules.get(component, [])
        variants = set()
        
        for rule in rules:
            if rule.variant:
                variants.add(rule.variant)
            if rule.state:
                variants.add(rule.state)
        
        return sorted(variants)
    
    def reset(self) -> None:
        """Clear all registered rules."""
        self._rules.clear()
        self._component_rules.clear()
    
    @property
    def rule_count(self) -> int:
        """Get number of registered rules."""
        return len(self._rules)


def create_terminal_style(style_kwargs: dict[str, Any]) -> str:
    """
    Create a Rich Style markup string from kwargs.
    
    This is a helper for creating inline Rich markup.
    
    Args:
        style_kwargs: Style constructor kwargs
        
    Returns:
        Rich markup string (e.g., "[bold red on blue]")
    """
    parts = []
    
    if style_kwargs.get("bold"):
        parts.append("bold")
    if style_kwargs.get("italic"):
        parts.append("italic")
    if style_kwargs.get("underline"):
        parts.append("underline")
    if "color" in style_kwargs:
        parts.append(style_kwargs["color"])
    if "bgcolor" in style_kwargs:
        parts.append(f"on {style_kwargs['bgcolor']}")
    
    if parts:
        return f"[{' '.join(parts)}]"
    return ""
