"""
ZoltCSS Design Tokens — The complete design system foundation.

All visual values in the framework live here. No raw hex codes, pixel values,
or font strings appear anywhere else in the codebase.

Token naming convention: dash-separated for CSS compatibility
  Example: "color-primary", "space-4", "font-size-xl"
"""

from __future__ import annotations


# ── Color Palette ─────────────────────────────────────────────────────────────
# Semantic names — not "blue-500", but "primary", "danger", "text"

COLORS = {
    # Primary brand color
    "color-primary": "#6C63FF",
    "color-primary-hover": "#5A52E0",
    "color-primary-active": "#4840CC",
    "color-primary-fg": "#FFFFFF",  # foreground (text) on primary bg
    "color-primary-subtle": "#EEF2FF",  # very light primary tint
    
    # Secondary
    "color-secondary": "#F3F4F6",
    "color-secondary-hover": "#E5E7EB",
    "color-secondary-fg": "#111827",
    
    # Backgrounds
    "color-bg": "#FFFFFF",
    "color-surface": "#F9FAFB",
    "color-surface-2": "#F3F4F6",
    "color-surface-3": "#E5E7EB",
    
    # Borders
    "color-border": "#E5E7EB",
    "color-border-strong": "#D1D5DB",
    
    # Text
    "color-text": "#111827",
    "color-text-muted": "#6B7280",
    "color-text-inverse": "#FFFFFF",
    
    # Semantic colors
    "color-success": "#10B981",
    "color-success-hover": "#059669",
    "color-success-fg": "#FFFFFF",
    
    "color-warning": "#F59E0B",
    "color-warning-hover": "#D97706",
    "color-warning-fg": "#FFFFFF",
    
    "color-danger": "#EF4444",
    "color-danger-hover": "#DC2626",
    "color-danger-fg": "#FFFFFF",
    
    "color-info": "#3B82F6",
    "color-info-hover": "#2563EB",
    "color-info-fg": "#FFFFFF",
}

# ── Typography ────────────────────────────────────────────────────────────────

TYPOGRAPHY = {
    "font-family": "Inter, system-ui, -apple-system, sans-serif",
    "font-family-mono": "JetBrains Mono, Fira Code, monospace",
    
    # Font sizes (using rem for accessibility)
    "font-size-xs": "0.75rem",     # 12px
    "font-size-sm": "0.875rem",    # 14px
    "font-size-base": "1rem",      # 16px
    "font-size-lg": "1.125rem",    # 18px
    "font-size-xl": "1.25rem",     # 20px
    "font-size-2xl": "1.5rem",     # 24px
    "font-size-3xl": "1.875rem",   # 30px
    "font-size-4xl": "2.25rem",    # 36px
    "font-size-5xl": "3rem",       # 48px
    
    # Font weights
    "font-weight-normal": "400",
    "font-weight-medium": "500",
    "font-weight-semibold": "600",
    "font-weight-bold": "700",
    
    # Line heights
    "line-height-tight": "1.25",
    "line-height-normal": "1.5",
    "line-height-relaxed": "1.75",
    
    # Letter spacing
    "letter-spacing-tight": "-0.025em",
    "letter-spacing-normal": "0",
    "letter-spacing-wide": "0.025em",
}

# ── Spacing (8px base grid) ───────────────────────────────────────────────────

SPACING = {
    "space-0": "0",
    "space-1": "0.25rem",   # 4px
    "space-2": "0.5rem",    # 8px
    "space-3": "0.75rem",   # 12px
    "space-4": "1rem",      # 16px
    "space-5": "1.25rem",   # 20px
    "space-6": "1.5rem",    # 24px
    "space-8": "2rem",      # 32px
    "space-10": "2.5rem",   # 40px
    "space-12": "3rem",     # 48px
    "space-16": "4rem",     # 64px
    "space-20": "5rem",     # 80px
    "space-24": "6rem",     # 96px
}

# ── Shape (Border Radius) ─────────────────────────────────────────────────────

RADIUS = {
    "radius-none": "0",
    "radius-sm": "0.25rem",    # 4px
    "radius-md": "0.5rem",     # 8px
    "radius-lg": "0.75rem",    # 12px
    "radius-xl": "1rem",       # 16px
    "radius-2xl": "1.5rem",    # 24px
    "radius-full": "9999px",
}

# ── Shadow ────────────────────────────────────────────────────────────────────

SHADOWS = {
    "shadow-none": "none",
    "shadow-sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "shadow-md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "shadow-lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "shadow-xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "shadow-2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    "shadow-inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
}

# ── Animation & Transitions ───────────────────────────────────────────────────

TRANSITIONS = {
    "transition-fast": "100ms ease",
    "transition-normal": "200ms ease",
    "transition-slow": "300ms ease",
    "transition-very-slow": "500ms ease",
}

EASING = {
    "ease-linear": "linear",
    "ease-in": "cubic-bezier(0.4, 0, 1, 1)",
    "ease-out": "cubic-bezier(0, 0, 0.2, 1)",
    "ease-in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
    "ease-bounce": "cubic-bezier(0.34, 1.56, 0.64, 1)",
}

# ── Breakpoints (Responsive) ──────────────────────────────────────────────────

BREAKPOINTS = {
    "breakpoint-sm": "640px",
    "breakpoint-md": "768px",
    "breakpoint-lg": "1024px",
    "breakpoint-xl": "1280px",
    "breakpoint-2xl": "1536px",
}

# Media query strings for use in StyleRule
MEDIA_QUERIES = {
    "sm": "@media (min-width: 640px)",
    "md": "@media (min-width: 768px)",
    "lg": "@media (min-width: 1024px)",
    "xl": "@media (min-width: 1280px)",
    "2xl": "@media (min-width: 1536px)",
}

# ── Z-Index Scale ─────────────────────────────────────────────────────────────

Z_INDEX = {
    "z-0": "0",
    "z-10": "10",
    "z-20": "20",
    "z-30": "30",
    "z-40": "40",
    "z-50": "50",
    "z-auto": "auto",
}

# ── Container Sizes ───────────────────────────────────────────────────────────

CONTAINERS = {
    "container-sm": "640px",
    "container-md": "768px",
    "container-lg": "1024px",
    "container-xl": "1280px",
    "container-2xl": "1536px",
    "container-full": "100%",
}

# ── Opacity ───────────────────────────────────────────────────────────────────

OPACITY = {
    "opacity-0": "0",
    "opacity-25": "0.25",
    "opacity-50": "0.5",
    "opacity-75": "0.75",
    "opacity-100": "1",
}

# ── Combine all tokens ────────────────────────────────────────────────────────

TOKENS: dict[str, str] = {
    **COLORS,
    **TYPOGRAPHY,
    **SPACING,
    **RADIUS,
    **SHADOWS,
    **TRANSITIONS,
    **EASING,
    **BREAKPOINTS,
    **Z_INDEX,
    **CONTAINERS,
    **OPACITY,
}

# ── Dark Mode Token Overrides ─────────────────────────────────────────────────

DARK_COLORS = {
    "color-primary": "#7C73FF",
    "color-primary-hover": "#6A61F0",
    "color-primary-active": "#5850E0",
    
    "color-secondary": "#1E293B",
    "color-secondary-hover": "#334155",
    "color-secondary-fg": "#F1F5F9",
    
    "color-bg": "#0F172A",
    "color-surface": "#1E293B",
    "color-surface-2": "#334155",
    "color-surface-3": "#475569",
    
    "color-border": "#334155",
    "color-border-strong": "#475569",
    
    "color-text": "#F1F5F9",
    "color-text-muted": "#94A3B8",
    "color-text-inverse": "#0F172A",
}

DARK_TOKENS: dict[str, str] = {**DARK_COLORS}

# ── Built-in Themes ───────────────────────────────────────────────────────────

OCEAN_COLORS = {
    "color-primary": "#0EA5E9",
    "color-primary-hover": "#0284C7",
    "color-bg": "#F0F9FF",
    "color-surface": "#E0F2FE",
    "color-text": "#0C4A6E",
    "color-text-muted": "#0369A1",
    "color-border": "#BAE6FD",
}

SUNSET_COLORS = {
    "color-primary": "#F97316",
    "color-primary-hover": "#EA580C",
    "color-bg": "#FFF7ED",
    "color-surface": "#FFEDD5",
    "color-text": "#431407",
    "color-text-muted": "#9A3412",
    "color-border": "#FDBA74",
}

FOREST_COLORS = {
    "color-primary": "#10B981",
    "color-primary-hover": "#059669",
    "color-bg": "#F0FDF4",
    "color-surface": "#DCFCE7",
    "color-text": "#052E16",
    "color-text-muted": "#166534",
    "color-border": "#86EFAC",
}

ROSE_COLORS = {
    "color-primary": "#F43F5E",
    "color-primary-hover": "#E11D48",
    "color-bg": "#FFF1F2",
    "color-surface": "#FFE4E6",
    "color-text": "#4C0519",
    "color-text-muted": "#9F1239",
    "color-border": "#FECDD3",
}

AMETHYST_COLORS = {
    "color-primary": "#A855F7",
    "color-primary-hover": "#9333EA",
    "color-bg": "#FAF5FF",
    "color-surface": "#F3E8FF",
    "color-text": "#581C87",
    "color-text-muted": "#9333EA",
    "color-border": "#E9D5FF",
}

SLATE_COLORS = {
    "color-primary": "#475569",
    "color-primary-hover": "#334155",
    "color-bg": "#F8FAFC",
    "color-surface": "#F1F5F9",
    "color-text": "#1E293B",
    "color-text-muted": "#64748B",
    "color-border": "#CBD5E1",
}

BUILT_IN_THEMES: dict[str, dict[str, str]] = {
    "light": {},
    "dark": DARK_COLORS,
    "ocean": OCEAN_COLORS,
    "sunset": SUNSET_COLORS,
    "forest": FOREST_COLORS,
    "rose": ROSE_COLORS,
    "amethyst": AMETHYST_COLORS,
    "slate": SLATE_COLORS,
}

# ── Token Metadata (for documentation & tooling) ──────────────────────────────

TOKEN_CATEGORIES = {
    "color": "Colors",
    "font": "Typography",
    "space": "Spacing",
    "radius": "Border Radius",
    "shadow": "Shadows",
    "transition": "Transitions",
    "ease": "Easing",
    "breakpoint": "Breakpoints",
    "z": "Z-Index",
    "container": "Container Sizes",
    "opacity": "Opacity",
}
