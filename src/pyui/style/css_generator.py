"""
ZoltCSS Generator — Converts StyleRules to optimized CSS.

Takes collected StyleRules from components and generates a single,
deduplicated, optimized CSS file with zero Tailwind dependency.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

from pyui.style.rules import StyleRule, token
from pyui.style.tokens import TOKENS


class ZoltCSSGenerator:
    """
    Generates optimized CSS from StyleRule collections.
    
    Features:
    - Deduplication of identical rules
    - Atomic class generation (short hashes for production)
    - Descriptive class names for development
    - Media query grouping for responsive rules
    - Dark mode via [data-theme='dark'] selector
    - State selectors (:hover, :active, :focus, :disabled)
    
    Example:
        generator = ZoltCSSGenerator()
        generator.register_rule(StyleRule(...))
        css = generator.generate(mode="production")
    """
    
    def __init__(self, mode: str = "development"):
        """
        Initialize the CSS generator.
        
        Args:
            mode: "development" or "production"
                   - development: descriptive class names
                   - production: short atomic hashes
        """
        self.mode = mode
        self._rules: list[StyleRule] = []
        self._rule_map: dict[tuple, str] = {}  # (props) -> class_name
        self._class_counter: int = 0
        
        # CSS variable definitions from tokens
        self._css_variables: dict[str, str] = {}
    
    def register_rule(self, rule: StyleRule) -> str:
        """
        Register a style rule and get its class name.
        
        Args:
            rule: StyleRule object
            
        Returns:
            Generated class name for this rule
        """
        # Create a unique key for deduplication
        rule_key = (
            rule.property,
            rule.value,
            rule.breakpoint,
            rule.dark_mode,
            rule.state,
        )
        
        # Check if we already have this rule
        if rule_key in self._rule_map:
            return self._rule_map[rule_key]
        
        # Generate new class name
        class_name = self._generate_class_name(rule)
        self._rule_map[rule_key] = class_name
        self._rules.append(rule)
        
        return class_name
    
    def register_rules(self, rules: list[StyleRule]) -> list[str]:
        """
        Register multiple style rules.
        
        Args:
            rules: List of StyleRule objects
            
        Returns:
            List of generated class names
        """
        return [self.register_rule(rule) for rule in rules]
    
    def _generate_class_name(self, rule: StyleRule) -> str:
        """
        Generate a class name for a rule.
        
        In development mode: descriptive names like "btn-bg-primary"
        In production mode: atomic hashes like "a1b2c3"
        """
        if self.mode == "production":
            # Generate short hash
            rule_str = f"{rule.property}-{rule.value}-{rule.state}-{rule.breakpoint}"
            hash_input = rule_str.encode()
            hash_value = hashlib.md5(hash_input).hexdigest()[:6]
            return f"z{hash_value}"
        else:
            # Development: descriptive name
            self._class_counter += 1
            
            # Sanitize property name
            prop_short = rule.property.replace("-", "")
            if len(prop_short) > 8:
                prop_short = prop_short[:8]
            
            # Add value hint
            value_hint = rule.value.replace("var(--", "").replace(")", "").replace(".", "-")
            if len(value_hint) > 12:
                value_hint = value_hint[:12]
            
            parts = [prop_short, value_hint]
            
            if rule.state:
                parts.append(rule.state)
            if rule.breakpoint:
                parts.append(f"bp-{rule.breakpoint}")
            
            return f"zolt-{'-'.join(parts)}-{self._class_counter}"
    
    def _get_css_value(self, value: str) -> str:
        """
        Resolve token references to actual values.
        
        If value is already a var() reference, keep it.
        If it's a raw token name, convert it.
        """
        if value.startswith("var(--"):
            return value
        return value
    
    def generate_css_variables(self, theme: str = "light") -> str:
        """
        Generate CSS custom properties (variables) from tokens.
        
        Args:
            theme: Theme name ("light", "dark", etc.)
            
        Returns:
            CSS :root block with all variables
        """
        from pyui.style.tokens import BUILT_IN_THEMES
        
        # Start with base tokens
        all_tokens = TOKENS.copy()
        
        # Apply theme overrides
        if theme in BUILT_IN_THEMES:
            all_tokens.update(BUILT_IN_THEMES[theme])
        
        # Convert to CSS variables
        lines = [":root {"]
        for token_name, token_value in sorted(all_tokens.items()):
            # Convert token name to CSS variable format
            # e.g., "color-primary" -> "--color-primary"
            css_var = f"--{token_name}"
            lines.append(f"  {css_var}: {token_value};")
        lines.append("}")
        
        return "\n".join(lines)
    
    def generate_dark_mode_variables(self) -> str:
        """
        Generate dark theme CSS variables override.
        
        Returns:
            CSS [data-theme='dark'] block
        """
        from pyui.style.tokens import DARK_OVERRIDES
        
        if not DARK_OVERRIDES:
            return ""
        
        lines = ["[data-theme='dark'] {"]
        for token_name, token_value in sorted(DARK_OVERRIDES.items()):
            css_var = f"--{token_name}"
            lines.append(f"  {css_var}: {token_value};")
        lines.append("}")
        
        return "\n".join(lines)
    
    def _group_rules(self) -> dict[str, list[StyleRule]]:
        """
        Group rules by their modifiers (breakpoint, state, dark_mode).
        
        Returns:
            Dict mapping group keys to lists of rules
        """
        groups: dict[str, list[StyleRule]] = defaultdict(list)
        
        for rule in self._rules:
            # Determine group key
            if rule.breakpoint:
                group_key = f"media-{rule.breakpoint}"
            elif rule.dark_mode:
                group_key = "dark-mode"
            elif rule.state:
                group_key = f"state-{rule.state}"
            else:
                group_key = "base"
            
            groups[group_key].append(rule)
        
        return groups
    
    def generate(self, theme: str = "light") -> str:
        """
        Generate complete CSS output.
        
        Args:
            theme: Theme name for CSS variables
            
        Returns:
            Complete CSS string
        """
        css_parts: list[str] = []
        
        # 1. CSS Variables
        css_parts.append(self.generate_css_variables(theme))
        css_parts.append("")
        
        # 2. Dark mode variables
        dark_vars = self.generate_dark_mode_variables()
        if dark_vars:
            css_parts.append(dark_vars)
            css_parts.append("")
        
        # 3. Group rules by modifier
        grouped = self._group_rules()
        
        # 4. Generate base styles (no modifiers)
        if "base" in grouped:
            base_rules = grouped["base"]
            # Group by class name
            by_class: dict[str, list[StyleRule]] = defaultdict(list)
            for rule in base_rules:
                class_name = self._rule_map.get((
                    rule.property,
                    rule.value,
                    rule.breakpoint,
                    rule.dark_mode,
                    rule.state,
                ), self._generate_class_name(rule))
                by_class[class_name].append(rule)
            
            # Generate CSS
            for class_name, rules in by_class.items():
                props = "\n  ".join(rule.to_css_declaration() for rule in rules)
                css_parts.append(f".{class_name} {{\n  {props}\n}}")
        
        # 5. Generate state-based styles
        for state in ["hover", "active", "focus", "disabled"]:
            state_key = f"state-{state}"
            if state_key in grouped:
                state_rules = grouped[state_key]
                by_class: dict[str, list[StyleRule]] = defaultdict(list)
                for rule in state_rules:
                    class_name = self._rule_map.get((
                        rule.property,
                        rule.value,
                        rule.breakpoint,
                        rule.dark_mode,
                        rule.state,
                    ), self._generate_class_name(rule))
                    by_class[class_name].append(rule)
                
                for class_name, rules in by_class.items():
                    props = "\n  ".join(rule.to_css_declaration() for rule in rules)
                    css_parts.append(f".{class_name}:{state} {{\n  {props}\n}}")
        
        # 6. Generate media queries for breakpoints
        breakpoint_map = {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px",
        }
        
        for bp in ["sm", "md", "lg", "xl", "2xl"]:
            bp_key = f"media-{bp}"
            if bp_key in grouped:
                bp_rules = grouped[bp_key]
                min_width = breakpoint_map[bp]
                
                # Group by class name
                by_class: dict[str, list[StyleRule]] = defaultdict(list)
                for rule in bp_rules:
                    class_name = self._rule_map.get((
                        rule.property,
                        rule.value,
                        rule.breakpoint,
                        rule.dark_mode,
                        rule.state,
                    ), self._generate_class_name(rule))
                    by_class[class_name].append(rule)
                
                # Generate media query block
                media_rules: list[str] = []
                for class_name, rules in by_class.items():
                    props = "\n    ".join(rule.to_css_declaration() for rule in rules)
                    media_rules.append(f"  .{class_name} {{\n    {props}\n  }}")
                
                if media_rules:
                    css_parts.append(f"@media (min-width: {min_width}) {{")
                    css_parts.append("\n".join(media_rules))
                    css_parts.append("}")
        
        return "\n\n".join(css_parts)
    
    def generate_minified(self, theme: str = "light") -> str:
        """
        Generate minified CSS (no whitespace).
        
        Args:
            theme: Theme name
            
        Returns:
            Minified CSS string
        """
        css = self.generate(theme)
        # Remove comments and extra whitespace
        lines = css.split("\n")
        minified_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("/*"):
                minified_lines.append(stripped)
        return "".join(minified_lines)
    
    def reset(self) -> None:
        """Clear all registered rules."""
        self._rules.clear()
        self._rule_map.clear()
        self._class_counter = 0
    
    @property
    def rule_count(self) -> int:
        """Get number of registered rules."""
        return len(self._rules)
    
    @property
    def class_count(self) -> int:
        """Get number of unique classes."""
        return len(self._class_counter)
