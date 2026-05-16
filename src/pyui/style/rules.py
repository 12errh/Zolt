"""
ZoltCSS Style Rules — The fundamental building block of the styling system.

StyleRule is a dataclass that represents a single CSS property declaration,
with optional modifiers for pseudo-classes, states, media queries, and component scope.

This abstraction allows the same style definition to be rendered as:
- CSS for web
- QSS for Qt desktop
- Rich Style objects for CLI
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pyui.style.tokens import TOKENS


@dataclass(frozen=True)
class StyleRule:
    """
    A single CSS property declaration with optional modifiers.
    
    Attributes
    ----------
    prop : str
        The CSS property name (e.g., "background-color", "font-size")
    value : str
        The CSS value (e.g., "var(--z-color-primary)", "1rem")
    pseudo : str | None
        CSS pseudo-class (":hover", ":focus", ":focus-visible", ":active", etc.)
    state : str | None
        Component state ("disabled", "active", "selected", etc.)
    media : str | None
        Media query ("@media (min-width: 768px)", etc.)
    component : str | None
        Component scope for namespacing (e.g., "Button", "Card")
    important : bool
        Whether to add !important flag
    """
    prop: str
    value: str
    pseudo: Optional[str] = None
    state: Optional[str] = None
    media: Optional[str] = None
    component: Optional[str] = None
    important: bool = False
    
    def render_css(self, selector: str = ".element") -> str:
        """
        Render this rule as a CSS declaration.
        
        Examples
        --------
        >>> rule = StyleRule("color", "var(--z-text)")
        >>> rule.render_css(".btn")
        '.btn { color: var(--z-text); }'
        
        >>> rule = StyleRule("bg", "var(--z-primary)", pseudo=":hover")
        >>> rule.render_css(".btn")
        '.btn:hover { background-color: var(--z-primary); }'
        """
        # Convert shorthand prop to full CSS property
        css_prop = _prop_to_css(self.prop)
        
        # Add !important if needed
        value = self.value
        if self.important:
            value = f"{value} !important"
        
        # Build selector with pseudo-class
        full_selector = selector
        if self.pseudo:
            full_selector = f"{selector}{self.pseudo}"
        
        return f"{full_selector} {{ {css_prop}: {value}; }}"
    
    def render_qss(self, selector: str = "QWidget") -> str:
        """
        Render this rule as Qt Style Sheet (QSS) declaration.
        
        QSS is similar to CSS but has some differences in property names
        and supported features.
        """
        qss_prop = _prop_to_qss(self.prop)
        
        value = self.value
        if self.important:
            value = f"{value} !important"
        
        full_selector = selector
        if self.pseudo:
            # QSS uses different pseudo-class syntax
            qss_pseudo = _css_to_qss_pseudo(self.pseudo)
            full_selector = f"{selector}{qss_pseudo}"
        
        if self.state:
            # QSS state selectors like :disabled
            full_selector = f"{selector}[{self.state}=\"true\"]"
        
        return f"{full_selector} {{ {qss_prop}: {value}; }}"
    
    @property
    def key(self) -> tuple:
        """
        Generate a unique key for deduplication.
        
        Two rules are considered identical if they have the same
        prop, value, pseudo, state, and media query.
        """
        return (self.prop, self.value, self.pseudo, self.state, self.media)
    
    def with_media(self, breakpoint: str) -> StyleRule:
        """
        Return a new rule wrapped in a media query.
        
        Parameters
        ----------
        breakpoint : str
            Breakpoint name ("sm", "md", "lg", "xl", "2xl")
            
        Returns
        -------
        StyleRule
            New rule with media query set
        """
        from zolt.style.tokens import MEDIA_QUERIES
        
        media = MEDIA_QUERIES.get(breakpoint)
        if not media:
            raise ValueError(f"Unknown breakpoint: {breakpoint}")
        
        return StyleRule(
            prop=self.prop,
            value=self.value,
            pseudo=self.pseudo,
            state=self.state,
            media=media,
            component=self.component,
            important=self.important,
        )
    
    def with_important(self) -> StyleRule:
        """Return a new rule with !important flag."""
        return StyleRule(
            prop=self.prop,
            value=self.value,
            pseudo=self.pseudo,
            state=self.state,
            media=self.media,
            component=self.component,
            important=True,
        )


def token(name: str) -> str:
    """
    Look up a token value by name.
    
    Parameters
    ----------
    name : str
        Token name (e.g., "color-primary", "space-4")
        
    Returns
    -------
    str
        Token value formatted as CSS variable reference
        
    Raises
    ------
    KeyError
        If token name not found
        
    Examples
    --------
    >>> token("color-primary")
    'var(--z-color-primary)'
    
    >>> token("space-4")
    'var(--z-space-4)'
    """
    if name not in TOKENS:
        raise KeyError(f"Token '{name}' not found. Available tokens: {list(TOKENS.keys())[:10]}...")
    
    # Convert token name to CSS variable format
    var_name = f"--z-{name}"
    return f"var({var_name})"


def _prop_to_css(prop: str) -> str:
    """Convert shorthand property name to full CSS property."""
    mapping = {
        "bg": "background-color",
        "fg": "color",
        "color": "color",
        "size": "font-size",
        "weight": "font-weight",
        "family": "font-family",
        "gap": "gap",
        "p": "padding",
        "px": "padding-left",
        "py": "padding-top",
        "pt": "padding-top",
        "pr": "padding-right",
        "pb": "padding-bottom",
        "pl": "padding-left",
        "m": "margin",
        "mx": "margin-left",
        "my": "margin-top",
        "mt": "margin-top",
        "mr": "margin-right",
        "mb": "margin-bottom",
        "ml": "margin-left",
        "w": "width",
        "h": "height",
        "min-w": "min-width",
        "min-h": "min-height",
        "max-w": "max-width",
        "max-h": "max-height",
        "radius": "border-radius",
        "border": "border",
        "border-color": "border-color",
        "border-width": "border-width",
        "shadow": "box-shadow",
        "opacity": "opacity",
        "display": "display",
        "direction": "flex-direction",
        "align": "align-items",
        "justify": "justify-content",
        "wrap": "flex-wrap",
        "position": "position",
        "top": "top",
        "right": "right",
        "bottom": "bottom",
        "left": "left",
        "z": "z-index",
        "overflow": "overflow",
        "cursor": "cursor",
        "transition": "transition",
        "transform": "transform",
        "text-align": "text-align",
        "text-decoration": "text-decoration",
        "line-height": "line-height",
        "letter-spacing": "letter-spacing",
        "white-space": "white-space",
        "word-break": "word-break",
    }
    return mapping.get(prop, prop)


def _prop_to_qss(prop: str) -> str:
    """Convert shorthand property name to QSS property."""
    # Most CSS properties work in QSS, but some have different names
    mapping = {
        "bg": "background-color",
        "fg": "color",
        "color": "color",
        "size": "font-size",
        "weight": "font-weight",
        "family": "font-family",
        "gap": "spacing",  # QSS uses 'spacing' for layouts
        "radius": "border-radius",
        "border": "border",
        "shadow": "",  # QSS doesn't support box-shadow well
        "opacity": "opacity",
        "display": "display",
        "w": "width",
        "h": "height",
        "min-w": "min-width",
        "min-h": "min-height",
        "max-w": "max-width",
        "max-h": "max-height",
        "p": "padding",
        "m": "margin",
        "position": "position",
        "top": "top",
        "right": "right",
        "bottom": "bottom",
        "left": "left",
        "z": "z-index",
        "overflow": "overflow",
        "cursor": "cursor",
        "text-align": "text-align",
    }
    return mapping.get(prop, prop)


def _css_to_qss_pseudo(pseudo: str) -> str:
    """Convert CSS pseudo-class to QSS equivalent."""
    mapping = {
        ":hover": ":hover",
        ":focus": ":focus",
        ":active": ":pressed",
        ":disabled": ":disabled",
        ":checked": ":checked",
        ":selected": ":selected",
    }
    return mapping.get(pseudo, pseudo)


# Type alias for list of rules
StyleRules = list[StyleRule]
