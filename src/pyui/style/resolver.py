"""
ZoltCSS Style Resolver — Component style resolution engine.

Resolves component + variant + state combinations into StyleRule collections.
This is where components define their visual appearance using the token system.
"""

from __future__ import annotations

from typing import Any

from pyui.style.rules import (
    StyleRule,
    create_base_rules,
    create_state_rules,
    create_responsive_rules,
    token,
)


class StyleResolver:
    """
    Resolves component styling into StyleRule collections.
    
    Each component has a resolver method that returns all StyleRules
    needed to render that component in a given variant and state.
    
    Example:
        resolver = StyleResolver()
        rules = resolver.resolve_button(variant="primary", size="md", disabled=False)
    """
    
    def __init__(self):
        self._component_resolvers: dict[str, callable] = {
            "button": self.resolve_button,
            "text": self.resolve_text,
            "heading": self.resolve_heading,
            "flex": self.resolve_flex,
            "grid": self.resolve_grid,
            "box": self.resolve_box,
            "input": self.resolve_input,
            "badge": self.resolve_badge,
            "card": self.resolve_card,
            "divider": self.resolve_divider,
        }
    
    def resolve(
        self,
        component: str,
        **kwargs: Any,
    ) -> list[StyleRule]:
        """
        Resolve styles for a component.
        
        Args:
            component: Component name (e.g., "button", "text")
            **kwargs: Component-specific parameters (variant, size, etc.)
            
        Returns:
            List of StyleRule objects
            
        Raises:
            ValueError: If component is not registered
        """
        if component not in self._component_resolvers:
            raise ValueError(
                f"Unknown component: {component}. "
                f"Registered components: {list(self._component_resolvers.keys())}"
            )
        
        resolver = self._component_resolvers[component]
        return resolver(**kwargs)
    
    def register_component(
        self,
        name: str,
        resolver_func: callable,
    ) -> None:
        """
        Register a custom component resolver.
        
        Args:
            name: Component name
            resolver_func: Function that resolves component styles
        """
        self._component_resolvers[name] = resolver_func
    
    # ── Component Resolvers ────────────────────────────────────────────────
    
    def resolve_button(
        self,
        variant: str | None = "primary",
        size: str | None = "md",
        disabled: bool = False,
    ) -> list[StyleRule]:
        """Resolve Button component styles."""
        rules: list[StyleRule] = []
        
        # Base button styles
        base_rules = [
            ("display", "inline-flex"),
            ("align-items", "center"),
            ("justify-content", "center"),
            ("gap", token("space-2")),
            ("font-family", token("font-family")),
            ("font-weight", token("font-weight-medium")),
            ("letter-spacing", token("letter-spacing-tight")),
            ("transition-property", "all"),
            ("transition-duration", token("transition-normal")),
            ("transition-timing-function", token("transition-timing")),
            ("cursor", "pointer"),
            ("border", "none"),
            ("outline", "none"),
        ]
        rules.extend(create_base_rules("button", base_rules))
        
        # Size variants
        size_rules = {
            "xs": [("height", token("space-7")), ("padding-left", token("space-3")), ("padding-right", token("space-3")), ("font-size", token("font-size-xs")), ("border-radius", token("radius-md"))],
            "sm": [("height", token("space-8")), ("padding-left", token("space-4")), ("padding-right", token("space-4")), ("font-size", token("font-size-sm")), ("border-radius", token("radius-lg"))],
            "md": [("height", token("space-9")), ("padding-left", token("space-4")), ("padding-right", token("space-4")), ("font-size", token("font-size-sm")), ("border-radius", token("radius-lg"))],
            "lg": [("height", token("space-11")), ("padding-left", token("space-6")), ("padding-right", token("space-6")), ("font-size", token("font-size-md")), ("border-radius", token("radius-xl"))],
            "xl": [("height", token("space-12")), ("padding-left", token("space-8")), ("padding-right", token("space-8")), ("font-size", token("font-size-md")), ("border-radius", token("radius-xl"))],
        }
        
        if size in size_rules:
            rules.extend(create_base_rules("button", size_rules[size]))
        
        # Color variants
        variant_styles = {
            "primary": [
                ("background-color", token("color-primary")),
                ("color", token("color-primary-fg")),
                ("box-shadow", token("shadow-sm")),
            ],
            "secondary": [
                ("background-color", token("color-secondary")),
                ("color", token("color-secondary-fg")),
            ],
            "ghost": [
                ("background-color", token("color-bg")),
                ("color", token("color-text")),
                ("border", f"1px solid {token('color-border')}"),
                ("box-shadow", token("shadow-sm")),
            ],
            "danger": [
                ("background-color", token("color-danger")),
                ("color", token("color-danger-fg")),
                ("box-shadow", token("shadow-sm")),
            ],
            "success": [
                ("background-color", token("color-success")),
                ("color", token("color-success-fg")),
                ("box-shadow", token("shadow-sm")),
            ],
            "link": [
                ("background-color", "transparent"),
                ("color", token("color-text")),
                ("text-decoration", "underline"),
                ("text-underline-offset", "4px"),
                ("padding", "0"),
                ("height", "auto"),
                ("box-shadow", "none"),
            ],
        }
        
        if variant in variant_styles:
            rules.extend(create_base_rules("button", variant_styles[variant]))
        
        # Hover states
        hover_styles = {
            "primary": [
                ("background-color", token("color-primary-hover")),
                ("box-shadow", token("shadow-md")),
                ("transform", "translateY(-1px)"),
            ],
            "secondary": [
                ("background-color", token("color-secondary-hover")),
                ("transform", "translateY(-1px)"),
            ],
            "ghost": [
                ("background-color", token("color-surface")),
                ("border-color", token("color-border-strong")),
                ("transform", "translateY(-1px)"),
            ],
            "danger": [
                ("background-color", token("color-danger-hover")),
                ("box-shadow", token("shadow-md")),
                ("transform", "translateY(-1px)"),
            ],
            "success": [
                ("background-color", token("color-success-hover")),
                ("transform", "translateY(-1px)"),
            ],
            "link": [
                ("text-decoration-color", token("color-text")),
            ],
        }
        
        if variant and variant in hover_styles:
            rules.extend(create_state_rules("button", "hover", hover_styles[variant]))
        
        # Disabled state
        if disabled:
            disabled_rules = [
                ("opacity", "0.4"),
                ("cursor", "not-allowed"),
                ("pointer-events", "none"),
                ("filter", "saturate(0)"),
            ]
            rules.extend(create_state_rules("button", "disabled", disabled_rules))
        
        # Active state (press)
        active_rules = [
            ("transform", "scale(0.97)"),
        ]
        rules.extend(create_state_rules("button", "active", active_rules))
        
        # Focus state
        focus_rules = [
            ("box-shadow", f"0 0 0 2px {token('color-bg')}, 0 0 0 4px {token('color-primary')}"),
        ]
        rules.extend(create_state_rules("button", "focus", focus_rules))
        
        return rules
    
    def resolve_text(
        self,
        variant: str | None = None,
        size: str | None = None,
        truncate: bool = False,
    ) -> list[StyleRule]:
        """Resolve Text component styles."""
        rules: list[StyleRule] = []
        
        # Base text styles
        base_rules = [
            ("font-family", token("font-family")),
            ("line-height", token("line-height-normal")),
            ("color", token("color-text")),
        ]
        rules.extend(create_base_rules("text", base_rules))
        
        # Size variants
        size_rules = {
            "xs": [("font-size", token("font-size-xs"))],
            "sm": [("font-size", token("font-size-sm"))],
            "md": [("font-size", token("font-size-md"))],
            "lg": [("font-size", token("font-size-lg"))],
            "xl": [("font-size", token("font-size-xl"))],
            "2xl": [("font-size", token("font-size-2xl"))],
        }
        
        if size in size_rules:
            rules.extend(create_base_rules("text", size_rules[size]))
        
        # Variant styles
        variant_styles = {
            "muted": [
                ("color", token("color-text-muted")),
                ("line-height", token("line-height-relaxed")),
            ],
            "error": [
                ("color", token("color-danger")),
                ("font-size", token("font-size-sm")),
            ],
            "success": [
                ("color", token("color-success")),
                ("font-size", token("font-size-sm")),
            ],
            "caption": [
                ("font-size", token("font-size-xs")),
                ("color", token("color-text-muted")),
                ("text-transform", "uppercase"),
                ("letter-spacing", token("letter-spacing-wider")),
                ("font-weight", token("font-weight-medium")),
            ],
        }
        
        if variant in variant_styles:
            rules.extend(create_base_rules("text", variant_styles[variant]))
        
        # Truncate
        if truncate:
            truncate_rules = [
                ("overflow", "hidden"),
                ("text-overflow", "ellipsis"),
                ("white-space", "nowrap"),
            ]
            rules.extend(create_base_rules("text", truncate_rules))
        
        return rules
    
    def resolve_heading(
        self,
        level: int = 2,
        variant: str | None = None,
    ) -> list[StyleRule]:
        """Resolve Heading component styles."""
        rules: list[StyleRule] = []
        
        # Level-based styles
        level_styles = {
            1: [
                ("font-size", token("font-size-4xl")),
                ("font-weight", token("font-weight-bold")),
                ("letter-spacing", token("letter-spacing-tight")),
                ("line-height", "1.1"),
            ],
            2: [
                ("font-size", token("font-size-3xl")),
                ("font-weight", token("font-weight-bold")),
                ("letter-spacing", token("letter-spacing-tight")),
                ("line-height", "1.2"),
            ],
            3: [
                ("font-size", token("font-size-2xl")),
                ("font-weight", token("font-weight-semibold")),
                ("letter-spacing", token("letter-spacing-tight")),
                ("line-height", "1.3"),
            ],
            4: [
                ("font-size", token("font-size-xl")),
                ("font-weight", token("font-weight-semibold")),
                ("letter-spacing", token("letter-spacing-tight")),
                ("line-height", "1.4"),
            ],
            5: [
                ("font-size", token("font-size-lg")),
                ("font-weight", token("font-weight-medium")),
                ("letter-spacing", token("letter-spacing-tight")),
            ],
            6: [
                ("font-size", token("font-size-md")),
                ("font-weight", token("font-weight-medium")),
                ("letter-spacing", token("letter-spacing-tight")),
            ],
        }
        
        if level in level_styles:
            rules.extend(create_base_rules("heading", level_styles[level]))
        
        # Default color
        rules.extend(create_base_rules("heading", [
            ("color", token("color-text")),
        ]))
        
        # Variant styles
        if variant == "muted":
            rules.extend(create_base_rules("heading", [
                ("color", token("color-text-muted")),
                ("font-weight", token("font-weight-normal")),
            ]))
        
        return rules
    
    def resolve_flex(
        self,
        direction: str = "row",
        align: str = "center",
        justify: str = "start",
        gap: int = 4,
        wrap: bool = False,
    ) -> list[StyleRule]:
        """Resolve Flex container styles."""
        rules: list[StyleRule] = []
        
        # Base flex
        rules.extend(create_base_rules("flex", [
            ("display", "flex"),
        ]))
        
        # Direction
        direction_map = {
            "row": "row",
            "col": "column",
            "row-reverse": "row-reverse",
            "col-reverse": "column-reverse",
        }
        rules.extend(create_base_rules("flex", [
            ("flex-direction", direction_map.get(direction, "row")),
        ]))
        
        # Alignment
        align_map = {
            "start": "flex-start",
            "center": "center",
            "end": "flex-end",
            "baseline": "baseline",
            "stretch": "stretch",
        }
        rules.extend(create_base_rules("flex", [
            ("align-items", align_map.get(align, "center")),
        ]))
        
        # Justify
        justify_map = {
            "start": "flex-start",
            "center": "center",
            "end": "flex-end",
            "between": "space-between",
            "around": "space-around",
            "evenly": "space-evenly",
        }
        rules.extend(create_base_rules("flex", [
            ("justify-content", justify_map.get(justify, "start")),
        ]))
        
        # Gap
        gap_token = f"space-{gap}" if gap in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16] else "space-4"
        rules.extend(create_base_rules("flex", [
            ("gap", token(gap_token)),
        ]))
        
        # Wrap
        if wrap:
            rules.extend(create_base_rules("flex", [
                ("flex-wrap", "wrap"),
            ]))
        
        return rules
    
    def resolve_grid(
        self,
        cols: int | str = 1,
        gap: int = 4,
    ) -> list[StyleRule]:
        """Resolve Grid container styles."""
        rules: list[StyleRule] = []
        
        # Base grid
        rules.extend(create_base_rules("grid", [
            ("display", "grid"),
        ]))
        
        # Columns
        if isinstance(cols, int):
            rules.extend(create_base_rules("grid", [
                ("grid-template-columns", f"repeat({cols}, 1fr)"),
            ]))
        else:
            rules.extend(create_base_rules("grid", [
                ("grid-template-columns", cols),
            ]))
        
        # Gap
        gap_token = f"space-{gap}" if gap in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16] else "space-4"
        rules.extend(create_base_rules("grid", [
            ("gap", token(gap_token)),
        ]))
        
        return rules
    
    def resolve_box(
        self,
        padding: int | None = None,
        margin: int | None = None,
        background: str | None = None,
        border_radius: str | None = None,
        shadow: str | None = None,
    ) -> list[StyleRule]:
        """Resolve Box container styles."""
        rules: list[StyleRule] = []
        
        # Base box
        rules.extend(create_base_rules("box", [
            ("display", "block"),
        ]))
        
        # Padding
        if padding is not None:
            padding_token = f"space-{padding}" if padding in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16] else "space-4"
            rules.extend(create_base_rules("box", [
                ("padding", token(padding_token)),
            ]))
        
        # Margin
        if margin is not None:
            margin_token = f"space-{margin}" if margin in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16] else "space-4"
            rules.extend(create_base_rules("box", [
                ("margin", token(margin_token)),
            ]))
        
        # Background
        if background:
            if background.startswith("color-"):
                rules.extend(create_base_rules("box", [
                    ("background-color", token(background)),
                ]))
            else:
                rules.extend(create_base_rules("box", [
                    ("background-color", background),
                ]))
        
        # Border radius
        if border_radius:
            radius_token = f"radius-{border_radius}" if border_radius in ["none", "sm", "md", "lg", "xl", "2xl", "full"] else "radius-md"
            rules.extend(create_base_rules("box", [
                ("border-radius", token(radius_token)),
            ]))
        
        # Shadow
        if shadow:
            shadow_token = f"shadow-{shadow}" if shadow in ["xs", "sm", "md", "lg", "xl", "2xl", "inner", "none"] else "shadow-md"
            rules.extend(create_base_rules("box", [
                ("box-shadow", token(shadow_token)),
            ]))
        
        return rules
    
    def resolve_input(
        self,
        variant: str | None = None,
        disabled: bool = False,
        error: bool = False,
    ) -> list[StyleRule]:
        """Resolve Input component styles."""
        rules: list[StyleRule] = []
        
        # Base input styles
        base_rules = [
            ("display", "block"),
            ("width", "100%"),
            ("font-family", token("font-family")),
            ("font-size", token("font-size-sm")),
            ("padding-left", token("space-4")),
            ("padding-right", token("space-4")),
            ("padding-top", token("space-3")),
            ("padding-bottom", token("space-3")),
            ("border-radius", token("radius-lg")),
            ("border", f"1px solid {token('color-border')}"),
            ("background-color", token("color-bg")),
            ("color", token("color-text")),
            ("transition-property", "all"),
            ("transition-duration", token("transition-fast")),
            ("transition-timing-function", token("transition-timing")),
            ("outline", "none"),
        ]
        rules.extend(create_base_rules("input", base_rules))
        
        # Hover state
        rules.extend(create_state_rules("input", "hover", [
            ("border-color", token("color-border-strong")),
        ]))
        
        # Focus state
        rules.extend(create_state_rules("input", "focus", [
            ("border-color", token("color-border-strong")),
            ("box-shadow", f"0 0 0 3px {token('color-primary-subtle')}"),
        ]))
        
        # Error state
        if error:
            rules.extend(create_base_rules("input", [
                ("border-color", token("color-danger")),
                ("box-shadow", f"0 0 0 3px {token('color-danger-subtle')}"),
            ]))
        
        # Disabled state
        if disabled:
            rules.extend(create_state_rules("input", "disabled", [
                ("opacity", "0.5"),
                ("cursor", "not-allowed"),
                ("background-color", token("color-surface")),
            ]))
        
        return rules
    
    def resolve_badge(
        self,
        variant: str | None = "primary",
    ) -> list[StyleRule]:
        """Resolve Badge component styles."""
        rules: list[StyleRule] = []
        
        # Base badge styles
        base_rules = [
            ("display", "inline-flex"),
            ("align-items", "center"),
            ("gap", token("space-1")),
            ("padding-left", token("space-3")),
            ("padding-right", token("space-3")),
            ("padding-top", "2px"),
            ("padding-bottom", "2px"),
            ("border-radius", token("radius-full")),
            ("font-size", token("font-size-xs")),
            ("font-weight", token("font-weight-medium")),
            ("letter-spacing", token("letter-spacing-wide")),
            ("border", "1px solid"),
        ]
        rules.extend(create_base_rules("badge", base_rules))
        
        # Variant styles
        variant_styles = {
            "primary": [
                ("background-color", token("color-primary-subtle")),
                ("color", token("color-primary")),
                ("border-color", f"{token('color-primary')}80"),  # 50% opacity
            ],
            "secondary": [
                ("background-color", token("color-surface")),
                ("color", token("color-text-muted")),
                ("border-color", token("color-border")),
            ],
            "success": [
                ("background-color", token("color-success-subtle")),
                ("color", token("color-success")),
                ("border-color", f"{token('color-success')}80"),
            ],
            "danger": [
                ("background-color", token("color-danger-subtle")),
                ("color", token("color-danger")),
                ("border-color", f"{token('color-danger')}80"),
            ],
            "warning": [
                ("background-color", token("color-warning-subtle")),
                ("color", token("color-warning")),
                ("border-color", f"{token('color-warning')}80"),
            ],
            "info": [
                ("background-color", token("color-info-subtle")),
                ("color", token("color-info")),
                ("border-color", f"{token('color-info')}80"),
            ],
        }
        
        if variant in variant_styles:
            rules.extend(create_base_rules("badge", variant_styles[variant]))
        
        return rules
    
    def resolve_card(
        self,
        padding: int = 6,
        shadow: str = "md",
        border_radius: str = "xl",
    ) -> list[StyleRule]:
        """Resolve Card component styles."""
        rules: list[StyleRule] = []
        
        # Base card styles
        base_rules = [
            ("display", "block"),
            ("background-color", token("color-surface")),
            ("border", f"1px solid {token('color-border')}"),
        ]
        rules.extend(create_base_rules("card", base_rules))
        
        # Padding
        padding_token = f"space-{padding}" if padding in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16] else "space-6"
        rules.extend(create_base_rules("card", [
            ("padding", token(padding_token)),
        ]))
        
        # Shadow
        shadow_token = f"shadow-{shadow}" if shadow in ["xs", "sm", "md", "lg", "xl", "2xl", "inner", "none"] else "shadow-md"
        rules.extend(create_base_rules("card", [
            ("box-shadow", token(shadow_token)),
        ]))
        
        # Border radius
        radius_token = f"radius-{border_radius}" if border_radius in ["none", "sm", "md", "lg", "xl", "2xl", "full"] else "radius-xl"
        rules.extend(create_base_rules("card", [
            ("border-radius", token(radius_token)),
        ]))
        
        return rules
    
    def resolve_divider(
        self,
        orientation: str = "horizontal",
        color: str | None = None,
    ) -> list[StyleRule]:
        """Resolve Divider component styles."""
        rules: list[StyleRule] = []
        
        # Base divider
        rules.extend(create_base_rules("divider", [
            ("background-color", color or token("color-border")),
            ("border", "none"),
        ]))
        
        if orientation == "horizontal":
            rules.extend(create_base_rules("divider", [
                ("width", "100%"),
                ("height", "1px"),
            ]))
        else:
            rules.extend(create_base_rules("divider", [
                ("height", "100%"),
                ("width", "1px"),
            ]))
        
        return rules
