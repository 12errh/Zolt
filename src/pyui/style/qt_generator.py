"""
Qt Style Generator — Converts StyleRules to Qt Stylesheets (QSS).

Generates QSS for Qt5/Qt6 desktop rendering from ZoltCSS StyleRules.
"""

from __future__ import annotations

from collections import defaultdict

from pyui.style.rules import StyleRule
from pyui.style.tokens import TOKENS, BUILT_IN_THEMES


class QtStyleGenerator:
    """
    Generates Qt Stylesheets (QSS) from StyleRule collections.
    
    Maps CSS properties to their QSS equivalents for desktop rendering.
    """
    
    # CSS to QSS property mapping
    CSS_TO_QSS = {
        "background-color": "background-color",
        "color": "color",
        "border": "border",
        "border-radius": "border-radius",
        "padding": "padding",
        "margin": "margin",
        "font-size": "font-size",
        "font-weight": "font-weight",
        "font-family": "font-family",
        "text-decoration": "text-decoration",
        "outline": "outline",
        "box-shadow": None,  # Not supported in QSS
        "width": "width",
        "height": "height",
        "min-width": "min-width",
        "min-height": "min-height",
        "max-width": "max-width",
        "max-height": "max-height",
    }
    
    def __init__(self):
        self._rules: list[StyleRule] = []
        self._widget_rules: dict[str, list[StyleRule]] = defaultdict(list)
    
    def register_rule(self, widget_type: str, rule: StyleRule) -> None:
        """
        Register a style rule for a widget type.
        
        Args:
            widget_type: Qt widget type (e.g., "QPushButton", "QLineEdit")
            rule: StyleRule object
        """
        self._widget_rules[widget_type].append(rule)
        self._rules.append(rule)
    
    def _convert_value(self, value: str) -> str:
        """
        Convert CSS value to QSS-compatible value.
        
        Handles token references and unit conversions.
        """
        # Handle var() references
        if value.startswith("var(--"):
            token_name = value[6:-1]  # Extract token name
            return TOKENS.get(token_name, value)
        
        return value
    
    def _css_to_qss_property(self, css_prop: str) -> str | None:
        """
        Convert CSS property name to QSS property name.
        
        Returns None if property is not supported in QSS.
        """
        return self.CSS_TO_QSS.get(css_prop)
    
    def generate(self, theme: str = "light") -> str:
        """
        Generate complete QSS output.
        
        Args:
            theme: Theme name ("light", "dark", etc.)
            
        Returns:
            Complete QSS string
        """
        qss_parts: list[str] = []
        
        # Apply theme colors
        theme_colors = TOKENS.copy()
        if theme in BUILT_IN_THEMES:
            theme_colors.update(BUILT_IN_THEMES[theme])
        
        # Generate styles for each widget type
        for widget_type, rules in self._widget_rules.items():
            if not rules:
                continue
            
            # Group rules by state
            base_rules: list[StyleRule] = []
            hover_rules: list[StyleRule] = []
            pressed_rules: list[StyleRule] = []
            focus_rules: list[StyleRule] = []
            disabled_rules: list[StyleRule] = []
            
            for rule in rules:
                if rule.state == "hover":
                    hover_rules.append(rule)
                elif rule.state == "active" or rule.state == "pressed":
                    pressed_rules.append(rule)
                elif rule.state == "focus":
                    focus_rules.append(rule)
                elif rule.state == "disabled":
                    disabled_rules.append(rule)
                else:
                    base_rules.append(rule)
            
            # Generate base selector
            if base_rules:
                selector = widget_type
                props = self._generate_properties(base_rules)
                if props:
                    qss_parts.append(f"{selector} {{\n{props}}}")
            
            # Generate hover state
            if hover_rules:
                selector = f"{widget_type}:hover"
                props = self._generate_properties(hover_rules)
                if props:
                    qss_parts.append(f"{selector} {{\n{props}}}")
            
            # Generate pressed/active state
            if pressed_rules:
                selector = f"{widget_type}:pressed"
                props = self._generate_properties(pressed_rules)
                if props:
                    qss_parts.append(f"{selector} {{\n{props}}}")
            
            # Generate focus state
            if focus_rules:
                selector = f"{widget_type}:focus"
                props = self._generate_properties(focus_rules)
                if props:
                    qss_parts.append(f"{selector} {{\n{props}}}")
            
            # Generate disabled state
            if disabled_rules:
                selector = f"{widget_type}:disabled"
                props = self._generate_properties(disabled_rules)
                if props:
                    qss_parts.append(f"{selector} {{\n{props}}}")
        
        return "\n\n".join(qss_parts)
    
    def _generate_properties(self, rules: list[StyleRule]) -> str:
        """
        Generate QSS properties from rules.
        
        Args:
            rules: List of StyleRule objects
            
        Returns:
            Formatted QSS properties string
        """
        lines: list[str] = []
        
        for rule in rules:
            qss_prop = self._css_to_qss_property(rule.property)
            if qss_prop is None:
                continue  # Skip unsupported properties
            
            qss_value = self._convert_value(rule.value)
            lines.append(f"  {qss_prop}: {qss_value};")
        
        if lines:
            return "\n".join(lines) + "\n"
        return ""
    
    def reset(self) -> None:
        """Clear all registered rules."""
        self._rules.clear()
        self._widget_rules.clear()
    
    @property
    def rule_count(self) -> int:
        """Get number of registered rules."""
        return len(self._rules)
