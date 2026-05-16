"""
Tests for ZoltCSS - Phase 0 of v1.5

Tests the new styling engine that replaces Tailwind CSS.
"""

import pytest
from pyui.style.tokens import TOKENS, BUILT_IN_THEMES
from pyui.style.rules import StyleRule, token, create_base_rules, create_state_rules
from pyui.style.resolver import StyleResolver
from pyui.style.css_generator import ZoltCSSGenerator
from pyui.style.qt_generator import QtStyleGenerator
from pyui.style.rich_generator import RichStyleGenerator


class TestTokens:
    """Test the token system."""
    
    def test_tokens_exist(self):
        """Verify tokens dictionary exists and has content."""
        assert isinstance(TOKENS, dict)
        assert len(TOKENS) > 50
    
    def test_color_tokens(self):
        """Verify color tokens are present."""
        assert "color-primary" in TOKENS
        assert "color-secondary" in TOKENS
        assert "color-bg" in TOKENS
        assert "color-text" in TOKENS
        assert "color-success" in TOKENS
        assert "color-danger" in TOKENS
    
    def test_typography_tokens(self):
        """Verify typography tokens are present."""
        assert "font-family" in TOKENS
        assert "font-size-sm" in TOKENS
        assert "font-size-md" in TOKENS
        assert "font-size-lg" in TOKENS
        assert "font-weight-normal" in TOKENS
        assert "font-weight-bold" in TOKENS
    
    def test_spacing_tokens(self):
        """Verify spacing tokens are present."""
        assert "space-0" in TOKENS
        assert "space-4" in TOKENS
        assert "space-8" in TOKENS
        assert "space-16" in TOKENS
    
    def test_radius_tokens(self):
        """Verify border radius tokens are present."""
        assert "radius-none" in TOKENS
        assert "radius-md" in TOKENS
        assert "radius-lg" in TOKENS
        assert "radius-full" in TOKENS
    
    def test_shadow_tokens(self):
        """Verify shadow tokens are present."""
        assert "shadow-sm" in TOKENS
        assert "shadow-md" in TOKENS
        assert "shadow-lg" in TOKENS
    
    def test_builtin_themes(self):
        """Verify built-in themes exist."""
        assert isinstance(BUILT_IN_THEMES, dict)
        assert "light" in BUILT_IN_THEMES
        assert "dark" in BUILT_IN_THEMES
        assert "ocean" in BUILT_IN_THEMES
        assert "forest" in BUILT_IN_THEMES
    
    def test_dark_theme_overrides(self):
        """Verify dark theme has proper overrides."""
        dark = BUILT_IN_THEMES["dark"]
        assert "color-bg" in dark
        assert "color-text" in dark
        # Dark mode should have dark background
        assert dark["color-bg"] != TOKENS["color-bg"]


class TestStyleRule:
    """Test StyleRule dataclass."""
    
    def test_create_basic_rule(self):
        """Test creating a basic style rule."""
        rule = StyleRule(property="color", value="red")
        assert rule.property == "color"
        assert rule.value == "red"
        assert rule.breakpoint is None
        assert rule.state is None
    
    def test_create_rule_with_modifiers(self):
        """Test creating a rule with modifiers."""
        rule = StyleRule(
            property="background-color",
            value="blue",
            breakpoint="md",
            state="hover",
            dark_mode="darkblue",
        )
        assert rule.breakpoint == "md"
        assert rule.state == "hover"
        assert rule.dark_mode == "darkblue"
    
    def test_rule_to_css_declaration(self):
        """Test converting rule to CSS declaration."""
        rule = StyleRule(property="padding", value="16px")
        assert rule.to_css_declaration() == "padding: 16px;"
    
    def test_rule_has_modifier(self):
        """Test checking if rule has modifiers."""
        base_rule = StyleRule(property="color", value="red")
        assert not base_rule.has_modifier()
        
        mod_rule = StyleRule(property="color", value="red", state="hover")
        assert mod_rule.has_modifier()
    
    def test_rule_hashable(self):
        """Test that rules are hashable for deduplication."""
        rule1 = StyleRule(property="color", value="red")
        rule2 = StyleRule(property="color", value="red")
        rule3 = StyleRule(property="color", value="blue")
        
        rule_set = {rule1, rule2, rule3}
        assert len(rule_set) == 2  # rule1 and rule2 are equal
    
    def test_rule_equality(self):
        """Test rule equality."""
        rule1 = StyleRule(property="color", value="red")
        rule2 = StyleRule(property="color", value="red")
        rule3 = StyleRule(property="color", value="blue")
        
        assert rule1 == rule2
        assert rule1 != rule3


class TestTokenHelper:
    """Test token helper functions."""
    
    def test_token_function(self):
        """Test token() helper creates var() references."""
        result = token("color-primary")
        assert result == "var(--color-primary)"
    
    def test_token_with_spacing(self):
        """Test token() with spacing tokens."""
        result = token("space-4")
        assert result == "var(--space-4)"


class TestStyleResolver:
    """Test StyleResolver component resolution."""
    
    def test_resolver_exists(self):
        """Test that resolver can be instantiated."""
        resolver = StyleResolver()
        assert resolver is not None
    
    def test_resolve_button(self):
        """Test resolving button styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("button", variant="primary", size="md")
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_button_disabled(self):
        """Test resolving disabled button styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("button", variant="primary", disabled=True)
        assert isinstance(rules, list)
        # Should include disabled state rules
        disabled_rules = [r for r in rules if r.state == "disabled"]
        assert len(disabled_rules) > 0
    
    def test_resolve_text(self):
        """Test resolving text styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("text", variant="muted", size="sm")
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_heading(self):
        """Test resolving heading styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("heading", level=1)
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_flex(self):
        """Test resolving flex container styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("flex", direction="col", gap=4)
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_grid(self):
        """Test resolving grid container styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("grid", cols=3, gap=6)
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_box(self):
        """Test resolving box container styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("box", padding=4, shadow="md")
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_input(self):
        """Test resolving input styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("input", error=True)
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_badge(self):
        """Test resolving badge styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("badge", variant="success")
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_card(self):
        """Test resolving card styles."""
        resolver = StyleResolver()
        rules = resolver.resolve("card", padding=6, shadow="lg")
        assert isinstance(rules, list)
        assert len(rules) > 0
    
    def test_resolve_unknown_component(self):
        """Test that unknown component raises error."""
        resolver = StyleResolver()
        with pytest.raises(ValueError, match="Unknown component"):
            resolver.resolve("unknown_component")
    
    def test_register_custom_component(self):
        """Test registering custom component resolver."""
        resolver = StyleResolver()
        
        def custom_resolver(**kwargs):
            return [StyleRule(property="color", value="purple")]
        
        resolver.register_component("custom", custom_resolver)
        rules = resolver.resolve("custom")
        assert len(rules) == 1
        assert rules[0].value == "purple"


class TestZoltCSSGenerator:
    """Test CSS generation."""
    
    def test_generator_exists(self):
        """Test that generator can be instantiated."""
        gen = ZoltCSSGenerator()
        assert gen is not None
    
    def test_register_rule(self):
        """Test registering a rule."""
        gen = ZoltCSSGenerator()
        rule = StyleRule(property="color", value="red")
        class_name = gen.register_rule(rule)
        assert isinstance(class_name, str)
        assert len(class_name) > 0
    
    def test_register_rules(self):
        """Test registering multiple rules."""
        gen = ZoltCSSGenerator()
        rules = [
            StyleRule(property="color", value="red"),
            StyleRule(property="background", value="blue"),
        ]
        class_names = gen.register_rules(rules)
        assert len(class_names) == 2
    
    def test_rule_deduplication(self):
        """Test that duplicate rules get same class name."""
        gen = ZoltCSSGenerator()
        rule1 = StyleRule(property="color", value="red")
        rule2 = StyleRule(property="color", value="red")
        
        class1 = gen.register_rule(rule1)
        class2 = gen.register_rule(rule2)
        
        assert class1 == class2
    
    def test_generate_css_variables(self):
        """Test generating CSS variables."""
        gen = ZoltCSSGenerator()
        css = gen.generate_css_variables("light")
        assert ":root {" in css
        assert "--color-primary:" in css
    
    def test_generate_dark_mode_variables(self):
        """Test generating dark mode variables."""
        gen = ZoltCSSGenerator()
        css = gen.generate_dark_mode_variables()
        assert "[data-theme='dark']" in css
        assert "--color-bg:" in css
    
    def test_generate_complete_css(self):
        """Test generating complete CSS."""
        gen = ZoltCSSGenerator()
        
        # Register some rules
        resolver = StyleResolver()
        button_rules = resolver.resolve("button", variant="primary")
        gen.register_rules(button_rules)
        
        css = gen.generate()
        assert ":root {" in css
        assert ".zolt-" in css or ".z" in css
    
    def test_production_mode(self):
        """Test production mode generates short class names."""
        gen = ZoltCSSGenerator(mode="production")
        rule = StyleRule(property="color", value="red")
        class_name = gen.register_rule(rule)
        assert class_name.startswith("z")
        assert len(class_name) < 15
    
    def test_development_mode(self):
        """Test development mode generates descriptive class names."""
        gen = ZoltCSSGenerator(mode="development")
        rule = StyleRule(property="color", value="red")
        class_name = gen.register_rule(rule)
        assert class_name.startswith("zolt-")
        assert len(class_name) > 15
    
    def test_reset(self):
        """Test resetting generator."""
        gen = ZoltCSSGenerator()
        rule = StyleRule(property="color", value="red")
        gen.register_rule(rule)
        assert gen.rule_count > 0
        
        gen.reset()
        assert gen.rule_count == 0


class TestQtStyleGenerator:
    """Test Qt stylesheet generation."""
    
    def test_qt_generator_exists(self):
        """Test that Qt generator can be instantiated."""
        gen = QtStyleGenerator()
        assert gen is not None
    
    def test_register_rule(self):
        """Test registering a rule for Qt widget."""
        gen = QtStyleGenerator()
        rule = StyleRule(property="background-color", value="red")
        gen.register_rule("QPushButton", rule)
        assert gen.rule_count == 1
    
    def test_generate_qss(self):
        """Test generating QSS."""
        gen = QtStyleGenerator()
        rule = StyleRule(property="background-color", value="#FF0000")
        gen.register_rule("QPushButton", rule)
        
        qss = gen.generate()
        assert "QPushButton" in qss
        assert "background-color:" in qss


class TestRichStyleGenerator:
    """Test Rich terminal style generation."""
    
    def test_rich_generator_exists(self):
        """Test that Rich generator can be instantiated."""
        gen = RichStyleGenerator()
        assert gen is not None
    
    def test_register_rule(self):
        """Test registering a rule for Rich component."""
        gen = RichStyleGenerator()
        rule = StyleRule(property="color", value="#FF0000")
        gen.register_rule("text", rule)
        assert gen.rule_count == 1
    
    def test_generate_style(self):
        """Test generating Rich style kwargs."""
        gen = RichStyleGenerator()
        rule = StyleRule(property="color", value="#FF0000")
        gen.register_rule("text", rule)
        
        style = gen.generate_style("text")
        assert isinstance(style, dict)
        assert "color" in style
    
    def test_hex_to_rich_color(self):
        """Test hex to Rich color conversion."""
        gen = RichStyleGenerator()
        color = gen._hex_to_rich_color("#FF0000")
        assert color == "red"
