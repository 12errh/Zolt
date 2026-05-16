"""
ZoltCSS Token System — The Design System Foundation

Every visual value in the entire framework lives in one place.
No raw hex codes, pixel values, or font strings appear anywhere else.

This is the v1.5 token system as specified in the PRD.
"""

from __future__ import annotations

# ── Color Palette ─────────────────────────────────────────────────────────────
# Semantic names — not "blue-500", but "primary", "danger", "text"

TOKENS: dict[str, str] = {
    # Semantic colors
    "color-primary": "#6C63FF",
    "color-primary-hover": "#5A52E0",
    "color-primary-active": "#4840CC",
    "color-primary-fg": "#FFFFFF",  # foreground (text) on primary bg
    "color-primary-subtle": "#EEF2FF",  # very light primary tint
    
    "color-secondary": "#F3F4F6",
    "color-secondary-hover": "#E5E7EB",
    "color-secondary-fg": "#111827",
    
    "color-bg": "#FFFFFF",
    "color-surface": "#F9FAFB",
    "color-surface-2": "#F3F4F6",
    "color-surface-3": "#E5E7EB",
    
    "color-border": "#E5E7EB",
    "color-border-strong": "#D1D5DB",
    
    "color-text": "#111827",
    "color-text-muted": "#6B7280",
    "color-text-inverse": "#FFFFFF",
    "color-text-disabled": "#9CA3AF",
    
    "color-success": "#10B981",
    "color-success-hover": "#059669",
    "color-success-fg": "#FFFFFF",
    "color-success-subtle": "#ECFDF5",
    
    "color-warning": "#F59E0B",
    "color-warning-hover": "#D97706",
    "color-warning-fg": "#FFFFFF",
    "color-warning-subtle": "#FFFBEB",
    
    "color-danger": "#EF4444",
    "color-danger-hover": "#DC2626",
    "color-danger-fg": "#FFFFFF",
    "color-danger-subtle": "#FEF2F2",
    
    "color-info": "#3B82F6",
    "color-info-hover": "#2563EB",
    "color-info-fg": "#FFFFFF",
    "color-info-subtle": "#EFF6FF",
    
    # Typography
    "font-family": "Inter, system-ui, -apple-system, sans-serif",
    "font-family-mono": "JetBrains Mono, Fira Code, monospace",
    
    "font-size-xs": "12px",
    "font-size-sm": "14px",
    "font-size-md": "16px",
    "font-size-lg": "18px",
    "font-size-xl": "20px",
    "font-size-2xl": "24px",
    "font-size-3xl": "30px",
    "font-size-4xl": "36px",
    "font-size-5xl": "48px",
    "font-size-6xl": "60px",
    
    "font-weight-normal": "400",
    "font-weight-medium": "500",
    "font-weight-semibold": "600",
    "font-weight-bold": "700",
    "font-weight-black": "900",
    
    "line-height-tight": "1.25",
    "line-height-normal": "1.5",
    "line-height-relaxed": "1.75",
    
    "letter-spacing-tight": "-0.025em",
    "letter-spacing-normal": "0",
    "letter-spacing-wide": "0.025em",
    "letter-spacing-wider": "0.05em",
    
    # Spacing (8px base grid)
    "space-0": "0",
    "space-1": "4px",
    "space-2": "8px",
    "space-3": "12px",
    "space-4": "16px",
    "space-5": "20px",
    "space-6": "24px",
    "space-8": "32px",
    "space-10": "40px",
    "space-12": "48px",
    "space-16": "64px",
    "space-20": "80px",
    "space-24": "96px",
    
    # Shape / Border Radius
    "radius-none": "0",
    "radius-sm": "4px",
    "radius-md": "8px",
    "radius-lg": "12px",
    "radius-xl": "16px",
    "radius-2xl": "24px",
    "radius-full": "9999px",
    
    # Shadows
    "shadow-xs": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "shadow-sm": "0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)",
    "shadow-md": "0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06)",
    "shadow-lg": "0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)",
    "shadow-xl": "0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)",
    "shadow-2xl": "0 25px 50px rgba(0, 0, 0, 0.25)",
    "shadow-inner": "inset 0 2px 4px rgba(0, 0, 0, 0.06)",
    "shadow-none": "none",
    
    # Transitions
    "transition-fast": "100ms ease",
    "transition-normal": "200ms ease",
    "transition-slow": "300ms ease",
    "transition-duration": "200ms",
    "transition-timing": "ease",
    
    # Breakpoints (for responsive system)
    "breakpoint-sm": "640px",
    "breakpoint-md": "768px",
    "breakpoint-lg": "1024px",
    "breakpoint-xl": "1280px",
    "breakpoint-2xl": "1536px",
    
    # Z-index scale
    "z-index-hide": "-1",
    "z-index-auto": "auto",
    "z-index-base": "0",
    "z-index-dropdown": "1000",
    "z-index-sticky": "1100",
    "z-index-fixed": "1200",
    "z-index-modal-backdrop": "1300",
    "z-index-modal": "1400",
    "z-index-popover": "1500",
    "z-index-tooltip": "1600",
    "z-index-toast": "1700",
}

# ── Built-in Theme Overrides ─────────────────────────────────────────────────

DARK_OVERRIDES: dict[str, str] = {
    "color-primary": "#7C73FF",
    "color-primary-hover": "#6A61F0",
    "color-primary-active": "#5A52E0",
    "color-primary-subtle": "#1E1B4B",
    
    "color-bg": "#0F172A",
    "color-surface": "#1E293B",
    "color-surface-2": "#334155",
    "color-surface-3": "#475569",
    
    "color-border": "#334155",
    "color-border-strong": "#475569",
    
    "color-text": "#F1F5F9",
    "color-text-muted": "#94A3B8",
    "color-text-inverse": "#0F172A",
    "color-text-disabled": "#64748B",
    
    "color-secondary": "#1E293B",
    "color-secondary-hover": "#334155",
    "color-secondary-fg": "#F1F5F9",
    
    "color-success-subtle": "#064E3B",
    "color-warning-subtle": "#78350F",
    "color-danger-subtle": "#7F1D1D",
    "color-info-subtle": "#1E3A8A",
}

OCEAN_OVERRIDES: dict[str, str] = {
    "color-primary": "#0EA5E9",
    "color-primary-hover": "#0284C7",
    "color-primary-active": "#0369A1",
    "color-primary-subtle": "#E0F2FE",
    
    "color-bg": "#F0F9FF",
    "color-surface": "#E0F2FE",
    "color-surface-2": "#BAE6FD",
    "color-surface-3": "#7DD3FC",
    
    "color-border": "#BAE6FD",
    "color-border-strong": "#7DD3FC",
    
    "color-text": "#0C4A6E",
    "color-text-muted": "#0369A1",
    
    "color-secondary": "#E0F2FE",
    "color-secondary-hover": "#BAE6FD",
    "color-secondary-fg": "#0C4A6E",
}

SUNSET_OVERRIDES: dict[str, str] = {
    "color-primary": "#F97316",
    "color-primary-hover": "#EA580C",
    "color-primary-active": "#C2410C",
    "color-primary-subtle": "#FFF7ED",
    
    "color-bg": "#FFF7ED",
    "color-surface": "#FFEDD5",
    "color-surface-2": "#FED7AA",
    "color-surface-3": "#FDBA74",
    
    "color-border": "#FDBA74",
    "color-border-strong": "#FB923C",
    
    "color-text": "#431407",
    "color-text-muted": "#9A3412",
    
    "color-secondary": "#FFEDD5",
    "color-secondary-hover": "#FED7AA",
    "color-secondary-fg": "#431407",
}

FOREST_OVERRIDES: dict[str, str] = {
    "color-primary": "#10B981",
    "color-primary-hover": "#059669",
    "color-primary-active": "#047857",
    "color-primary-subtle": "#ECFDF5",
    
    "color-bg": "#F0FDF4",
    "color-surface": "#DCFCE7",
    "color-surface-2": "#BBF7D0",
    "color-surface-3": "#86EFAC",
    
    "color-border": "#86EFAC",
    "color-border-strong": "#4ADE80",
    
    "color-text": "#052E16",
    "color-text-muted": "#166534",
    
    "color-secondary": "#DCFCE7",
    "color-secondary-hover": "#BBF7D0",
    "color-secondary-fg": "#052E16",
}

ROSE_OVERRIDES: dict[str, str] = {
    "color-primary": "#F43F5E",
    "color-primary-hover": "#E11D48",
    "color-primary-active": "#BE123C",
    "color-primary-subtle": "#FFF1F2",
    
    "color-bg": "#FFF1F2",
    "color-surface": "#FFE4E6",
    "color-surface-2": "#FECDD3",
    "color-surface-3": "#FDA4AF",
    
    "color-border": "#FDA4AF",
    "color-border-strong": "#FB7185",
    
    "color-text": "#4C0519",
    "color-text-muted": "#9F1239",
    
    "color-secondary": "#FFE4E6",
    "color-secondary-hover": "#FECDD3",
    "color-secondary-fg": "#4C0519",
}

MIDNIGHT_OVERRIDES: dict[str, str] = {
    "color-primary": "#8B5CF6",
    "color-primary-hover": "#7C3AED",
    "color-primary-active": "#6D28D9",
    "color-primary-subtle": "#1E1B4B",
    
    "color-bg": "#0F172A",
    "color-surface": "#1E293B",
    "color-surface-2": "#334155",
    "color-surface-3": "#475569",
    
    "color-border": "#475569",
    "color-border-strong": "#64748B",
    
    "color-text": "#F8FAFC",
    "color-text-muted": "#94A3B8",
    
    "color-secondary": "#334155",
    "color-secondary-hover": "#475569",
    "color-secondary-fg": "#F8FAFC",
}

SAND_OVERRIDES: dict[str, str] = {
    "color-primary": "#D97706",
    "color-primary-hover": "#B45309",
    "color-primary-active": "#92400E",
    "color-primary-subtle": "#FFFBEB",
    
    "color-bg": "#FFFBEB",
    "color-surface": "#FEF3C7",
    "color-surface-2": "#FDE68A",
    "color-surface-3": "#FCD34D",
    
    "color-border": "#FCD34D",
    "color-border-strong": "#FBBF24",
    
    "color-text": "#451a03",
    "color-text-muted": "#92400E",
    
    "color-secondary": "#FEF3C7",
    "color-secondary-hover": "#FDE68A",
    "color-secondary-fg": "#451a03",
}

MONO_OVERRIDES: dict[str, str] = {
    "color-primary": "#171717",
    "color-primary-hover": "#262626",
    "color-primary-active": "#404040",
    "color-primary-subtle": "#F5F5F5",
    
    "color-bg": "#FFFFFF",
    "color-surface": "#FAFAFA",
    "color-surface-2": "#F5F5F5",
    "color-surface-3": "#E5E5E5",
    
    "color-border": "#E5E5E5",
    "color-border-strong": "#D4D4D4",
    
    "color-text": "#171717",
    "color-text-muted": "#737373",
    
    "color-secondary": "#F5F5F5",
    "color-secondary-hover": "#E5E5E5",
    "color-secondary-fg": "#171717",
}

BUILT_IN_THEMES: dict[str, dict[str, str]] = {
    "light": {},
    "dark": DARK_OVERRIDES,
    "ocean": OCEAN_OVERRIDES,
    "sunset": SUNSET_OVERRIDES,
    "forest": FOREST_OVERRIDES,
    "rose": ROSE_OVERRIDES,
    "midnight": MIDNIGHT_OVERRIDES,
    "sand": SAND_OVERRIDES,
    "mono": MONO_OVERRIDES,
}
