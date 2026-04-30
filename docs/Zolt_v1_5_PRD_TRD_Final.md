# Zolt v1.5 — "Production UI" Release
## Product & Technical Requirements Document — Final

**Framework:** Zolt (formerly PyUI)
**Version:** 1.5.0
**Status:** Active Development Planning
**Prerequisite:** Zolt v1.0 complete (Phase 1 done, framework live on PyPI)
**Author:** Zolt Core Team
**Last Updated:** April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What v1.0 Got Right & What It Lacks](#2-what-v10-got-right--what-it-lacks)
3. [The Build Order Principle — Why Sequence Matters](#3-the-build-order-principle)
4. [Product Requirements (PRD)](#4-product-requirements-prd)
5. [Technical Requirements (TRD)](#5-technical-requirements-trd)
   - 5.1 Full Architecture — Layers Built in Order
   - 5.2 Layer 1: ZoltCSS — The Design System Engine
   - 5.3 Layer 2: JS Bundler — zolt-bundler
   - 5.4 Layer 3: Animation Engine
   - 5.5 Layer 4: 3D Engine
   - 5.6 Layer 5: Zolt UI — Prebuilt Component Library
   - 5.7 Layer 6: Design Import System
   - 5.8 Layer 7: Desktop v1.5 (Qt5 + Qt6 + WebEngine)
   - 5.9 Layer 8: CLI Renderer Upgrade
   - 5.10 Layer 9: AI-First Architecture & Skill Files
   - 5.11 Performance Requirements
   - 5.12 Accessibility Requirements
6. [API Design — Full Reference](#6-api-design--full-reference)
7. [Development Phases](#7-development-phases)
8. [Unit Test Plan — Per Phase](#8-unit-test-plan--per-phase)
9. [AI Skills System — Full Specification](#9-ai-skills-system--full-specification)
10. [Docs Website Specification](#10-docs-website-specification)
11. [Demo Artifacts Specification](#11-demo-artifacts-specification)
12. [File & Folder Structure v1.5](#12-file--folder-structure-v15)
13. [Dependencies & Versions](#13-dependencies--versions)
14. [Migration Guide — v1.0 → v1.5](#14-migration-guide--v10--v15)
15. [Risks & Mitigations](#15-risks--mitigations)
16. [Glossary](#16-glossary)

---

## 1. Executive Summary

Zolt v1.5 is the "Production UI" release. V1.0 proved that Python can compile to UI. V1.5 makes that output genuinely world-class — animated, 3D-capable, beautifully styled by default, and independent of any external CSS framework.

The most important architectural change in v1.5 is one that is invisible to the user but fundamental to everything: **Zolt replaces its Tailwind CSS dependency with ZoltCSS — its own purpose-built styling engine**. This is not cosmetic. It is the foundation that every other v1.5 feature sits on. It is built first, before anything else, because if we build animations, 3D, and 80 prebuilt components on top of Tailwind and then replace it later, we rewrite everything twice.

**The seven pillars of v1.5, in build order:**

1. **ZoltCSS** — Zolt's own styling engine. Zero Tailwind. Zero CDN. Every visual property expressed as a Python method. One style declaration produces correct output for web, Qt desktop, and terminal.
2. **JS Bundler** — `zolt-bundler` manages GSAP, Three.js, and Alpine.js as local assets. No CDN. No npm commands for the user.
3. **Animation Engine** — GSAP-powered, declared in pure Python. Scroll-triggered, timeline, page transitions, micro-interactions.
4. **3D Engine** — Three.js scenes, Spline embeds, particle systems, GLTF models — all from Python.
5. **Zolt UI** — 80+ production-grade prebuilt components built on ZoltCSS, styled beautifully by default.
6. **Design Import** — `zolt import figma <url>` converts Figma, Framer, and Webflow designs to Zolt Python code.
7. **AI-First** — Skill files, `zolt.schema.json`, and `LLMS.txt` make Zolt writable by Claude Code and any AI agent on the first attempt.

**Deliverables at launch:**
- `zolt-framework==1.5.0` on PyPI
- `zolt-ui==1.5.0` on PyPI (80+ components)
- `zolt.dev` — complete docs website, built entirely with Zolt, deployed on Vercel
- `ZoltDemo.exe` / `.app` / `.deb` — desktop showcase app
- `zolt demo` — interactive CLI showcase command
- Skill files for 100% of public API surface

---

## 2. What v1.0 Got Right & What It Lacks

### What works in v1.0

- Python class-based UI API is clean and correct
- Compiler pipeline (class tree → IR → HTML) is solid and fast
- Reactive state system is correctly implemented
- Hot reload works under 200ms
- Basic component library covers layout and content
- Theme token system concept is right

### What is broken or missing

| Problem | Impact | Root cause |
|---|---|---|
| Styling depends entirely on Tailwind CSS | Framework is not independent; CDN kills production apps; can't style Qt or CLI with same system | Wrong architecture — must fix before anything else |
| Tailwind loaded from CDN | App breaks if CDN offline; 3MB unused CSS loads on every page | Architecture |
| No animations | Output looks static, unprofessional | Not implemented |
| No 3D support | Cannot build modern marketing sites | Not implemented |
| No prebuilt components | Every developer starts from zero | Backlogged |
| No design import | Gap between Figma design and Zolt code | Not implemented |
| Qt5 not supported | Linux users and older hardware locked out | Qt6 only |
| No AI skill files | Agents hallucinate APIs, generate wrong code | Not implemented |
| Docs insufficient | Adoption blocked | Resource constraint |
| No showcase demos | Hard to demonstrate capability | Not built |

---

## 3. The Build Order Principle

> **The most expensive mistake in framework development is building features on a broken foundation and then replacing the foundation later.**

In the old v1.5 plan, the phases were: build system → animation → 3D → components → AI. That order has a fatal flaw: if we build 80 Zolt UI components that use Tailwind class strings, and then replace Tailwind with ZoltCSS in a later phase, we rewrite all 80 components. Every animation helper that outputs Tailwind classes gets rewritten. Every docs example gets rewritten.

**The correct order is:**

```
ZoltCSS Engine          ← Foundation. Everything below depends on this.
     │
     ▼
JS Bundler              ← Foundation. Animations and 3D need bundled JS.
     │
     ▼
Animation Engine        ← Depends on: ZoltCSS (for animated element styling)
     │                                 JS Bundler (for GSAP)
     ▼
3D Engine               ← Depends on: ZoltCSS (canvas styling)
     │                                 JS Bundler (for Three.js)
     ▼
Zolt UI Components      ← Depends on: ZoltCSS (all visual styling)
     │                                 Animation Engine (entrance animations)
     ▼
Design Import           ← Depends on: Zolt UI (maps Figma nodes to components)
     │                                 ZoltCSS (colour/spacing extraction)
     ▼
Desktop Qt5/Qt6         ← Depends on: ZoltCSS (Qt style generator)
     │
     ▼
CLI Upgrade             ← Depends on: ZoltCSS (Rich style generator)
     │
     ▼
AI Skills & Schema      ← Depends on: Everything stable above
     │
     ▼
Docs Website            ← Depends on: Everything — it uses all features
     │
     ▼
Demo Artifacts          ← Depends on: Everything — it showcases all features
     │
     ▼
Production Hardening    ← Final pass before release
```

This is the order used in Section 7 (Development Phases). Building in this order means no feature ever gets rewritten due to a foundation change.

---

## 4. Product Requirements (PRD)

### 4.1 Problem Statement

Zolt v1.0 exists and runs. But the output is not competitive with what a professional frontend team produces. A developer evaluating Zolt today sees:

- No animations — pages look flat and static
- No 3D — cannot build modern hero sections
- A Tailwind dependency they didn't sign up for
- No prebuilt components — high time cost to style even a login page
- A build system that calls an external CDN (wrong for production)
- No path from their Figma design to Zolt code
- A styling API that leaks CSS vocabulary through `.className()`

V1.5 closes every gap. By the end of v1.5, a single Python developer using Zolt should be able to build a product website that wins Awwwards — in less time than it would take a React developer.

### 4.2 Vision & Goals

**Vision:** Any person — Python developer, designer, student, or AI agent — should be able to build a world-class production UI entirely in Python, with no knowledge of CSS, JavaScript, or any frontend tooling.

**Primary Goals:**

1. Own the entire styling pipeline — no third-party CSS framework, no CDN, no class names visible to the developer
2. Make the styling API the easiest and most expressive in any framework — simpler than Tailwind, more powerful than tkinter
3. Ship an animation system that produces output indistinguishable from sites built with Framer Motion
4. Ship a 3D system that enables Three.js-quality scenes from Python
5. Ship 80+ prebuilt components that look production-ready with zero customisation
6. Enable design import from Figma in a single CLI command
7. Make AI agents (Claude Code, Cursor) first-class users with skill files and schema

**Secondary Goals:**

- `prefers-reduced-motion` respected on all animations
- Dark mode automatic on all 80+ Zolt UI components
- Qt5 + Qt6 + Qt6 WebEngine all supported for desktop
- Textual-powered interactive CLI renderer
- `zolt eject` command outputs raw HTML/CSS/JS for teams that need to hand off

### 4.3 Target Users

All v1.0 users continue to work unchanged. V1.5 additionally targets:

**Designers who code** — Know Figma, write some Python, want to go directly from design to live app without a handoff step.

**Non-technical founders** — Use `zolt-ui` prebuilt components to assemble a full SaaS landing page without writing a single CSS property.

**AI coding agents** — Claude Code, Cursor, GitHub Copilot. Given a brief, they generate a complete production Zolt app that compiles and renders correctly on the first attempt, using skill files.

**Frontend developers evaluating Zolt** — Sceptical that Python can produce quality UI. The 3D support, Figma import, and animation quality is what changes their mind.

### 4.4 Success Metrics

| Metric | Target (6 months post-launch) |
|---|---|
| PyPI downloads (`zolt-framework`) | 100,000 / month |
| PyPI downloads (`zolt-ui`) | 40,000 / month |
| GitHub stars | 12,000 |
| CSS bundle size (gzip, typical app) | < 12KB |
| JS bundle size (gzip, no 3D) | < 90KB |
| First Contentful Paint (simulated 4G) | < 1.2s |
| Lighthouse Performance | > 90 |
| Lighthouse Accessibility | > 95 |
| AI agent first-attempt correctness | > 95% |
| Hot reload latency | < 200ms |
| Figma import accuracy | > 80% |
| `.exe` demo downloads (first month) | 5,000+ |

### 4.5 Non-Goals for v1.5

- React or Vue component interoperability (v2.0)
- Native iOS/Android apps (v2.0)
- Server-side rendering (v2.0)
- Full-stack backend (v2.0 — see Zolt v2.0 PRD)
- Visual drag-and-drop builder (v2.x)
- Figma plugin (export directly from Figma UI — v1.6)
- GraphQL API layer (v2.0)
- Zolt Cloud hosting (v2.0)

---

## 5. Technical Requirements (TRD)

### 5.1 Full Architecture — Layers Built in Order

```
┌──────────────────────────────────────────────────────────────────────┐
│                        User Python Code                               │
│                                                                       │
│  from zolt import App, Page, Flex, Heading, Button                   │
│  from zolt.animate import fade_in, stagger, Timeline                 │
│  from zolt.three import Scene3D, Torus, PointLight                   │
│  from zolt_ui import LoginPage, HeroSection, PricingTable            │
│                                                                       │
│  class MyApp(App):                                                    │
│      home = Page(title="Home")                                        │
│      home.add(                                                        │
│          Heading("Hello").color("text").size("5xl").weight("black"),  │
│          Button("Go").color("primary").size("lg").shadow("md")        │
│              .animate(slide_up(duration=0.5))                         │
│      )                                                                │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                ┌───────────────▼──────────────┐
                │       Zolt Compiler           │
                │  Class tree → IR Tree         │
                │  StyleRule collection         │
                │  AnimationNode resolution     │
                │  Scene3DNode serialisation    │
                └────┬──────────────┬───────────┘
                     │              │
      ┌──────────────▼──┐    ┌──────▼────────────────┐
      │  ZoltCSS Engine │    │    IR → Renderer       │
      │                 │    │                        │
      │  Token System   │    │  Web:     HTML         │
      │  Style Resolver │    │  Qt5/Qt6: QSS          │
      │  CSS Generator  │    │  CLI:     Rich Style   │
      │  QSS Generator  │    │                        │
      │  Rich Generator │    └──────────────────────┬─┘
      └────────┬────────┘                           │
               │                                    │
      ┌────────▼────────┐          ┌────────────────▼──────────┐
      │  zolt.min.css   │          │    zolt-bundler            │
      │  ~8KB gzipped   │          │    GSAP + Alpine + 3JS     │
      │  Zero Tailwind  │          │    → app.bundle.js         │
      │  Zero CDN       │          │    ~90KB–350KB gzipped     │
      └─────────────────┘          └───────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│              AI Compatibility Layer (horizontal across all)           │
│   zolt/skills/*.yaml  ·  zolt.schema.json  ·  LLMS.txt              │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 5.2 Layer 1: ZoltCSS — The Design System Engine

> **This is built first. Everything else — animations, 3D, Zolt UI — sits on top of it.**

ZoltCSS is Zolt's own styling engine. It replaces Tailwind entirely. No external CSS dependency. No class names visible to the developer. No CDN. The developer expresses all styling through Python methods; ZoltCSS compiles those methods to a single optimised CSS file at build time.

#### Why This Is Better Than Tailwind

| | Tailwind (v1.0) | ZoltCSS (v1.5) |
|---|---|---|
| CSS knowledge needed | Yes — must know utility names | None |
| API leakage | `className("bg-blue-500")` visible | `color("primary")` — zero CSS |
| Cross-target | Web only | Web + Qt + CLI from same declaration |
| Theme switching | Rebuild + Tailwind config | CSS variable swap, instant |
| Bundle size | Tailwind CLI required at build | Pure Python, no external tools |
| Ownership | Third-party | 100% owned by Zolt |
| Readability | `px-4 py-2 text-sm font-medium` | `.size("md")` — English |

#### 5.2.1 The Token System

Every visual value in the entire framework lives in one place. No raw hex codes, pixel values, or font strings appear anywhere else in the codebase.

```python
# zolt/style/tokens.py

TOKENS = {
    # ── Color Palette ─────────────────────────────────────────────────
    # Semantic names — not "blue-500", but "primary", "danger", "text"
    "color-primary":          "#6C63FF",
    "color-primary-hover":    "#5A52E0",
    "color-primary-active":   "#4840CC",
    "color-primary-fg":       "#FFFFFF",   # foreground (text) on primary bg
    "color-primary-subtle":   "#EEF2FF",   # very light primary tint

    "color-secondary":        "#F3F4F6",
    "color-secondary-hover":  "#E5E7EB",
    "color-secondary-fg":     "#111827",

    "color-bg":               "#FFFFFF",   # page background
    "color-surface":          "#F9FAFB",   # card / panel background
    "color-surface-2":        "#F3F4F6",   # nested surface
    "color-surface-3":        "#E5E7EB",   # deeply nested surface

    "color-border":           "#E5E7EB",
    "color-border-strong":    "#D1D5DB",

    "color-text":             "#111827",
    "color-text-muted":       "#6B7280",
    "color-text-subtle":      "#9CA3AF",
    "color-text-disabled":    "#D1D5DB",

    "color-success":          "#10B981",
    "color-success-fg":       "#FFFFFF",
    "color-success-subtle":   "#D1FAE5",
    "color-warning":          "#F59E0B",
    "color-warning-fg":       "#FFFFFF",
    "color-warning-subtle":   "#FEF3C7",
    "color-danger":           "#EF4444",
    "color-danger-fg":        "#FFFFFF",
    "color-danger-subtle":    "#FEE2E2",
    "color-info":             "#3B82F6",
    "color-info-fg":          "#FFFFFF",
    "color-info-subtle":      "#DBEAFE",

    # ── Spacing (4px base grid, 8px standard) ──────────────────────────
    "space-0":   "0px",    "space-px":  "1px",
    "space-0-5": "2px",    "space-1":   "4px",
    "space-1-5": "6px",    "space-2":   "8px",
    "space-2-5": "10px",   "space-3":   "12px",
    "space-3-5": "14px",   "space-4":   "16px",
    "space-5":   "20px",   "space-6":   "24px",
    "space-7":   "28px",   "space-8":   "32px",
    "space-9":   "36px",   "space-10":  "40px",
    "space-11":  "44px",   "space-12":  "48px",
    "space-14":  "56px",   "space-16":  "64px",
    "space-20":  "80px",   "space-24":  "96px",
    "space-28":  "112px",  "space-32":  "128px",
    "space-40":  "160px",  "space-48":  "192px",
    "space-56":  "224px",  "space-64":  "256px",

    # ── Typography ─────────────────────────────────────────────────────
    "font-sans":    "Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    "font-serif":   "Playfair Display, Georgia, 'Times New Roman', serif",
    "font-mono":    "JetBrains Mono, 'Fira Code', Menlo, monospace",
    "font-display": "'Cal Sans', 'Plus Jakarta Sans', Inter, sans-serif",

    "font-size-2xs":  "10px",  "font-size-xs":   "11px",
    "font-size-sm":   "13px",  "font-size-base":  "15px",
    "font-size-md":   "15px",  "font-size-lg":    "17px",
    "font-size-xl":   "20px",  "font-size-2xl":   "24px",
    "font-size-3xl":  "30px",  "font-size-4xl":   "36px",
    "font-size-5xl":  "48px",  "font-size-6xl":   "60px",
    "font-size-7xl":  "72px",  "font-size-8xl":   "96px",
    "font-size-9xl":  "128px",

    "font-weight-thin":       "100",  "font-weight-light":      "300",
    "font-weight-normal":     "400",  "font-weight-medium":     "500",
    "font-weight-semi":       "600",  "font-weight-bold":       "700",
    "font-weight-extra":      "800",  "font-weight-black":      "900",

    "line-height-none":     "1",      "line-height-tight":    "1.2",
    "line-height-snug":     "1.35",   "line-height-normal":   "1.5",
    "line-height-relaxed":  "1.65",   "line-height-loose":    "2",

    "letter-spacing-tight":  "-0.04em",  "letter-spacing-snug":   "-0.02em",
    "letter-spacing-normal":  "0em",     "letter-spacing-wide":    "0.025em",
    "letter-spacing-wider":   "0.08em",  "letter-spacing-widest":  "0.2em",

    # ── Border Radius ──────────────────────────────────────────────────
    "radius-none":  "0",       "radius-xs":   "2px",
    "radius-sm":    "4px",     "radius-md":   "8px",
    "radius-lg":    "12px",    "radius-xl":   "16px",
    "radius-2xl":   "20px",    "radius-3xl":  "24px",
    "radius-full":  "9999px",

    # ── Shadows ────────────────────────────────────────────────────────
    "shadow-none":  "none",
    "shadow-xs":   "0 1px 2px rgba(0,0,0,0.04)",
    "shadow-sm":   "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
    "shadow-md":   "0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04)",
    "shadow-lg":   "0 10px 15px rgba(0,0,0,0.06), 0 4px 6px rgba(0,0,0,0.03)",
    "shadow-xl":   "0 20px 25px rgba(0,0,0,0.07), 0 8px 10px rgba(0,0,0,0.04)",
    "shadow-2xl":  "0 40px 60px rgba(0,0,0,0.12)",
    "shadow-inner":"inset 0 2px 4px rgba(0,0,0,0.05)",
    "shadow-glow-primary": "0 0 0 4px rgba(108,99,255,0.18)",
    "shadow-glow-danger":  "0 0 0 4px rgba(239,68,68,0.18)",

    # ── Transitions ────────────────────────────────────────────────────
    "ease-instant": "0ms linear",
    "ease-fast":    "120ms cubic-bezier(0.16, 1, 0.3, 1)",
    "ease-normal":  "220ms cubic-bezier(0.16, 1, 0.3, 1)",
    "ease-slow":    "380ms cubic-bezier(0.16, 1, 0.3, 1)",
    "ease-bounce":  "500ms cubic-bezier(0.34, 1.56, 0.64, 1)",
    "ease-spring":  "600ms cubic-bezier(0.175, 0.885, 0.32, 1.275)",

    # ── Z-Index ────────────────────────────────────────────────────────
    "z-below":   "-1",   "z-base":     "0",    "z-above":    "10",
    "z-dropdown":"100",  "z-sticky":   "200",  "z-overlay":  "300",
    "z-modal":   "400",  "z-toast":    "500",  "z-tooltip":  "600",
    "z-max":     "9999",

    # ── Breakpoints (used in media queries) ────────────────────────────
    "bp-sm":  "640px",   "bp-md":  "768px",
    "bp-lg":  "1024px",  "bp-xl":  "1280px",  "bp-2xl": "1536px",

    # ── Blur ───────────────────────────────────────────────────────────
    "blur-sm":  "4px",   "blur-md":  "8px",
    "blur-lg":  "16px",  "blur-xl":  "32px",  "blur-2xl": "64px",
}

# Dark mode — only tokens that change
DARK_TOKENS = {
    "color-bg":          "#09090B",
    "color-surface":     "#111113",
    "color-surface-2":   "#18181B",
    "color-surface-3":   "#27272A",
    "color-border":      "#27272A",
    "color-border-strong":"#3F3F46",
    "color-text":        "#FAFAFA",
    "color-text-muted":  "#A1A1AA",
    "color-text-subtle": "#71717A",
    "color-text-disabled":"#3F3F46",
    "color-primary-subtle": "#1E1B4B",
    "color-secondary":   "#27272A",
    "color-secondary-hover":"#3F3F46",
    "color-secondary-fg":"#FAFAFA",
}
```

#### 5.2.2 StyleRule — The Atomic Unit

```python
# zolt/style/rules.py

from dataclasses import dataclass, field

@dataclass(frozen=True)
class StyleRule:
    """
    One atomic CSS declaration.
    Immutable so it can be hashed and deduplicated.
    """
    prop:      str           # "background-color"
    value:     str           # "var(--z-color-primary)" or "#6C63FF"
    pseudo:    str = ""      # ":hover", ":focus-visible", ":active", "::before"
    state:     str = ""      # "disabled", "loading", "checked", "error"
    media:     str = ""      # "@media (max-width: 768px)"
    important: bool = False

def token(name: str) -> str:
    """Convert a token name to a CSS variable reference."""
    return f"var(--z-{name})"

def px(value: int | str) -> str:
    """Ensure a value is a pixel string."""
    return f"{value}px" if isinstance(value, int) else value
```

#### 5.2.3 StyleResolver — Python Props to CSS Rules

The heart of ZoltCSS. Every component type has a resolver method. The resolver takes the component's Python props and returns a list of `StyleRule` objects. No CSS strings. No class names at this stage — just structured data.

```python
# zolt/style/resolver.py

class StyleResolver:
    """
    Maps component props to StyleRule lists.
    One method per component type.
    Rules are target-agnostic — the generator decides CSS, QSS, or Rich.
    """

    # ── BUTTON ───────────────────────────────────────────────────────
    def button(
        self,
        color:       str  = "primary",
        size:        str  = "md",
        radius:      str  = "md",
        shadow:      str  = "none",
        full_width:  bool = False,
        icon_only:   bool = False,
        ghost:       bool = False,
    ) -> list[StyleRule]:

        # Base rules — every button always gets these
        rules = [
            StyleRule("display",         "inline-flex"),
            StyleRule("align-items",     "center"),
            StyleRule("justify-content", "center"),
            StyleRule("font-family",     token("font-sans")),
            StyleRule("font-weight",     token("font-weight-medium")),
            StyleRule("border-style",    "solid"),
            StyleRule("border-width",    "1px"),
            StyleRule("cursor",          "pointer"),
            StyleRule("user-select",     "none"),
            StyleRule("white-space",     "nowrap"),
            StyleRule("text-decoration", "none"),
            StyleRule("vertical-align",  "middle"),
            StyleRule("transition",      f"all {token('ease-fast')}"),
            StyleRule("border-radius",   token(f"radius-{radius}")),
            # Press effect
            StyleRule("transform",       "scale(0.97)", pseudo=":active"),
            # Focus ring (accessibility — never remove this)
            StyleRule("outline",         f"2px solid {token('color-primary')}", pseudo=":focus-visible"),
            StyleRule("outline-offset",  "2px", pseudo=":focus-visible"),
            # Disabled state
            StyleRule("opacity",         "0.45",       state="disabled"),
            StyleRule("cursor",          "not-allowed",state="disabled"),
            StyleRule("pointer-events",  "none",       state="disabled"),
            # Loading state
            StyleRule("cursor",          "wait",       state="loading"),
            StyleRule("pointer-events",  "none",       state="loading"),
        ]

        # Color variants — semantically named
        variant_map = {
            "primary": [
                StyleRule("background-color", token("color-primary")),
                StyleRule("color",            token("color-primary-fg")),
                StyleRule("border-color",     "transparent"),
                StyleRule("background-color", token("color-primary-hover"), pseudo=":hover"),
                StyleRule("box-shadow",       token("shadow-glow-primary"), pseudo=":hover"),
            ],
            "secondary": [
                StyleRule("background-color", token("color-secondary")),
                StyleRule("color",            token("color-text")),
                StyleRule("border-color",     token("color-border")),
                StyleRule("background-color", token("color-secondary-hover"), pseudo=":hover"),
            ],
            "ghost": [
                StyleRule("background-color", "transparent"),
                StyleRule("color",            token("color-text")),
                StyleRule("border-color",     "transparent"),
                StyleRule("background-color", token("color-surface-2"), pseudo=":hover"),
                StyleRule("border-color",     token("color-border"), pseudo=":hover"),
            ],
            "outline": [
                StyleRule("background-color", "transparent"),
                StyleRule("color",            token("color-primary")),
                StyleRule("border-color",     token("color-primary")),
                StyleRule("background-color", token("color-primary-subtle"), pseudo=":hover"),
            ],
            "danger": [
                StyleRule("background-color", token("color-danger")),
                StyleRule("color",            token("color-danger-fg")),
                StyleRule("border-color",     "transparent"),
                StyleRule("background-color", "#DC2626", pseudo=":hover"),
                StyleRule("box-shadow",       token("shadow-glow-danger"), pseudo=":hover"),
            ],
            "success": [
                StyleRule("background-color", token("color-success")),
                StyleRule("color",            token("color-success-fg")),
                StyleRule("border-color",     "transparent"),
                StyleRule("background-color", "#059669", pseudo=":hover"),
            ],
            "link": [
                StyleRule("background-color", "transparent"),
                StyleRule("color",            token("color-primary")),
                StyleRule("border-color",     "transparent"),
                StyleRule("padding",          "0"),
                StyleRule("text-decoration",  "underline", pseudo=":hover"),
                StyleRule("color",            token("color-primary-hover"), pseudo=":hover"),
            ],
        }
        rules.extend(variant_map.get(color, variant_map["primary"]))

        # Size variants (skipped for link variant)
        if color != "link" and not icon_only:
            size_map = {
                "2xs": [StyleRule("padding", "2px 8px"),   StyleRule("font-size", token("font-size-xs")),  StyleRule("gap", token("space-1")),   StyleRule("height", "24px")],
                "xs":  [StyleRule("padding", "4px 10px"),  StyleRule("font-size", token("font-size-xs")),  StyleRule("gap", token("space-1")),   StyleRule("height", "28px")],
                "sm":  [StyleRule("padding", "6px 14px"),  StyleRule("font-size", token("font-size-sm")),  StyleRule("gap", token("space-1-5")), StyleRule("height", "32px")],
                "md":  [StyleRule("padding", "8px 18px"),  StyleRule("font-size", token("font-size-base")),StyleRule("gap", token("space-2")),   StyleRule("height", "40px")],
                "lg":  [StyleRule("padding", "11px 24px"), StyleRule("font-size", token("font-size-lg")),  StyleRule("gap", token("space-2")),   StyleRule("height", "48px")],
                "xl":  [StyleRule("padding", "14px 32px"), StyleRule("font-size", token("font-size-xl")),  StyleRule("gap", token("space-2-5")), StyleRule("height", "56px")],
            }
            rules.extend(size_map.get(size, size_map["md"]))

        if icon_only:
            icon_size_map = {"xs":"28px","sm":"32px","md":"40px","lg":"48px","xl":"56px"}
            s = icon_size_map.get(size, "40px")
            rules.extend([StyleRule("width",s), StyleRule("height",s), StyleRule("padding","0")])

        if shadow != "none":
            rules.append(StyleRule("box-shadow", token(f"shadow-{shadow}")))

        if full_width:
            rules.append(StyleRule("width", "100%"))

        return rules

    # ── TEXT ─────────────────────────────────────────────────────────
    def text(
        self,
        size:     str  = "base",
        weight:   str  = "normal",
        color:    str  = "text",
        align:    str  = "inherit",
        leading:  str  = "normal",
        tracking: str  = "normal",
        family:   str  = "sans",
        italic:   bool = False,
        underline:bool = False,
        truncate: bool = False,
        clamp:    int  = 0,         # line clamp: 0 = disabled
    ) -> list[StyleRule]:
        rules = [
            StyleRule("font-family",    token(f"font-{family}")),
            StyleRule("font-size",      token(f"font-size-{size}")),
            StyleRule("font-weight",    token(f"font-weight-{weight}")),
            StyleRule("color",          token(f"color-{color}") if not color.startswith("#") else color),
            StyleRule("line-height",    token(f"line-height-{leading}")),
            StyleRule("letter-spacing", token(f"letter-spacing-{tracking}")),
        ]
        if align != "inherit":
            rules.append(StyleRule("text-align", align))
        if italic:
            rules.append(StyleRule("font-style", "italic"))
        if underline:
            rules.append(StyleRule("text-decoration", "underline"))
        if truncate:
            rules.extend([
                StyleRule("overflow", "hidden"),
                StyleRule("text-overflow", "ellipsis"),
                StyleRule("white-space", "nowrap"),
            ])
        if clamp > 0:
            rules.extend([
                StyleRule("display", "-webkit-box"),
                StyleRule("-webkit-line-clamp", str(clamp)),
                StyleRule("-webkit-box-orient", "vertical"),
                StyleRule("overflow", "hidden"),
            ])
        return rules

    # ── FLEX ─────────────────────────────────────────────────────────
    def flex(
        self,
        direction: str        = "row",
        align:     str        = "stretch",
        justify:   str        = "start",
        wrap:      bool       = False,
        gap:       int | str  = 0,
        gap_x:     int | str  = 0,
        gap_y:     int | str  = 0,
        inline:    bool       = False,
    ) -> list[StyleRule]:
        align_map   = {"start":"flex-start","end":"flex-end","center":"center","stretch":"stretch","baseline":"baseline"}
        justify_map = {"start":"flex-start","end":"flex-end","center":"center","between":"space-between","around":"space-around","evenly":"space-evenly"}
        rules = [
            StyleRule("display",         "inline-flex" if inline else "flex"),
            StyleRule("flex-direction",  direction),
            StyleRule("align-items",     align_map.get(align, align)),
            StyleRule("justify-content", justify_map.get(justify, justify)),
            StyleRule("flex-wrap",       "wrap" if wrap else "nowrap"),
        ]
        if gap:
            rules.append(StyleRule("gap", self._sp(gap)))
        if gap_x:
            rules.append(StyleRule("column-gap", self._sp(gap_x)))
        if gap_y:
            rules.append(StyleRule("row-gap", self._sp(gap_y)))
        return rules

    # ── GRID ─────────────────────────────────────────────────────────
    def grid(
        self,
        cols:    int | str = 1,
        rows:    int | str = 0,
        gap:     int | str = 4,
        gap_x:   int | str = 0,
        gap_y:   int | str = 0,
        auto_rows: str     = "auto",
    ) -> list[StyleRule]:
        rules = [
            StyleRule("display", "grid"),
            StyleRule("grid-template-columns",
                      f"repeat({cols}, minmax(0, 1fr))" if isinstance(cols, int) else cols),
            StyleRule("gap", self._sp(gap)),
        ]
        if rows:
            rules.append(StyleRule("grid-template-rows",
                f"repeat({rows}, {auto_rows})" if isinstance(rows, int) else rows))
        if gap_x:
            rules.append(StyleRule("column-gap", self._sp(gap_x)))
        if gap_y:
            rules.append(StyleRule("row-gap", self._sp(gap_y)))
        return rules

    # ── BOX (generic container) ───────────────────────────────────────
    def box(
        self,
        p:       int | str | tuple | None = None,
        px:      int | str | None = None,
        py:      int | str | None = None,
        pt:      int | str | None = None,
        pb:      int | str | None = None,
        pl:      int | str | None = None,
        pr:      int | str | None = None,
        m:       int | str | tuple | None = None,
        mx:      int | str | None = None,
        my:      int | str | None = None,
        width:   str = "auto",
        height:  str = "auto",
        min_w:   str = "0",
        min_h:   str = "0",
        max_w:   str = "none",
        max_h:   str = "none",
        bg:      str | None = None,
        border:  bool = False,
        radius:  str = "none",
        shadow:  str = "none",
        overflow:str = "visible",
        overflow_x:str = "visible",
        overflow_y:str = "visible",
        opacity: float = 1.0,
        cursor:  str = "auto",
        position:str = "static",
        z_index: str = "auto",
    ) -> list[StyleRule]:
        rules = []
        # Spacing
        if p  is not None: rules.append(StyleRule("padding",        self._sp(p)))
        if px is not None: rules.extend([StyleRule("padding-left",  self._sp(px)), StyleRule("padding-right", self._sp(px))])
        if py is not None: rules.extend([StyleRule("padding-top",   self._sp(py)), StyleRule("padding-bottom", self._sp(py))])
        if pt is not None: rules.append(StyleRule("padding-top",    self._sp(pt)))
        if pb is not None: rules.append(StyleRule("padding-bottom", self._sp(pb)))
        if pl is not None: rules.append(StyleRule("padding-left",   self._sp(pl)))
        if pr is not None: rules.append(StyleRule("padding-right",  self._sp(pr)))
        if m  is not None: rules.append(StyleRule("margin",         self._sp(m)))
        if mx is not None: rules.extend([StyleRule("margin-left",   self._sp(mx)), StyleRule("margin-right", self._sp(mx))])
        if my is not None: rules.extend([StyleRule("margin-top",    self._sp(my)), StyleRule("margin-bottom", self._sp(my))])
        # Sizing
        if width   != "auto": rules.append(StyleRule("width",      width))
        if height  != "auto": rules.append(StyleRule("height",     height))
        if min_w   != "0":    rules.append(StyleRule("min-width",  min_w))
        if min_h   != "0":    rules.append(StyleRule("min-height", min_h))
        if max_w   != "none": rules.append(StyleRule("max-width",  max_w))
        if max_h   != "none": rules.append(StyleRule("max-height", max_h))
        # Visual
        if bg:
            v = token(f"color-{bg}") if not bg.startswith("#") else bg
            rules.append(StyleRule("background-color", v))
        if border:
            rules.extend([StyleRule("border-width","1px"), StyleRule("border-style","solid"), StyleRule("border-color", token("color-border"))])
        if radius  != "none": rules.append(StyleRule("border-radius", token(f"radius-{radius}")))
        if shadow  != "none": rules.append(StyleRule("box-shadow",    token(f"shadow-{shadow}")))
        if overflow!= "visible": rules.append(StyleRule("overflow",   overflow))
        if overflow_x!="visible": rules.append(StyleRule("overflow-x", overflow_x))
        if overflow_y!="visible": rules.append(StyleRule("overflow-y", overflow_y))
        if opacity  != 1.0:  rules.append(StyleRule("opacity",    str(opacity)))
        if cursor   != "auto": rules.append(StyleRule("cursor",    cursor))
        if position != "static": rules.append(StyleRule("position", position))
        if z_index  != "auto": rules.append(StyleRule("z-index",   z_index))
        return rules

    # ── INPUT ─────────────────────────────────────────────────────────
    def input(self, size: str = "md", variant: str = "default", error: bool = False) -> list[StyleRule]:
        rules = [
            StyleRule("display",          "block"),
            StyleRule("width",            "100%"),
            StyleRule("font-family",      token("font-sans")),
            StyleRule("background-color", token("color-bg")),
            StyleRule("color",            token("color-text")),
            StyleRule("border-width",     "1px"),
            StyleRule("border-style",     "solid"),
            StyleRule("border-color",     token("color-border-strong") if not error else token("color-danger")),
            StyleRule("border-radius",    token("radius-md")),
            StyleRule("transition",       f"all {token('ease-fast')}"),
            StyleRule("outline",          "none"),
            StyleRule("border-color",     token("color-primary"), pseudo=":focus"),
            StyleRule("box-shadow",       token("shadow-glow-primary"), pseudo=":focus"),
        ]
        size_map = {
            "sm": [StyleRule("padding", "6px 10px"),  StyleRule("font-size", token("font-size-sm")),  StyleRule("height","32px")],
            "md": [StyleRule("padding", "8px 12px"),  StyleRule("font-size", token("font-size-base")),StyleRule("height","40px")],
            "lg": [StyleRule("padding", "10px 16px"), StyleRule("font-size", token("font-size-lg")), StyleRule("height","48px")],
        }
        rules.extend(size_map.get(size, size_map["md"]))
        if error:
            rules.extend([StyleRule("border-color", token("color-danger")), StyleRule("box-shadow", token("shadow-glow-danger"), pseudo=":focus")])
        return rules

    # ── BADGE / TAG ───────────────────────────────────────────────────
    def badge(self, color: str = "primary", size: str = "md", radius: str = "full") -> list[StyleRule]:
        color_map = {
            "primary": (token("color-primary-subtle"), token("color-primary")),
            "success": (token("color-success-subtle"), token("color-success")),
            "warning": (token("color-warning-subtle"), token("color-warning")),
            "danger":  (token("color-danger-subtle"),  token("color-danger")),
            "info":    (token("color-info-subtle"),    token("color-info")),
            "neutral": (token("color-surface-2"),      token("color-text-muted")),
        }
        bg, fg = color_map.get(color, color_map["neutral"])
        size_map = {
            "sm": [StyleRule("padding","2px 6px"),  StyleRule("font-size", token("font-size-xs"))],
            "md": [StyleRule("padding","3px 8px"),  StyleRule("font-size", token("font-size-xs"))],
            "lg": [StyleRule("padding","4px 10px"), StyleRule("font-size", token("font-size-sm"))],
        }
        rules = [
            StyleRule("display",      "inline-flex"),
            StyleRule("align-items",  "center"),
            StyleRule("gap",          token("space-1")),
            StyleRule("font-weight",  token("font-weight-medium")),
            StyleRule("border-radius",token(f"radius-{radius}")),
            StyleRule("background-color", bg),
            StyleRule("color",        fg),
            *size_map.get(size, size_map["md"]),
        ]
        return rules

    # ── CARD ──────────────────────────────────────────────────────────
    def card(
        self,
        p:      int | str = 6,
        shadow: str = "md",
        radius: str = "xl",
        border: bool = True,
        hover_lift: bool = False,
    ) -> list[StyleRule]:
        rules = [
            StyleRule("background-color", token("color-surface")),
            StyleRule("border-radius",    token(f"radius-{radius}")),
            StyleRule("padding",          self._sp(p)),
            StyleRule("box-shadow",       token(f"shadow-{shadow}")),
            StyleRule("transition",       f"all {token('ease-normal')}"),
        ]
        if border:
            rules.extend([StyleRule("border-width","1px"), StyleRule("border-style","solid"), StyleRule("border-color", token("color-border"))])
        if hover_lift:
            rules.extend([
                StyleRule("transform",   "translateY(-4px)",   pseudo=":hover"),
                StyleRule("box-shadow",  token("shadow-xl"),   pseudo=":hover"),
            ])
        return rules

    # ── DIVIDER ───────────────────────────────────────────────────────
    def divider(self, orientation: str = "horizontal", color: str = "border") -> list[StyleRule]:
        if orientation == "horizontal":
            return [StyleRule("width","100%"), StyleRule("height","1px"),
                    StyleRule("background-color", token(f"color-{color}")), StyleRule("border","none")]
        return [StyleRule("width","1px"), StyleRule("height","100%"),
                StyleRule("background-color", token(f"color-{color}")), StyleRule("border","none")]

    # ── RESPONSIVE HELPER ─────────────────────────────────────────────
    def responsive(self, rules: list[StyleRule], breakpoint: str) -> list[StyleRule]:
        """Wrap rules in a media query for responsive styling."""
        bp = {"sm":"640px","md":"768px","lg":"1024px","xl":"1280px","2xl":"1536px"}
        query = f"@media (min-width: {bp.get(breakpoint, breakpoint)})"
        return [StyleRule(r.prop, r.value, r.pseudo, r.state, query, r.important) for r in rules]

    def _sp(self, value) -> str:
        """Resolve spacing value — int maps to token, string returned as-is."""
        if isinstance(value, int): return token(f"space-{value}")
        if isinstance(value, tuple): return " ".join(self._sp(v) for v in value)
        return value
```

#### 5.2.4 ZoltCSS Generator — Outputs the CSS File

```python
# zolt/style/css_generator.py

class ZoltCSSGenerator:
    """
    Collects StyleRules from every component in the IR tree.
    Deduplicates. Assigns short atomic class names.
    Outputs one zolt.min.css file. No Tailwind. No external tools.
    Pure Python. Typical output: 6–14KB gzipped.
    """

    def __init__(self, tokens: dict, dark_tokens: dict, dev_mode: bool = False):
        self._tokens = tokens
        self._dark_tokens = dark_tokens
        self._dev_mode = dev_mode
        self._registry: dict[str, str] = {}  # rule fingerprint → class name
        self._counter = 0

    def register(self, rules: list[StyleRule]) -> list[str]:
        """Register rules for a component. Returns class names to apply."""
        names = []
        for rule in rules:
            fp = f"{rule.prop}|{rule.value}|{rule.pseudo}|{rule.state}|{rule.media}"
            if fp not in self._registry:
                self._counter += 1
                self._registry[fp] = self._name(rule)
            names.append(self._registry[fp])
        return names

    def _name(self, rule: StyleRule) -> str:
        if self._dev_mode:
            safe = rule.prop.replace("-","")[:14]
            return f"z-{safe}-{self._counter}"
        return f"z{self._counter}"

    def render(self) -> str:
        out = []

        # CSS custom properties — all tokens as variables
        out.append(":root {")
        for k, v in self._tokens.items():
            out.append(f"  --z-{k}: {v};")
        out.append("}")

        # Dark mode overrides
        if self._dark_tokens:
            out.append("\n@media (prefers-color-scheme: dark) {\n  :root {")
            for k, v in self._dark_tokens.items():
                out.append(f"    --z-{k}: {v};")
            out.append("  }\n}")

        # [data-theme='dark'] override for manual dark mode toggle
        out.append("\n[data-theme='dark'] {")
        for k, v in self._dark_tokens.items():
            out.append(f"  --z-{k}: {v};")
        out.append("}")

        out.append("")

        # Atomic classes — group standard, then by media query
        standard = {}
        by_media  = {}
        for fp, name in self._registry.items():
            prop, value, pseudo, state, media = fp.split("|")
            rule = StyleRule(prop, value, pseudo, state, media)
            if media:
                by_media.setdefault(media, {})[name] = rule
            else:
                standard[name] = rule

        for name, rule in standard.items():
            out.append(self._css_rule(name, rule))

        for media, rules in by_media.items():
            out.append(f"\n{media} {{")
            for name, rule in rules.items():
                out.append("  " + self._css_rule(name, rule))
            out.append("}")

        return "\n".join(out)

    def _css_rule(self, name: str, rule: StyleRule) -> str:
        imp = " !important" if rule.important else ""
        decl = f"{rule.prop}: {rule.value}{imp};"
        sel = f".{name}"

        if rule.pseudo:
            sel += rule.pseudo

        if rule.state == "disabled":
            sel = f".{name}:disabled, .{name}[aria-disabled='true']"
        elif rule.state == "loading":
            sel = f".{name}[data-loading='true']"
        elif rule.state == "checked":
            sel = f".{name}:checked, .{name}[aria-checked='true']"
        elif rule.state == "error":
            sel = f".{name}[data-error='true'], .{name}[aria-invalid='true']"

        return f"{sel} {{ {decl} }}"
```

#### 5.2.5 Qt Style Generator — Same Rules, QSS Output

```python
# zolt/style/qt_generator.py

class QtStyleGenerator:
    """
    Consumes the same StyleRule lists as the CSS generator.
    Outputs QSS (Qt Style Sheets) for Qt5 and Qt6 desktop.
    Resolves CSS variables to actual values from the token dictionary.
    """
    def __init__(self, tokens: dict):
        self._tokens = tokens

    def to_qss(self, widget_class: str, rules: list[StyleRule]) -> str:
        normal  = [r for r in rules if not r.pseudo and not r.state]
        hover   = [r for r in rules if r.pseudo == ":hover"]
        focus   = [r for r in rules if r.pseudo in (":focus",":focus-visible")]
        pressed = [r for r in rules if r.pseudo == ":active"]
        disabled= [r for r in rules if r.state == "disabled"]

        def block(selector, rule_list):
            if not rule_list: return ""
            css_rules = [f"  {self._prop(r.prop)}: {self._val(r.value)};" for r in rule_list]
            return f"{selector} {{\n" + "\n".join(css_rules) + "\n}\n"

        qss = ""
        qss += block(widget_class, normal)
        qss += block(f"{widget_class}:hover", hover)
        qss += block(f"{widget_class}:focus", focus)
        qss += block(f"{widget_class}:pressed", pressed)
        qss += block(f"{widget_class}:disabled", disabled)
        return qss

    def _val(self, value: str) -> str:
        """Resolve var(--z-token-name) to its actual value."""
        if value.startswith("var(--z-"):
            key = value[8:-1]
            resolved = self._tokens.get(key, value)
            # Recursively resolve nested vars
            if resolved.startswith("var(--z-"):
                return self._val(resolved)
            return resolved
        return value

    def _prop(self, css_prop: str) -> str:
        """Map CSS property names to QSS equivalents."""
        mapping = {
            "background-color": "background-color",
            "border-color":     "border-color",
            "border-radius":    "border-radius",
            "color":            "color",
            "font-size":        "font-size",
            "font-weight":      "font-weight",
            "font-family":      "font-family",
            "padding":          "padding",
            "border-width":     "border-width",
        }
        return mapping.get(css_prop, css_prop)
```

#### 5.2.6 Rich Style Generator — Same Rules, CLI Output

```python
# zolt/style/rich_generator.py

class RichStyleGenerator:
    """
    Consumes StyleRule lists and outputs Rich Style objects for CLI rendering.
    Uses the same token system as web and Qt.
    """
    def __init__(self, tokens: dict):
        self._tokens = tokens

    def to_rich_style(self, rules: list[StyleRule]) -> "rich.Style":
        import rich.style as rs
        normal = {r.prop: r.value for r in rules if not r.pseudo and not r.state}

        bg   = self._resolve(normal.get("background-color", ""))
        fg   = self._resolve(normal.get("color", ""))
        bold = normal.get("font-weight", "") in ("700","800","900",
               "var(--z-font-weight-bold)","var(--z-font-weight-extra)",
               "var(--z-font-weight-black)")
        italic = normal.get("font-style","") == "italic"
        under  = normal.get("text-decoration","") == "underline"

        kwargs = {}
        if bg:   kwargs["bgcolor"] = bg
        if fg:   kwargs["color"]   = fg
        if bold: kwargs["bold"]    = True
        if italic: kwargs["italic"] = True
        if under:  kwargs["underline"] = True
        return rs.Style(**kwargs)

    def _resolve(self, value: str) -> str:
        if not value: return ""
        if value.startswith("var(--z-"):
            key = value[8:-1]
            resolved = self._tokens.get(key, "")
            if resolved.startswith("var(--z-"):
                return self._resolve(resolved)
            return resolved
        return value
```

---

### 5.3 Layer 2: JS Bundler — zolt-bundler

Built after ZoltCSS because animations and 3D both need it.

`zolt-bundler` is a small Python package that:
- Ships pre-compiled `esbuild` binaries for Windows/macOS/Linux (x64 + ARM)
- Bundles GSAP, Alpine.js, Three.js, Lottie, Rive, and Spline runtime as local assets
- Exposes one Python API: `Bundler(entries=[...], output="dist/app.js").run()`
- Is called by `zolt build` and `zolt run` automatically — the user never runs it

```bash
# User never does this:
npm install gsap three alpinejs    ← never

# Zolt does this internally:
pip install zolt[web]
# → installs zolt-bundler which includes all JS as package data
# → zolt-bundler calls embedded esbuild to produce app.bundle.js
```

**Why esbuild over webpack/rollup:** esbuild bundles in milliseconds not seconds, ships as a single binary, requires no config file, and supports tree-shaking out of the box. A 50-component app bundles in under 300ms.

**Bundle composition and size targets:**

| Bundle mode | Contents | Gzip target |
|---|---|---|
| Minimal | Alpine.js only | ~15KB |
| Animated | Alpine.js + GSAP + ScrollTrigger | ~65KB |
| Full | Alpine.js + GSAP + Three.js | ~300KB |
| Maximum | All libs | ~480KB |

Zolt's compiler detects which JS libraries are used and only bundles those. An app with no `Scene3D` components never pays for Three.js.

---

### 5.4 Layer 3: Animation Engine

Built after ZoltCSS (animated elements need styling) and after zolt-bundler (needs GSAP).

#### Architecture

**Python side:** Every `BaseComponent` gains an `.animate()` method. Animation functions like `fade_in()` and `slide_up()` return `AnimationSpec` objects — structured Python data, not strings. The compiler collects all `AnimationSpec` objects from the IR tree into `AnimationNode` entries.

**Generated JS side:** The web renderer converts `AnimationNode` entries to GSAP JavaScript, appended to `app.bundle.js`. Qt uses `QPropertyAnimation`. CLI ignores most animations (stateless) but respects `counter()` and `typewriter()`.

#### Full Animation API

```python
# zolt/animate/__init__.py — complete public API

# ── Opacity ────────────────────────────────────────────────────────
def fade_in (duration=0.5, delay=0, ease="power2.out") -> AnimationSpec: ...
def fade_out(duration=0.5, delay=0, ease="power2.in")  -> AnimationSpec: ...

# ── Translate + Opacity ────────────────────────────────────────────
def slide_up   (duration=0.7, delay=0, distance=48, ease="power3.out") -> AnimationSpec: ...
def slide_down (duration=0.7, delay=0, distance=48, ease="power3.out") -> AnimationSpec: ...
def slide_left (duration=0.7, delay=0, distance=48, ease="power3.out") -> AnimationSpec: ...
def slide_right(duration=0.7, delay=0, distance=48, ease="power3.out") -> AnimationSpec: ...

# ── Scale ──────────────────────────────────────────────────────────
def scale_in (duration=0.5, delay=0, from_scale=0.88, ease="back.out(1.7)") -> AnimationSpec: ...
def scale_out(duration=0.4, delay=0, to_scale=0.88,   ease="power2.in")     -> AnimationSpec: ...

# ── Blur ───────────────────────────────────────────────────────────
def blur_in (duration=0.7, delay=0, from_blur=12, ease="power2.out") -> AnimationSpec: ...
def blur_out(duration=0.5, delay=0, to_blur=12,   ease="power2.in")  -> AnimationSpec: ...

# ── Advanced ───────────────────────────────────────────────────────
def clip_reveal(duration=0.9, delay=0, direction="up",    ease="power4.inOut") -> AnimationSpec: ...
def flip_in    (duration=0.6, delay=0, axis="y",          ease="power3.out")   -> AnimationSpec: ...
def bounce_in  (duration=0.8, delay=0,                    ease="elastic.out(1, 0.3)") -> AnimationSpec: ...

# ── Text ───────────────────────────────────────────────────────────
def typewriter   (speed=0.04, cursor=True, cursor_char="|") -> AnimationSpec: ...
def counter      (start=0, end=100, duration=2.0, suffix="", prefix="") -> AnimationSpec: ...
def word_by_word (duration=0.6, stagger=0.08, ease="power2.out") -> AnimationSpec: ...
def char_by_char (duration=0.5, stagger=0.02, ease="power2.out") -> AnimationSpec: ...
def scramble     (duration=1.5, chars="upperCase")                -> AnimationSpec: ...

# ── Interactive (cursor-driven) ────────────────────────────────────
def magnetic  (strength=0.25, ease=0.12)          -> AnimationSpec: ...
def tilt_3d   (max_angle=12, perspective=1000)     -> AnimationSpec: ...
def hover_lift(amount=6, shadow=True)              -> AnimationSpec: ...
def parallax  (speed=0.3, direction="y")           -> AnimationSpec: ...
def cursor_follow(strength=0.2)                    -> AnimationSpec: ...

# ── Compound ───────────────────────────────────────────────────────
def stagger(
    each:       AnimationSpec,
    interval:   float = 0.1,
    from_:      str   = "start",    # "start"|"end"|"center"|"edges"|"random"
    trigger:    str   = "scroll",   # "scroll"|"load"|"hover"|"click"
) -> AnimationSpec: ...

# ── Continuous ─────────────────────────────────────────────────────
def float_up  (speed=2.5, amplitude=8)   -> AnimationSpec: ...  # infinite float
def pulse     (scale=1.05, speed=2.0)    -> AnimationSpec: ...  # infinite pulse
def spin      (duration=8.0, ease="none")-> AnimationSpec: ...  # infinite spin
def shimmer   (duration=1.5)             -> AnimationSpec: ...  # loading shimmer

# ── Timeline ───────────────────────────────────────────────────────
class Timeline:
    def add(self, component, animation: AnimationSpec, offset: str = "+=0") -> Timeline: ...
    def play_on(self, trigger: str) -> Timeline: ...     # "load"|"scroll"|"click"
    def repeat(self, times: int = -1, yoyo: bool = False) -> Timeline: ...
    def delay(self, seconds: float) -> Timeline: ...

# ── Scroll-triggered ───────────────────────────────────────────────
class ScrollReveal:
    start:       str   = "top 80%"
    end:         str   = "bottom 20%"
    scrub:       bool | float = False   # True = scrub, float = smooth factor
    pin:         bool  = False
    once:        bool  = True           # play once then stay
    markers:     bool  = False          # dev mode debug markers

class ScrollLinked:
    """Link any CSS property to scroll progress."""
    prop:        str                    # "opacity", "transform", etc.
    from_value:  str
    to_value:    str
    start:       int = 0               # scroll px
    end:         int = 800

# ── Page Transitions ───────────────────────────────────────────────
class PageTransition:
    enter:       AnimationSpec
    leave:       AnimationSpec
    duration:    float = 0.35

# ── Lottie ─────────────────────────────────────────────────────────
class Lottie(Component):
    src:         str
    loop:        bool  = True
    autoplay:    bool  = True
    speed:       float = 1.0
    width:       str   = "100%"
    height:      str   = "auto"

# ── Rive ───────────────────────────────────────────────────────────
class Rive(Component):
    src:         str
    animation:   str | None = None
    state_machine:str | None = None
    autoplay:    bool = True
```

**`prefers-reduced-motion` compliance:** All generated GSAP code is wrapped in a motion preference check. When the OS reports reduced motion preference, all animations are skipped — components are shown in their final state instantly. This is non-negotiable and automatic.

---

### 5.5 Layer 4: 3D Engine

Built after the animation engine (3D objects animate) and after zolt-bundler (needs Three.js).

#### Full 3D API

```python
# zolt/three/__init__.py

# ── Scene ──────────────────────────────────────────────────────────
class Scene3D(Component):
    width:       str   = "100%"
    height:      str   = "500px"
    background:  str   = "transparent"   # color or "transparent"
    camera:      CameraConfig = CameraConfig(fov=75, near=0.1, far=1000, position=(0,0,5))
    antialias:   bool  = True
    shadow:      bool  = True
    pixel_ratio: float = 2.0

    def add(self, *objects) -> Scene3D: ...
    def controls(self, c: Controls) -> Scene3D: ...
    def env_map(self, preset: str) -> Scene3D: ...   # "sunset","dawn","night","warehouse"
    def fog(self, color: str, near: float, far: float) -> Scene3D: ...
    def on_created(self, fn: Callable) -> Scene3D: ...

# ── Geometry Primitives ────────────────────────────────────────────
class Sphere   (Geometry): radius=1; w_seg=64; h_seg=64
class Box      (Geometry): width=1; height=1; depth=1
class Torus    (Geometry): radius=1; tube=0.4; radial_seg=16; tubular_seg=100
class Cylinder (Geometry): top_r=1; bottom_r=1; height=2; seg=32
class Cone     (Geometry): radius=1; height=2; seg=32
class Plane    (Geometry): width=1; height=1; w_seg=1; h_seg=1
class Ring     (Geometry): inner_r=0.5; outer_r=1; seg=32
class Text3D   (Geometry): text=""; font="/assets/fonts/inter_bold.json"; size=0.5; depth=0.1; bevel=True
class RoundedBox(Geometry): width=1; height=1; depth=1; radius=0.1; smooth=5

# ── Mesh ───────────────────────────────────────────────────────────
class Mesh(Component):
    geometry:    Geometry
    material:    Material | dict
    position:    tuple = (0,0,0)
    rotation:    tuple = (0,0,0)
    scale:       tuple = (1,1,1)
    cast_shadow: bool = True
    receive_shadow: bool = True
    visible:     bool = True

    def animate(self, *animations) -> Mesh: ...
    def rotate(self, x=0, y=0, z=0) -> Mesh: ...   # per-frame speed
    def material(self, **kwargs) -> Mesh: ...

# ── Materials ──────────────────────────────────────────────────────
class MeshStandardMaterial:
    color:      str   = "#ffffff"
    metalness:  float = 0.0
    roughness:  float = 0.5
    wireframe:  bool  = False
    transparent:bool  = False
    opacity:    float = 1.0
    env_map_intensity: float = 1.0

class MeshPhysicalMaterial(MeshStandardMaterial):
    transmission: float = 0.0   # Glass — 1.0 = fully transparent
    ior:          float = 1.5
    thickness:    float = 0.5
    clearcoat:    float = 0.0

class MeshBasicMaterial:
    color:   str  = "#ffffff"
    wireframe: bool = False

class ShaderMaterial:
    vertex_shader:   str
    fragment_shader: str
    uniforms:        dict = {}
    transparent:     bool = False

# ── Lights ─────────────────────────────────────────────────────────
class AmbientLight:     color="#fff"; intensity=0.5
class DirectionalLight: color="#fff"; intensity=1.0; position=(5,5,5); cast_shadow=True
class PointLight:       color="#fff"; intensity=1.0; position=(0,10,0); distance=0; cast_shadow=True
class SpotLight:        color="#fff"; intensity=1.0; position=(0,10,0); angle=0.3; cast_shadow=True
class HemisphereLight:  sky_color="#fff"; ground_color="#444"; intensity=0.6
class RectAreaLight:    color="#fff"; intensity=1.0; width=5; height=5; position=(0,5,0)

# ── Controls ───────────────────────────────────────────────────────
class OrbitControls:
    enable_zoom:   bool  = True
    enable_pan:    bool  = True
    auto_rotate:   bool  = False
    auto_rotate_speed: float = 1.0
    damping:       bool  = True
    min_distance:  float = 1
    max_distance:  float = 100
    min_polar_angle: float = 0
    max_polar_angle: float = 3.14

# ── Built-in Animations ────────────────────────────────────────────
class Float:    speed=1.5; amplitude=0.4; rotation_intensity=0.5
class Rotate:   x=0; y=0.01; z=0        # per-frame rotation
class Pulse:    scale_to=1.1; speed=2.0
class Oscillate:amplitude=1; speed=1.5; axis="y"

# ── Assets ─────────────────────────────────────────────────────────
class GLTFModel(Component):
    src:         str
    auto_rotate: bool  = False
    auto_rotate_speed: float = 1.0
    cast_shadow: bool  = True
    loading:     Component | None = None

class ParticleSystem(Component):
    count:  int   = 2000
    color:  str   = "#ffffff"
    size:   float = 0.01
    spread: float = 8.0
    flow:   bool  = True
    flow_speed: float = 0.3

# ── Spline ─────────────────────────────────────────────────────────
class Spline(Component):
    url:     str
    width:   str = "100%"
    height:  str = "500px"
    loading: Component | None = None
    events:  dict[str, Callable] = {}
```

---

### 5.6 Layer 5: Zolt UI — 80+ Prebuilt Components

Built after ZoltCSS (all styling), animation engine (entrance animations built-in), and 3D (hero variants with 3D backgrounds).

`pip install zolt-ui`

Every component uses ZoltCSS tokens. Every component is dark mode compatible. Every component has animations built in. Every component works on web, Qt desktop, and CLI (where applicable).

#### Full Component Catalogue

```
Authentication (8)
├── LoginPage           — 3 variants: centered, split, minimal
├── SignupPage           — 3 variants + social + invite code
├── ForgotPasswordPage
├── MagicLinkPage
├── TwoFactorPage        — TOTP + SMS options
├── OnboardingFlow       — multi-step with progress bar
├── ProfileSetupPage
└── AuthLayout           — shared wrapper with brand area

Landing / Marketing (20)
├── HeroSection          — 8 variants: centered, split, video bg, 3D bg,
│                          gradient, editorial, minimal, bold-type
├── FeatureGrid          — icon + title + desc, 3-column
├── FeatureShowcase      — large alternating rows with screenshots
├── FeatureComparison    — side-by-side feature matrix
├── PricingTable         — monthly/annual toggle, 3 tiers, highlighted
├── PricingComparison    — full feature comparison table
├── TestimonialsGrid     — avatar + quote cards
├── TestimonialsCarousel — auto-scrolling with controls
├── LogoCloud            — partner logos marquee (infinite scroll)
├── StatsRow             — animated number counters
├── CTASection           — 6 variants: centered, split, dark, gradient, image, minimal
├── FAQAccordion         — animated open/close with smooth height
├── TeamGrid             — photo + name + role + social links
├── BlogGrid             — article card grid
├── BlogFeatured         — large featured post + grid
├── NewsletterSection    — email capture with validation
├── BentoGrid            — asymmetric bento box layout (Notion-style)
├── TimelineSection      — vertical / horizontal with animation
├── VideoSection         — thumbnail with Lightbox player
└── MapSection           — embedded map with custom marker

Dashboard / App (24)
├── AppLayout            — sidebar + topbar + content + mobile drawer
├── Sidebar              — collapsible with icons, groups, and badges
├── Topbar               — search + notifications + avatar + breadcrumb
├── StatsGrid            — KPI cards with icon, value, trend, sparkline
├── DataTable            — sort / filter / paginate / select / export
├── AreaChart
├── BarChart             — grouped / stacked
├── LineChart            — multi-series
├── DonutChart
├── HeatmapChart
├── ActivityFeed         — timestamped event list with icons
├── NotificationPanel    — notification drawer with groups
├── CommandPalette       — Cmd+K with sections + keyboard nav
├── UserTable            — avatar + name + role + actions
├── SettingsLayout       — sticky sidebar nav + content area
├── BillingSection       — plan cards + payment method + invoice table
├── EmptyState           — illustrated with CTA + 3 illustration styles
├── LoadingState         — skeleton loaders for every component type
├── ErrorState           — error boundary with retry
├── SearchResults        — real-time result list
├── FilterBar            — multi-filter chip bar with clear all
├── Breadcrumbs          — navigational with truncation
├── Kanban               — drag-and-drop board
└── CalendarView         — month/week/day views

E-commerce (10)
├── ProductCard          — image + title + price + rating + CTA
├── ProductGrid          — responsive with filters
├── ProductDetail        — hero image gallery + specs + add to cart
├── CartDrawer           — slide-out with upsells
├── CheckoutFlow         — 3-step: cart → shipping → payment
├── OrderSummary
├── OrderHistory         — table with status badges
├── ReviewsSection       — star distribution + review cards
├── WishlistGrid
└── CategoryNav          — horizontal or sidebar category tree

Forms & Inputs (14)
├── ContactForm          — with file upload + captcha
├── MultiStepForm        — step indicator + animated transitions
├── SearchBar            — with autocomplete dropdown
├── DatePicker           — single + range
├── TimePicker
├── FileUpload           — drag-and-drop + preview
├── RichTextEditor       — Tiptap with toolbar
├── CodeEditor           — syntax highlight + line numbers
├── AddressForm          — with country detection + postcode lookup
├── PaymentForm          — Stripe Elements wrapper
├── TagInput             — multi-tag with autocomplete
├── ColorPicker          — hex + HSL + swatches
├── RatingInput          — star / emoji variants
└── SliderInput          — single + range + labels

Feedback & Overlays (9)
├── Toast                — top/bottom, 5 variants, with actions
├── Modal                — animated, focus-trapped, accessible
├── Drawer               — left/right/bottom slide-in
├── AlertBanner          — dismissible top-of-page banner
├── ConfirmDialog        — destructive action confirmation
├── Tooltip              — rich with arrow, delay, max-width
├── Popover              — floating panel with content
├── ContextMenu          — right-click with groups + icons
└── CommandMenu          — slash-command with keyboard

Navigation (5)
├── MegaNav             — full-featured with mega dropdown + mobile
├── TabBar              — animated underline indicator
├── BottomNav           — mobile bottom navigation
├── FloatingNav         — scroll-aware sticky navbar
└── Pagination          — numbered + prev/next + page size selector

Total: 90 components across 7 categories
```

**Usage — minimal code, maximum result:**

```python
from zolt import App, Page
from zolt_ui.auth import LoginPage
from zolt_ui.landing import HeroSection, PricingTable, FAQAccordion, CTASection
from zolt_ui.dashboard import AppLayout, StatsGrid, DataTable

class MySaaS(App):
    theme = "dark"

    # Marketing site — assembled from prebuilts, zero styling needed
    home = Page(title="My SaaS", route="/")
    home.add(
        HeroSection(
            title="Build anything.",
            subtitle="In pure Python.",
            variant="centered",
            background="gradient",
            cta_primary=Button("Start free"),
            cta_secondary=Button("View demo"),
        ),
        PricingTable(plans=my_plans, on_select=handle_plan),
        FAQAccordion(items=my_faqs),
        CTASection(title="Ready?", variant="dark"),
    )

    # Auth — one line each
    login  = LoginPage(providers=["google","github"], on_success=go_to_dashboard)
    signup = SignupPage(providers=["google"],          on_success=go_to_onboarding)

    # App — fully prebuilt layout
    dashboard = Page(route="/dashboard", guard=lambda: is_logged_in())
    dashboard.add(
        AppLayout(
            sidebar=Sidebar(items=nav_items, collapsed=False),
            content=Stack(gap=6).add(
                StatsGrid(stats=live_stats),
                DataTable(data=users, columns=["Name","Email","Plan","Status"]),
            )
        )
    )
```

---

### 5.7 Layer 6: Design Import System

Built after Zolt UI (import maps Figma components to zolt-ui components).

```bash
zolt import figma   https://figma.com/file/ABC123/MyApp   --output pages/
zolt import framer  ./framer-export/                      --output pages/
zolt import webflow ./webflow-export.zip                  --output pages/
```

**Figma import pipeline:**

1. Call Figma REST API → fetch full node tree as JSON
2. Walk node tree: DOCUMENT → CANVAS → FRAME → GROUP → COMPONENT
3. Map each node type: AUTO_LAYOUT → Flex/Grid, TEXT → Text/Heading, INSTANCE → zolt-ui fuzzy match
4. Extract styles: typography, colors (map to nearest ZoltCSS token), spacing
5. Generate `.py` file with complete component tree

**Accuracy targets:**

| Element | Target |
|---|---|
| Layout structure (flex/grid/stack) | 90%+ |
| Typography (size, weight, family) | 92%+ |
| Colors (mapped to theme tokens) | 96%+ |
| Spacing and padding | 85%+ |
| Component name matching (zolt-ui) | 75%+ |
| Interactive states | 55%+ |

---

### 5.8 Layer 7: Desktop v1.5 — Qt5 + Qt6 + WebEngine

**Qt5:** Full widget renderer. All Zolt UI components supported. `pip install zolt[qt5]`.

**Qt6:** Enhanced widget renderer. Native dark mode. `pip install zolt[qt6]`.

**Qt6 WebEngine:** Full Chromium inside a Qt window. Renders identical to web output including GSAP animations and Three.js 3D. `pip install zolt[qt6-webengine]`.

| Mode | Startup | Binary size | 3D | Animations | Fidelity |
|---|---|---|---|---|---|
| tkinter | < 0.5s | 8MB | No | Basic | Low |
| Qt5 | < 1s | 35MB | No | QPropertyAnimation | Medium |
| Qt6 | < 1s | 40MB | No | QPropertyAnimation | High |
| Qt6 WebEngine | < 1.5s | 120MB | Yes | Full GSAP | Pixel-perfect |

**How Qt WebEngine mode works:** The Python app compiles web output to a temp directory. Zolt starts a local aiohttp server on a random port serving the output. Qt6 WebEngineView points to `http://localhost:{port}`. Result: full browser rendering inside a native desktop window, with the Python process handling all logic.

---

### 5.9 Layer 8: CLI Renderer Upgrade

V1.0 CLI used plain Rich. V1.5 upgrades to Textual for interactive apps while keeping Rich for static output.

```bash
zolt run --cli                    # Textual interactive mode (default)
zolt run --cli --static           # Rich static output (piping, logging)
```

New interactive CLI components: `CLIModal`, `CLIForm`, `CLITable`, `CLIMenu`, `CLIProgress`, `CLIChart`. All styled using `RichStyleGenerator` from ZoltCSS tokens — same theme as web and desktop.

---

### 5.10 Layer 9: AI-First Architecture & Skill Files

Built last (after everything is stable) so skill files describe the real, final API.

**The four parts of AI compatibility:**

1. **Skill files** (`zolt/skills/*.yaml`) — one per component, machine-readable
2. **`zolt.schema.json`** — auto-generated from type hints, all props and methods
3. **`LLMS.txt`** (`zolt.dev/llms.txt`) — human+AI readable plain text API summary
4. **Predictable patterns** — one way to do each thing; consistent method names everywhere

**Consistent method names that AI agents can rely on:**
- All event handlers: `onClick`, `onChange`, `onSubmit`, `onHover`, `onFocus`, `onBlur`, `onMount`, `onUnmount`
- All size props: `"2xs"`, `"xs"`, `"sm"`, `"md"`, `"lg"`, `"xl"` — same across every component
- All color props: semantic token names — `"primary"`, `"danger"`, `"text-muted"` etc.
- All animation entries: `.animate(animation_spec)` — same on every component

---

### 5.11 Performance Requirements

| Metric | Target |
|---|---|
| CSS output (ZoltCSS, gzipped) | < 12KB |
| JS bundle (no 3D, gzipped) | < 90KB |
| JS bundle (with GSAP, gzipped) | < 130KB |
| JS bundle (with Three.js, gzipped) | < 320KB |
| First Contentful Paint (4G) | < 1.2s |
| Lighthouse Performance | > 90 |
| Lighthouse Accessibility | > 95 |
| `zolt build` total time (50 components) | < 8s |
| Hot reload latency | < 200ms |
| ZoltCSS generation time | < 100ms |
| esbuild bundle time | < 500ms |

### 5.12 Accessibility Requirements

- All components pass axe-core automated audit
- All interactive elements keyboard-navigable
- All WCAG 2.1 AA colour contrast met (4.5:1 text, 3:1 UI)
- Focus indicators on all interactive elements (built into ZoltCSS focus styles)
- `aria-live` on dynamic content
- Focus trap in modals and drawers
- All images require `alt` — compiler emits `[ZOLT-1502]` warning if missing
- `prefers-reduced-motion` disables all GSAP animations automatically

---

## 6. API Design — Full Reference

### 6.1 Developer Styling API

This is the developer-facing surface. Everything flows through Python methods — zero CSS.

```python
# Every component inherits these styling methods from BaseComponent

# ── Color ─────────────────────────────────────────────────────────
.color(variant: str)            # "primary"|"secondary"|"ghost"|"danger"|"link"
.bg(token_or_hex: str)          # "surface"|"primary"|"#FF0000"
.text_color(token: str)         # "text"|"text-muted"|"primary"|"danger"

# ── Size ──────────────────────────────────────────────────────────
.size(s: str)                   # "2xs"|"xs"|"sm"|"md"|"lg"|"xl"
.width(w: str)                  # "full"|"auto"|"screen"|"fit"|"100px"
.height(h: str)
.min_width(w: str)
.max_width(w: str)

# ── Spacing ───────────────────────────────────────────────────────
.padding(n: int | tuple)        # int = token index (1–64), tuple = (v,h) or (t,r,b,l)
.p(n)                           # shorthand
.px(n)                          # horizontal padding
.py(n)                          # vertical padding
.pt(n); .pb(n); .pl(n); .pr(n) # individual sides
.margin(n: int | tuple)         # same as padding
.m(n); .mx(n); .my(n)
.mt(n); .mb(n); .ml(n); .mr(n)
.gap(n: int)                    # spacing between children

# ── Shape ─────────────────────────────────────────────────────────
.radius(r: str)                 # "none"|"sm"|"md"|"lg"|"xl"|"2xl"|"full"
.shadow(s: str)                 # "none"|"xs"|"sm"|"md"|"lg"|"xl"|"2xl"
.border(color: str = "border")  # adds 1px solid border
.border_width(w: str)
.border_color(c: str)
.outline(color: str, width: str = "2px")

# ── Typography (on text-bearing components) ───────────────────────
.font_size(s: str)              # "xs"|"sm"|"base"|"lg"|"xl"|"2xl"...|"9xl"
.font_weight(w: str)            # "thin"|"light"|"normal"|"medium"|"semi"|"bold"|"black"
.font_family(f: str)            # "sans"|"serif"|"mono"|"display"
.line_height(lh: str)           # "none"|"tight"|"snug"|"normal"|"relaxed"|"loose"
.tracking(t: str)               # "tight"|"snug"|"normal"|"wide"|"wider"|"widest"
.text_align(a: str)             # "left"|"center"|"right"|"justify"
.italic(enabled: bool = True)
.underline(enabled: bool = True)
.truncate(enabled: bool = True)
.clamp(lines: int)              # line clamp

# ── Layout ────────────────────────────────────────────────────────
.display(d: str)                # "flex"|"grid"|"block"|"inline"|"hidden"
.flex(direction="row", align="stretch", justify="start", wrap=False)
.grid(cols=1, gap=4)
.position(p: str)               # "static"|"relative"|"absolute"|"fixed"|"sticky"
.z_index(z: str | int)
.overflow(o: str)               # "visible"|"hidden"|"scroll"|"auto"

# ── Visual ────────────────────────────────────────────────────────
.opacity(o: float)              # 0.0–1.0
.blur(b: str)                   # "sm"|"md"|"lg"|"xl"
.cursor(c: str)                 # "pointer"|"default"|"not-allowed"|"wait"|"text"
.transition(speed: str = "normal") # "fast"|"normal"|"slow"
.transform(css: str)            # raw transform as escape hatch

# ── State ─────────────────────────────────────────────────────────
.hidden(condition: bool | ReactiveVar = True)
.disabled(condition: bool | ReactiveVar = False)
.loading(condition: bool | ReactiveVar = False)
.error(condition: bool | ReactiveVar = False)

# ── Responsive ────────────────────────────────────────────────────
# Every method can be scoped to a breakpoint:
.on("md").size("lg")            # size lg on screens ≥ 768px
.on("lg").padding(8)            # padding 8 on screens ≥ 1024px
.on("sm").display("hidden")     # hide on mobile

# ── Dark Mode ─────────────────────────────────────────────────────
.dark().bg("surface-2")         # override bg in dark mode
.dark().text_color("text")      # override text in dark mode

# ── Animation ─────────────────────────────────────────────────────
.animate(spec: AnimationSpec)
.animate_on_scroll(spec: AnimationSpec)
.animate_on_hover(spec: AnimationSpec)
.animate_on_click(spec: AnimationSpec)

# ── Events ────────────────────────────────────────────────────────
.onClick(fn: Callable)
.onChange(fn: Callable)
.onSubmit(fn: Callable)
.onHover(fn: Callable)
.onFocus(fn: Callable)
.onBlur(fn: Callable)
.onMount(fn: Callable)
.onUnmount(fn: Callable)

# ── Escape Hatch (use sparingly, emits ZOLT-1600 warning) ─────────
.css(**props)                   # raw CSS: .css(background_color="#FF0000")
```

**Real usage examples:**

```python
# A complete hero section — zero CSS knowledge required
Flex(direction="col", align="center", gap=6).p(20).add(
    Heading("Ship faster.").size("7xl").weight("black").tracking("tight")
        .text_color("text").animate(slide_up(duration=0.9)),
    Text("Build in Python. Deploy everywhere.").size("xl").text_color("text-muted")
        .max_width("600px").text_align("center").animate(fade_in(delay=0.3)),
    Flex(gap=4).animate(slide_up(delay=0.5)).add(
        Button("Get started").color("primary").size("lg").shadow("md"),
        Button("See examples").color("ghost").size("lg"),
    )
)

# A stat card — expressive, readable
Card().p(6).shadow("lg").radius("xl").border(True).hover_lift(True).add(
    Flex(justify="between", align="center").mb(4).add(
        Text("Total Revenue").size("sm").text_color("text-muted"),
        Badge("↗ 12%", color="success"),
    ),
    Heading("$128,420").size("3xl").weight("bold")
        .animate(counter(start=0, end=128420, prefix="$", duration=2.0)),
    Text("vs $114,600 last month").size("xs").text_color("text-subtle").mt(1),
)

# Responsive grid
Grid(cols=1, gap=6).on("md").grid(cols=2).on("lg").grid(cols=3).add(
    *[FeatureCard(f) for f in features]
)

# Dark mode override
Flex(direction="col", gap=4).bg("surface").dark().bg("surface-2").p(6).radius("xl").add(
    Text("Dashboard").size("lg").weight("semi"),
    Text("Welcome back").text_color("text-muted"),
)
```

### 6.2 Theme API

```python
from zolt.style import Theme, DARK_TOKENS

class MyApp(App):
    # Use a built-in theme
    theme = "dark"              # "light"|"dark"|"ocean"|"forest"|"sunset"|"rose"|"midnight"|"terminal"

    # Or fully custom
    theme = Theme(
        primary       = "#FF5C1A",
        primary_hover = "#E54D10",
        primary_fg    = "#FFFFFF",
        background    = "#FAFAF8",
        surface       = "#F5F5F3",
        text          = "#1A1A1A",
        font_sans     = "Geist, Inter, sans-serif",
        radius_md     = "10px",
        shadow_md     = "0 4px 12px rgba(0,0,0,0.08)",
        dark = DarkTheme(       # optional dark mode overrides
            background = "#0C0C0A",
            surface    = "#141412",
        )
    )

    # Runtime theme switching
    current_theme = reactive("light")

    @classmethod
    def toggle_theme(cls):
        cls.current_theme.set("dark" if cls.current_theme.get() == "light" else "light")
```

**Eight built-in themes:**

| Name | Primary | Background | Character |
|---|---|---|---|
| `light` | #6C63FF | #FFFFFF | Clean modern default |
| `dark` | #7C73FF | #09090B | Deep obsidian |
| `ocean` | #0EA5E9 | #F0F9FF | Calm, professional |
| `forest` | #10B981 | #F0FDF4 | Natural, fresh |
| `sunset` | #F97316 | #FFF7ED | Warm, energetic |
| `rose` | #F43F5E | #FFF1F2 | Bold, expressive |
| `midnight` | #7C3AED | #0D0D1A | Dark purple luxury |
| `terminal` | #00FF88 | #0A0A0A | Developer aesthetic |

---

## 7. Development Phases

### Phase 0 — ZoltCSS: The Styling Engine Foundation
**Duration:** 3 weeks
**This is built first. Nothing else starts until Phase 0 is complete and all tests pass.**

#### Tasks

**Week 1 — Core engine**
1. `zolt/style/tokens.py` — full token dictionary (all categories above)
2. `zolt/style/rules.py` — `StyleRule` dataclass, `token()` helper
3. `zolt/style/resolver.py` — resolvers for 8 core components: Button, Text, Heading, Flex, Grid, Box, Input, Badge, Card, Divider
4. `zolt/style/css_generator.py` — `ZoltCSSGenerator`: register → deduplicate → render CSS
5. Wire into IR: `IRNode` gains `css_classes: list[str]` field
6. Wire into web renderer: uses `node.css_classes` instead of building class strings
7. **Remove all Tailwind references** — no `pytailwindcss`, no `.tailwind.config.js`, no class strings
8. Remove all CDN `<script>` and `<link>` tags from generated HTML
9. Verify: `zolt build --web` output contains zero external URLs

**Week 2 — Cross-target generators**
1. `zolt/style/qt_generator.py` — `QtStyleGenerator`: StyleRules → QSS
2. `zolt/style/rich_generator.py` — `RichStyleGenerator`: StyleRules → Rich Style objects
3. Wire Qt5 renderer to use `QtStyleGenerator`
4. Wire Qt6 renderer to use `QtStyleGenerator`
5. Wire CLI renderer to use `RichStyleGenerator`
6. Extend resolver for remaining v1.0 components (Table, Chart, Modal, etc.)
7. Responsive system: `.on("md")` breakpoint API — generates media-scoped rules
8. Dark mode system: CSS variable swap via `[data-theme='dark']` selector

**Week 3 — Theme system + polish**
1. Theme v2 class with all 8 built-in themes
2. Runtime theme switching via `data-theme` attribute toggle
3. `zolt/style/theme.py` — theme resolver, merge with defaults
4. CI test: build output scan for any external URL — fail if found
5. CI test: CSS output size check — fail if > 15KB gzipped
6. All v1.0 tests passing with new styling system
7. Dev mode: descriptive class names. Prod mode: short atomic names
8. Build size report: `zolt build --analyze` shows CSS + JS breakdown

#### Acceptance Criteria (Phase 0 complete when ALL pass)
- [ ] `zolt build --web` produces CSS with zero Tailwind classes
- [ ] CSS file gzipped < 15KB for a 20-component app
- [ ] No external URLs in any build output
- [ ] All v1.0 component tests pass with ZoltCSS
- [ ] Same component renders correctly on web, Qt, and CLI using same StyleRules
- [ ] Dark mode works via `data-theme='dark'` attribute
- [ ] All 8 built-in themes produce correct output
- [ ] `.on("md").size("lg")` generates correct media query CSS

---

### Phase 1 — zolt-bundler: JS Build System
**Duration:** 1 week
**Prerequisite:** Phase 0 complete.

#### Tasks
1. `zolt-bundler` package — ships esbuild binaries for Win/Mac/Linux (x64 + ARM)
2. GSAP, Alpine.js, Three.js, Lottie, Rive, Spline runtime as package data assets
3. `Bundler` Python class — entry files, output path, minify flag, tree-shake flag
4. Auto-detection: compiler scans IR for `Scene3D` → include Three.js, for `animate()` → include GSAP
5. `zolt run` → dev mode bundler (fast, source maps on)
6. `zolt build` → production bundler (minified, tree-shaken, no source maps)
7. Bundle size report included in `zolt build` output
8. CI test: bundle size limits per mode (fail if exceeded)

#### Acceptance Criteria
- [ ] `zolt build` produces `app.bundle.js` with zero CDN references
- [ ] App with no animations: bundle < 20KB gzipped (Alpine only)
- [ ] App with GSAP: bundle < 130KB gzipped
- [ ] App with Three.js: bundle < 320KB gzipped
- [ ] Bundle time < 500ms for any app size

---

### Phase 2 — Animation Engine
**Duration:** 3 weeks
**Prerequisite:** Phase 0 (ZoltCSS) + Phase 1 (bundler) complete.

#### Tasks

**Week 1 — Core animations**
1. `AnimationSpec` dataclass — type, params, trigger, target_id
2. `IRNode` gains `animations: list[AnimationSpec]` field
3. All basic animations: `fade_in/out`, `slide_*`, `scale_in/out`, `blur_in/out`
4. `.animate()` method on `BaseComponent`
5. GSAP code generator: `AnimationCodegen` — walks IR animation nodes → GSAP JS
6. `prefers-reduced-motion` wrapper around all generated GSAP
7. Load trigger: animations that fire on page load

**Week 2 — Advanced animations**
1. `ScrollReveal` — IntersectionObserver + GSAP ScrollTrigger
2. `stagger()` — sequential child animation with scroll trigger
3. `Timeline` class — full GSAP timeline control
4. `PageTransition` — enter/leave on route change
5. Text animations: `typewriter`, `counter`, `word_by_word`, `char_by_char`, `scramble`
6. Continuous: `float_up`, `pulse`, `spin`, `shimmer`

**Week 3 — Interactive + special**
1. `magnetic`, `tilt_3d`, `hover_lift`, `parallax`, `cursor_follow`
2. `ScrollLinked` — CSS property linked to scroll position
3. `Lottie` component — bundled lottie-web
4. `Rive` component — bundled @rive-app/canvas
5. Qt animation bridge: translate specs to `QPropertyAnimation`
6. Animation demo page (used in docs + demo app)

#### Acceptance Criteria
- [ ] All animation types compile to correct GSAP JavaScript
- [ ] `stagger` with scroll trigger works in Chrome, Firefox, Safari
- [ ] `prefers-reduced-motion` disables all animations instantly
- [ ] Timeline chains multiple animations correctly
- [ ] Page transitions work between routes
- [ ] Counter animation displays correct final value
- [ ] Qt fade_in compiles to correct `QPropertyAnimation`

---

### Phase 3 — 3D Engine
**Duration:** 3 weeks
**Prerequisite:** Phase 2 (animations, as 3D objects animate) complete.

#### Tasks

**Week 1 — Scene foundation**
1. `Scene3DNode` in IR — camera, lights, objects, controls, animation loop
2. `Scene3D`, all geometry primitives (Sphere, Box, Torus, Cylinder, Plane, etc.)
3. All material types (Standard, Physical, Basic, Shader)
4. All light types (Ambient, Directional, Point, Spot, Hemisphere, RectArea)
5. Three.js code generator: `Scene3DCodegen` — IR → Three.js JS module
6. requestAnimationFrame loop generation
7. Responsive canvas (resizes with container, pixel ratio capped at 2)

**Week 2 — Controls, animations, assets**
1. `OrbitControls` with full configuration
2. Built-in animations: `Float`, `Rotate`, `Pulse`, `Oscillate`
3. `ParticleSystem` — configurable particles
4. `GLTFModel` — async load with Draco compression + loading state
5. Scroll-linked 3D: `ScrollLinked` applied to 3D properties
6. Environment maps: `scene.env_map("sunset")`
7. Fog: `scene.fog(color, near, far)`

**Week 3 — Spline + polish**
1. `Spline` component — local runtime bundled, event binding
2. `RoundedBox` and `Text3D` geometries
3. WebGL fallback: `Scene3D(fallback=Image(...))` for no-WebGL environments
4. Qt WebEngine 3D: verify Three.js runs inside Qt6 WebEngine
5. Performance: 60fps target on mid-range device verified with benchmark
6. 3D demo page

#### Acceptance Criteria
- [ ] Three.js scene renders correctly from Python declarations
- [ ] GLTF model loads from local path
- [ ] Spline embed renders and fires Python event handlers
- [ ] ParticleSystem renders 2000 particles at ≥ 60fps (mid-range GPU)
- [ ] 3D scene inside Qt6 WebEngine — Three.js works
- [ ] WebGL fallback renders fallback component when WebGL unavailable
- [ ] Scroll-linked 3D updates on scroll without jank

---

### Phase 4 — Zolt UI: 90 Prebuilt Components
**Duration:** 5 weeks
**Prerequisite:** Phase 2 (animations) + Phase 3 (3D, for hero with 3D variant) complete.

#### Tasks (by week)

**Week 1 — Auth (8) + Design system foundation**
- Design system tokens shared by all zolt-ui components
- `LoginPage` (3 variants), `SignupPage` (3 variants)
- `ForgotPasswordPage`, `MagicLinkPage`, `TwoFactorPage`
- `OnboardingFlow`, `ProfileSetupPage`, `AuthLayout`
- All with animations, dark mode, accessible

**Week 2 — Landing/Marketing (20)**
- `HeroSection` (8 variants — including 3D background variant)
- `FeatureGrid`, `FeatureShowcase`, `FeatureComparison`
- `PricingTable`, `PricingComparison`
- `TestimonialsGrid`, `TestimonialsCarousel`
- `LogoCloud`, `StatsRow`, `CTASection` (6 variants)
- `FAQAccordion`, `TeamGrid`, `BentoGrid`, `TimelineSection`

**Week 3 — Dashboard/App (24)**
- `AppLayout`, `Sidebar`, `Topbar`
- `StatsGrid`, `DataTable`
- All chart types (Area, Bar, Line, Donut, Heatmap)
- `ActivityFeed`, `NotificationPanel`, `CommandPalette`
- `SettingsLayout`, `BillingSection`
- `EmptyState`, `LoadingState`, `ErrorState`

**Week 4 — Forms (14) + Feedback (9)**
- All form components including `RichTextEditor` and `CodeEditor`
- `DatePicker`, `TimePicker`, `FileUpload`
- All feedback + overlay components: Toast, Modal, Drawer, Tooltip, etc.

**Week 5 — Navigation (5) + E-commerce (10) + Polish**
- All nav components
- All e-commerce components
- `zolt studio` — browser gallery showing all 90 components
- Auto-screenshot generation for docs
- Dark mode pass for all 90 components
- Accessibility audit pass for all 90 components

#### Acceptance Criteria
- [ ] All 90 components render without errors
- [ ] All 90 components pass axe-core accessibility audit
- [ ] All 90 components have correct dark mode
- [ ] All 90 components have built-in entrance animations
- [ ] `zolt studio` opens and shows all components
- [ ] `from zolt_ui import LoginPage` works in one line

---

### Phase 5 — Design Import System
**Duration:** 3 weeks
**Prerequisite:** Phase 4 (zolt-ui, for component mapping) complete.

**Week 1:** Figma importer — API client, node walker, mapper, style extractor, code generator
**Week 2:** Framer + Webflow importers
**Week 3:** Accuracy improvements, review CLI, test suite (10 real Figma files)

#### Acceptance Criteria
- [ ] `zolt import figma <url>` produces valid Python in < 30s
- [ ] Generated code compiles without errors on 90% of test files
- [ ] Layout accuracy > 85% on test suite
- [ ] Color accuracy > 90% on test suite
- [ ] `zolt import review ./output.py` guides through manual fixes

---

### Phase 6 — Desktop v1.5: Qt5 + Qt6 + WebEngine
**Duration:** 2 weeks
**Prerequisite:** Phase 4 complete.

**Tasks:**
1. PyQt5 renderer — full widget mapping
2. `zolt[qt5]` extra
3. Qt6 WebEngine mode — full Chromium in Qt window
4. Python local server for WebEngine
5. Textual TUI upgrade — interactive mode
6. Animation bridge — specs → QPropertyAnimation
7. CI: build desktop apps on Windows, macOS, Linux

#### Acceptance Criteria
- [ ] `pyui build --desktop --qt5` produces working app on Windows and Linux
- [ ] Qt6 WebEngine mode renders Three.js correctly
- [ ] Textual interactive mode: form submission works in terminal
- [ ] `zolt run --cli --static` pipes correctly to stdout

---

### Phase 7 — AI-First: Skills, Schema, LLMS.txt
**Duration:** 2 weeks
**Prerequisite:** All previous phases complete (skill files describe the real final API).

**Tasks:**
1. Skill files for 100% of public components (YAML format — see Section 9)
2. `zolt.schema.json` auto-generator from type hints + docstrings
3. `LLMS.txt` file — hand-written, tested with Claude Code
4. AI correctness benchmark — 20 test specs, Claude Code generates code, verify compiles
5. `zolt skills validate` — CI check that all skill files are complete
6. VS Code extension v1.5 — schema-powered autocomplete + error squiggles
7. Error code documentation page on docs site

#### Acceptance Criteria
- [ ] Skill files for 100% of public API surface
- [ ] `zolt.schema.json` covers all props with types
- [ ] AI benchmark: > 95% of Claude Code generated apps compile on first attempt
- [ ] VS Code extension shows inline docs for all props

---

### Phase 8 — Docs Website (built entirely with Zolt)
**Duration:** 3 weeks
**Prerequisite:** Phase 7 complete.

The docs site is the ultimate test of the framework. It uses every feature — animations, 3D hero, Zolt UI components, dark mode, responsive layout. It is deployed on Vercel. See Section 10 for full spec.

**Week 1:** Information architecture, all content written, code examples tested
**Week 2:** Design implementation — dark editorial aesthetic, 3D hero, animation showcase
**Week 3:** Component gallery, AI usage page, deploy to Vercel, Lighthouse >95

#### Acceptance Criteria
- [ ] `zolt.dev` live and serving
- [ ] Lighthouse: Performance >95, Accessibility >97, Best Practices >95, SEO >95
- [ ] Source code in `zolt-framework/docs-site/` (publicly visible)
- [ ] Dark mode works on all pages
- [ ] All 90 Zolt UI components shown in live gallery
- [ ] Search works (Algolia DocSearch)

---

### Phase 9 — Demo Artifacts (.exe + CLI Demo)
**Duration:** 2 weeks
**Prerequisite:** Phase 8 complete.

See Section 11 for full spec.

**Tasks:**
1. 8-section demo app built with Zolt
2. `zolt build --desktop --qt6-webengine` → binaries for all platforms
3. Code-signing: macOS notarisation, Windows Authenticode
4. `zolt demo` CLI command — Textual interactive showcase
5. GitHub Release with all platform binaries

#### Acceptance Criteria
- [ ] Windows `.exe` < 130MB, opens and runs correctly
- [ ] macOS `.app` opens on macOS 12+
- [ ] Linux `.deb` installs on Ubuntu 22.04+
- [ ] `zolt demo` CLI shows interactive showcase
- [ ] All 8 demo sections work correctly

---

### Phase 10 — Production Hardening & Launch
**Duration:** 2 weeks

1. Lighthouse CI — all examples > 90, fail on regression
2. Axe accessibility CI — all zolt-ui components pass
3. Cross-browser Playwright tests — Chrome, Firefox, Safari, Edge
4. Bundle size CI — fail if thresholds exceeded
5. AI benchmark CI — runs on every release candidate
6. Security: scan zolt-bundler JS for known vulnerabilities
7. Load test: dev server with 100 concurrent hot-reload connections
8. `CHANGELOG.md` — complete release notes
9. PyPI: `zolt-framework==1.5.0` + `zolt-ui==1.5.0`
10. Launch: HN Show HN, Reddit, demo video, blog post

---

## 8. Unit Test Plan — Per Phase

### Phase 0 — ZoltCSS Tests

```python
# tests/v1_5/test_zoltcss/test_tokens.py

def test_all_required_tokens_present():
    from zolt.style.tokens import TOKENS
    required = [
        "color-primary", "color-bg", "color-text", "color-border",
        "space-4", "space-8", "font-size-base", "font-size-2xl",
        "radius-md", "shadow-md", "ease-normal"
    ]
    for key in required:
        assert key in TOKENS, f"Missing token: {key}"

def test_dark_tokens_are_subset_of_tokens():
    from zolt.style.tokens import TOKENS, DARK_TOKENS
    for key in DARK_TOKENS:
        assert key in TOKENS, f"Dark token '{key}' not in base tokens"

# tests/v1_5/test_zoltcss/test_resolver.py

def test_button_primary_has_background_rule():
    from zolt.style.resolver import StyleResolver
    resolver = StyleResolver()
    rules = resolver.button(color="primary")
    props = {r.prop: r.value for r in rules if not r.pseudo and not r.state}
    assert "background-color" in props
    assert "var(--z-color-primary)" in props["background-color"]

def test_button_hover_rule_exists():
    from zolt.style.resolver import StyleResolver
    rules = StyleResolver().button(color="primary")
    hover = [r for r in rules if r.pseudo == ":hover"]
    assert len(hover) > 0

def test_button_disabled_state_rules():
    from zolt.style.resolver import StyleResolver
    rules = StyleResolver().button()
    disabled = [r for r in rules if r.state == "disabled"]
    assert any(r.prop == "opacity" for r in disabled)
    assert any(r.prop == "cursor" for r in disabled)

def test_button_focus_visible_accessibility():
    from zolt.style.resolver import StyleResolver
    rules = StyleResolver().button()
    focus = [r for r in rules if r.pseudo == ":focus-visible"]
    assert any(r.prop == "outline" for r in focus), "Button must have focus ring"

def test_text_resolver_all_props():
    from zolt.style.resolver import StyleResolver
    rules = StyleResolver().text(size="xl", weight="bold", color="primary")
    props = {r.prop for r in rules}
    assert "font-size" in props
    assert "font-weight" in props
    assert "color" in props

def test_flex_resolver():
    from zolt.style.resolver import StyleResolver
    rules = StyleResolver().flex(direction="col", align="center", gap=4)
    props = {r.prop: r.value for r in rules}
    assert props["display"] == "flex"
    assert props["flex-direction"] == "col"
    assert props["align-items"] == "center"
    assert "space-4" in props["gap"]

def test_responsive_wraps_in_media_query():
    from zolt.style.resolver import StyleResolver
    from zolt.style.rules import StyleRule
    resolver = StyleResolver()
    rules = [StyleRule("font-size","var(--z-font-size-xl)")]
    responsive = resolver.responsive(rules, "md")
    assert all(r.media == "@media (min-width: 768px)" for r in responsive)

# tests/v1_5/test_zoltcss/test_generator.py

def test_generator_produces_root_vars():
    from zolt.style.css_generator import ZoltCSSGenerator
    from zolt.style.tokens import TOKENS, DARK_TOKENS
    gen = ZoltCSSGenerator(TOKENS, DARK_TOKENS)
    css = gen.render()
    assert ":root {" in css
    assert "--z-color-primary:" in css
    assert "--z-font-size-base:" in css

def test_generator_deduplicates_rules():
    from zolt.style.css_generator import ZoltCSSGenerator
    from zolt.style.rules import StyleRule
    from zolt.style.tokens import TOKENS, DARK_TOKENS
    gen = ZoltCSSGenerator(TOKENS, DARK_TOKENS)
    rule = StyleRule("display", "flex")
    names1 = gen.register([rule])
    names2 = gen.register([rule])
    # Same rule → same class name
    assert names1 == names2
    css = gen.render()
    # Should appear exactly once
    assert css.count(f"display: flex") == 1

def test_dark_mode_token_override():
    from zolt.style.css_generator import ZoltCSSGenerator
    from zolt.style.tokens import TOKENS, DARK_TOKENS
    gen = ZoltCSSGenerator(TOKENS, DARK_TOKENS)
    css = gen.render()
    assert "[data-theme='dark']" in css
    assert "--z-color-bg:" in css

def test_no_external_urls_in_output():
    """Critical: no CDN references in any build output."""
    from zolt.style.css_generator import ZoltCSSGenerator
    from zolt.style.tokens import TOKENS, DARK_TOKENS
    gen = ZoltCSSGenerator(TOKENS, DARK_TOKENS)
    css = gen.render()
    assert "tailwindcss.com" not in css
    assert "unpkg.com" not in css
    assert "cdn." not in css

def test_css_size_within_target(tmp_path, simple_app):
    """Gzipped CSS must be under 15KB for a 20-component app."""
    import gzip, subprocess
    result = subprocess.run(["zolt","build","--web","--out",str(tmp_path)], cwd=simple_app)
    assert result.returncode == 0
    css = (tmp_path / "zolt.min.css").read_bytes()
    assert len(gzip.compress(css)) < 15_000, "CSS too large"

# tests/v1_5/test_zoltcss/test_qt_generator.py

def test_qt_generator_resolves_tokens():
    from zolt.style.qt_generator import QtStyleGenerator
    from zolt.style.rules import StyleRule
    from zolt.style.tokens import TOKENS
    gen = QtStyleGenerator(TOKENS)
    rules = [StyleRule("background-color", "var(--z-color-primary)")]
    qss = gen.to_qss("QPushButton", rules)
    assert "#6C63FF" in qss or "6C63FF" in qss.upper()
    assert "QPushButton" in qss

def test_same_rules_produce_correct_qt_and_css():
    from zolt.style.resolver import StyleResolver
    from zolt.style.css_generator import ZoltCSSGenerator
    from zolt.style.qt_generator import QtStyleGenerator
    from zolt.style.tokens import TOKENS, DARK_TOKENS

    resolver = StyleResolver()
    rules = resolver.button(color="primary", size="md")

    css_gen = ZoltCSSGenerator(TOKENS, DARK_TOKENS)
    css_gen.register(rules)
    css = css_gen.render()
    assert "var(--z-color-primary)" in css

    qt_gen = QtStyleGenerator(TOKENS)
    qss = qt_gen.to_qss("QPushButton", rules)
    assert "#6C63FF" in qss or "6C63FF" in qss.upper()
```

### Phase 1 — Bundler Tests

```python
def test_bundler_produces_single_file(tmp_path):
    from zolt.build.bundler import Bundler
    b = Bundler(entries=["alpine"], output=str(tmp_path / "out.js"), minify=True)
    b.run()
    assert (tmp_path / "out.js").exists()

def test_no_cdnurls_in_bundle(tmp_path):
    from zolt.build.bundler import Bundler
    b = Bundler(entries=["alpine","gsap"], output=str(tmp_path / "out.js"))
    b.run()
    content = (tmp_path / "out.js").read_text()
    assert "unpkg.com" not in content
    assert "cdnjs" not in content

def test_threejs_excluded_when_not_used(tmp_path, simple_app_no_3d):
    # App with no Scene3D — Three.js should not be in bundle
    result = subprocess.run(["zolt","build","--web","--out",str(tmp_path)], cwd=simple_app_no_3d)
    bundle = (tmp_path / "app.bundle.js").read_text()
    assert "THREE.Scene" not in bundle
```

### Phase 2 — Animation Tests

```python
def test_fade_in_compiles_to_gsap():
    from zolt import Button
    from zolt.animate import fade_in
    from zolt.renderers.web.animation_codegen import AnimationCodegen

    btn = Button("Click").animate(fade_in(duration=0.6, delay=0.2))
    ir = build_ir_node(btn)
    js = AnimationCodegen().generate(ir)
    assert "gsap.from" in js
    assert "opacity: 0" in js
    assert "duration: 0.6" in js
    assert "delay: 0.2" in js

def test_reduced_motion_wrapper_present():
    from zolt import Heading
    from zolt.animate import slide_up
    from zolt.renderers.web.animation_codegen import AnimationCodegen

    h = Heading("Hi").animate(slide_up())
    ir = build_ir_node(h)
    js = AnimationCodegen().generate(ir)
    assert "prefers-reduced-motion" in js
    assert "matchMedia" in js

def test_scroll_trigger_generated():
    from zolt import Grid
    from zolt.animate import stagger, slide_up
    from zolt.renderers.web.animation_codegen import AnimationCodegen

    g = Grid(cols=3).animate(stagger(each=slide_up(duration=0.7), interval=0.12, trigger="scroll"))
    ir = build_ir_node(g)
    js = AnimationCodegen().generate(ir)
    assert "ScrollTrigger" in js
    assert "stagger: 0.12" in js

def test_counter_animation():
    from zolt import Text
    from zolt.animate import counter
    from zolt.renderers.web.animation_codegen import AnimationCodegen

    t = Text("0").animate(counter(start=0, end=1000, duration=2.0, prefix="$"))
    ir = build_ir_node(t)
    js = AnimationCodegen().generate(ir)
    assert "1000" in js
    assert "$" in js

def test_timeline_sequences_correctly():
    from zolt import Heading, Text
    from zolt.animate import fade_in, slide_up, Timeline

    tl = (Timeline()
        .add(Heading("H"), fade_in(duration=0.5))
        .add(Text("T"),    slide_up(duration=0.7), offset="-=0.3")
        .play_on("load"))

    from zolt.renderers.web.animation_codegen import AnimationCodegen
    js = AnimationCodegen().generate_timeline(tl)
    assert "gsap.timeline" in js
    assert '"-=0.3"' in js
```

### Phase 3 — 3D Engine Tests

```python
def test_scene3d_renders_canvas():
    from zolt.three import Scene3D, Sphere, AmbientLight
    from zolt.renderers.web import render_component
    scene = Scene3D(height="400px").add(AmbientLight(), Sphere(radius=1))
    html = render_component(scene)
    assert "<canvas" in html

def test_scene3d_generates_threejs():
    from zolt.three import Scene3D, Box, PointLight
    from zolt.renderers.web.scene3d_codegen import Scene3DCodegen
    scene = Scene3D().add(PointLight(), Box(width=1))
    ir = build_scene_ir(scene)
    js = Scene3DCodegen().generate(ir)
    assert "THREE.Scene()" in js
    assert "THREE.BoxGeometry" in js
    assert "THREE.PointLight" in js
    assert "requestAnimationFrame" in js

def test_webgl_fallback_renders_fallback():
    from zolt.three import Scene3D
    from zolt import Image
    from zolt.renderers.web import render_component
    scene = Scene3D(fallback=Image(src="/fb.png")).add()
    html = render_component(scene)
    assert "/fb.png" in html

def test_particle_system_count_correct():
    from zolt.three import Scene3D, ParticleSystem
    from zolt.renderers.web.scene3d_codegen import Scene3DCodegen
    scene = Scene3D().add(ParticleSystem(count=500))
    js = Scene3DCodegen().generate(build_scene_ir(scene))
    assert "500" in js
```

### Phase 4 — Zolt UI Tests

```python
def test_all_90_components_render_without_error():
    """Smoke test — every component renders with default props."""
    from zolt.renderers.web import render_component
    import zolt_ui, inspect
    errors = []
    for cat in ["auth","landing","dashboard","ecommerce","forms","feedback","navigation"]:
        module = __import__(f"zolt_ui.{cat}", fromlist=["*"])
        for name in dir(module):
            cls = getattr(module, name)
            if inspect.isclass(cls) and hasattr(cls, "compose"):
                try:
                    html = render_component(cls())
                    assert len(html) > 20
                except Exception as e:
                    errors.append(f"{name}: {e}")
    assert not errors, "Failed:\n" + "\n".join(errors)

def test_login_page_all_variants():
    from zolt_ui.auth import LoginPage
    from zolt.renderers.web import render_component
    for variant in ["centered","split","minimal"]:
        html = render_component(LoginPage(variant=variant))
        assert "email" in html.lower()
        assert "password" in html.lower()

def test_pricing_table_renders_plans():
    from zolt_ui.landing import PricingTable
    from zolt.renderers.web import render_component
    plans = [{"name":"Free","price":0},{"name":"Pro","price":29}]
    html = render_component(PricingTable(plans=plans))
    assert "Free" in html and "Pro" in html

def test_all_components_have_focus_ring_in_css():
    """Every interactive component must have a visible focus ring."""
    from zolt.style.resolver import StyleResolver
    interactive = ["button","input"]
    resolver = StyleResolver()
    for comp in interactive:
        rules = getattr(resolver, comp)()
        focus_rules = [r for r in rules if r.pseudo in (":focus",":focus-visible")]
        assert focus_rules, f"{comp} missing focus styles"
        has_outline = any(r.prop == "outline" for r in focus_rules)
        assert has_outline, f"{comp} focus missing 'outline' rule"
```

### Phase 7 — AI Skills Tests

```python
def test_all_public_components_have_skill_files():
    from pathlib import Path
    import zolt
    skills_dir = Path(zolt.__file__).parent / "skills"
    required = ["Button","Text","Heading","Page","App","Grid","Flex",
                "Stack","Input","Card","Scene3D","Spline","Lottie"]
    for name in required:
        assert (skills_dir / f"{name}.yaml").exists(), f"Missing: {name}.yaml"

def test_skill_files_have_required_keys():
    import yaml
    from pathlib import Path
    import zolt
    required = ["name","description","props","examples","common_patterns","anti_patterns"]
    for f in (Path(zolt.__file__).parent / "skills").glob("*.yaml"):
        data = yaml.safe_load(f.read_text())
        for k in required:
            assert k in data, f"{f.name} missing: {k}"

def test_schema_covers_all_classes():
    import json
    from pathlib import Path
    import zolt
    schema = json.loads((Path(zolt.__file__).parent / "schema.json").read_text())
    for cls in ["App","Page","Button","Text","Heading","Grid","Flex","Scene3D"]:
        assert cls in schema["classes"], f"Missing from schema: {cls}"

def test_error_messages_are_actionable():
    from zolt.compiler.validator import validate_app
    from zolt import App, Button
    class BadApp(App):
        home_page = None
    errors = validate_app(BadApp)
    if errors:
        for e in errors:
            assert hasattr(e, "code"), "Error missing code"
            assert hasattr(e, "suggestion"), "Error missing suggestion"
```

---

## 9. AI Skills System — Full Specification

### Skill File Format

```yaml
# zolt/skills/Button.yaml

name: Button
version: "1.5.0"
category: input
since: "1.0.0"
description: >
  Interactive button. Renders as HTML <button> (web), QPushButton (Qt),
  or a styled action in Textual CLI. All styling through methods — zero CSS.

props:
  label:
    type: str
    required: true
    description: Text displayed in the button.
    example: '"Get started"'

  color:
    type: "Literal['primary','secondary','ghost','outline','danger','success','link']"
    required: false
    default: '"primary"'
    description: Visual variant. Uses theme tokens — changes with theme.

  size:
    type: "Literal['2xs','xs','sm','md','lg','xl']"
    required: false
    default: '"md"'

  radius:
    type: "Literal['none','sm','md','lg','xl','2xl','full']"
    required: false
    default: '"md"'

  shadow:
    type: "Literal['none','xs','sm','md','lg','xl']"
    required: false
    default: '"none"'

  full_width:
    type: bool
    required: false
    default: "False"
    description: Stretches to fill container width.

  icon:
    type: "str | None"
    required: false
    description: Lucide icon name. See lucide.dev.

  loading:
    type: "bool | ReactiveVar[bool]"
    required: false
    default: "False"
    description: Shows spinner and disables pointer events.

  disabled:
    type: "bool | ReactiveVar[bool]"
    required: false
    default: "False"

methods:
  onClick:
    returns: Button
    args: "handler: Callable[[], None | Awaitable[None]]"
    description: Handler called on click. Supports async.

  animate:
    returns: Button
    args: "spec: AnimationSpec"
    description: Entrance animation.
    example: '.animate(slide_up(duration=0.5, delay=0.3))'

examples:
  minimal: |
    Button("Get started")

  primary_with_size: |
    Button("Continue").color("primary").size("lg")

  with_icon: |
    Button("Next").icon("arrow-right").color("primary").size("md")

  async_loading: |
    submitting = reactive(False)
    async def handle():
        submitting.set(True)
        await do_work()
        submitting.set(False)
    Button("Submit").loading(submitting).onClick(handle)

  cta_pair: |
    Flex(gap=3).add(
        Button("Get started").color("primary").size("lg"),
        Button("Learn more").color("ghost").size("lg"),
    )

  animated: |
    Button("Start").color("primary").size("xl").shadow("md")
        .animate(slide_up(duration=0.5, delay=0.8))

common_patterns:
  - name: CTA pair (hero sections)
    code: |
      Flex(gap=4).add(
          Button("Start free").color("primary").size("lg"),
          Button("See demo").color("ghost").size("lg"),
      )

  - name: Async submit button
    code: |
      loading = reactive(False)
      async def submit():
          loading.set(True)
          await api.save(data)
          loading.set(False)
      Button("Save").loading(loading).onClick(submit)

  - name: Danger confirmation
    code: |
      Button("Delete account").color("danger").size("md")
          .onClick(show_confirm_dialog)

anti_patterns:
  - wrong: 'Button("X").css(background_color="#6C63FF")'
    correct: 'Button("X").color("primary")'
    reason: "Raw CSS bypasses theming and dark mode."

  - wrong: 'Button("X", size="large")'
    correct: 'Button("X").size("lg")'
    reason: '"large" is not a valid size. Use "lg".'

targets:
  web: full
  desktop_qt5: full
  desktop_qt6: full
  desktop_tk: partial
  cli_textual: full
  cli_rich: basic

related: [IconButton, ButtonGroup, LinkButton]
```

### LLMS.txt (published at `zolt.dev/llms.txt`)

```
# Zolt Framework v1.5 — AI-Readable API Summary
# Full schema: https://zolt.dev/schema.json
# Skill files: https://zolt.dev/skills/

## NON-NEGOTIABLE RULES
1. Never use .css() for colors — use .color(), .bg(), .text_color() with token names
2. Never write CSS class strings — every style is a Python method
3. Sizes are always: "2xs"|"xs"|"sm"|"md"|"lg"|"xl" — same for every component
4. Color tokens: "primary"|"secondary"|"danger"|"success"|"text"|"text-muted"|"border"
5. Radius tokens: "none"|"sm"|"md"|"lg"|"xl"|"2xl"|"full"
6. Shadow tokens: "none"|"xs"|"sm"|"md"|"lg"|"xl"|"2xl"
7. Spacing uses integers 0-64 mapped to the 4px/8px grid (e.g. .p(4) = 16px padding)
8. Animations: always import from zolt.animate — never write JavaScript
9. 3D: always import from zolt.three — never write Three.js manually
10. Event handlers: onClick, onChange, onSubmit, onHover — same names everywhere

## MINIMAL APP
from zolt import App, Page, Heading, Text, Button

class MyApp(App):
    home = Page(title="Home", route="/")
    home.add(
        Heading("Hello World").size("4xl").weight("bold"),
        Text("Built with Zolt.").text_color("text-muted"),
        Button("Get started").color("primary").size("lg"),
    )

## ANIMATED APP
from zolt import App, Page, Flex, Heading, Button
from zolt.animate import slide_up, fade_in, stagger

class AnimApp(App):
    home = Page(title="Home", route="/")
    home.add(
        Flex(direction="col", align="center", gap=6).p(20).add(
            Heading("Ship faster.").size("7xl").weight("black")
                .animate(slide_up(duration=0.9)),
            Button("Start").color("primary").size("xl")
                .animate(fade_in(delay=0.4)),
        )
    )

## WITH 3D
from zolt.three import Scene3D, Torus, PointLight, OrbitControls, Float

class ThreeDApp(App):
    home = Page(title="3D")
    home.add(
        Scene3D(height="500px").add(
            PointLight(intensity=1.0, position=(5,5,5)),
            Mesh(geometry=Torus(radius=1), material={"color":"#6C63FF"})
                .animate(Float(speed=1.5)),
        ).controls(OrbitControls(auto_rotate=True))
    )

## WITH PREBUILT COMPONENTS (zolt-ui)
from zolt_ui.auth import LoginPage
from zolt_ui.landing import HeroSection, PricingTable

class SaaSApp(App):
    home = Page(route="/")
    home.add(
        HeroSection(title="My Product", variant="centered"),
        PricingTable(plans=plans),
    )
    login = LoginPage(providers=["google"], on_success=go_to_dashboard)

## RESPONSIVE STYLING
# Use .on("breakpoint") to scope styles to screen sizes
Grid(cols=1, gap=4).on("md").grid(cols=2).on("lg").grid(cols=3)
Text("Hi").size("base").on("lg").font_size("xl")

## DARK MODE
# Automatic: set App.theme = "dark"
# Manual override per-component:
Card().bg("surface").dark().bg("surface-2")

## IMPORT FROM FIGMA
# In terminal: zolt import figma https://figma.com/file/ABC123/Design
# Produces: components/design.py — review before using in production
```

---

## 10. Docs Website Specification

**URL:** `zolt.dev`
**Built with:** Zolt v1.5 — every feature used in the site itself
**Deployed:** Vercel via `zolt build --web`

### Design Language

Deep obsidian background (`#09090B`), phosphor green accents (`#00FF88`), chalk white typography. JetBrains Mono for code and labels, Playfair Display for editorial headlines, Geist for body. Same as the `terminal` theme from Zolt.

### Page Architecture

```
/ (homepage)
├── Hero             — Three.js particle field, animated headline, pip install block
├── Code demo        — Python left | rendered output right (live, interactive tabs)
├── Animation demo   — all animation types in scrolling cards
├── 3D demo          — live Three.js scene, Spline embed, particle system
├── Zolt UI gallery  — 12 component previews with hover animation
├── Design import    — before/after: Figma → Zolt code
├── AI section       — "Claude Code writes this on the first try"
└── CTA              — pip install + GitHub stars

/docs/getting-started/installation
/docs/getting-started/your-first-app
/docs/getting-started/concepts

/docs/design-system/tokens
/docs/design-system/theming
/docs/design-system/dark-mode
/docs/design-system/responsive

/docs/components/[name]          (90+ pages, one per component)
/docs/animate/[animation-name]
/docs/3d/scene3d
/docs/3d/spline
/docs/3d/particles
/docs/import/figma
/docs/ai/skill-files
/docs/ai/schema
/docs/deployment/vercel
/docs/deployment/desktop

/components                      (live gallery — all 90 zolt-ui components)
/errors                          (every ZOLT-XXXX error code)
/changelog
/showcase                        (community builds)
```

### Lighthouse Targets
Performance >95 · Accessibility >97 · Best Practices >95 · SEO >95

---

## 11. Demo Artifacts Specification

### Desktop Demo App — 8 Sections

1. **Welcome** — Full-screen particle system + animated headline + `pip install` block
2. **ZoltCSS** — Theme switcher with live re-render; all 8 themes side by side
3. **Components** — All 90 Zolt UI components with code toggle
4. **Animation** — Every animation type with duration/ease sliders
5. **3D** — Interactive Three.js scene, Spline embed, GLTF viewer, scroll-linked 3D
6. **Design Import** — Figma JSON input → Zolt code → rendered output
7. **AI Usage** — Live: type a spec, watch Claude Code generate valid Zolt
8. **Build Output** — Real-time bundle size, Lighthouse scores, output files

**Distribution:**

| Platform | Format | Size target |
|---|---|---|
| Windows | `ZoltDemo-1.5.0-win64.exe` | < 130MB |
| macOS | `ZoltDemo-1.5.0-macos.dmg` | < 140MB |
| Linux | `ZoltDemo-1.5.0-amd64.deb` | < 120MB |

### `zolt demo` CLI Command

```
$ zolt demo

╔══════════════════════════════════╗
║   Zolt v1.5 — Interactive Demo   ║
╚══════════════════════════════════╝

  ▸ 1. ZoltCSS — the styling engine
    2. Animation system
    3. 3D capabilities
    4. Zolt UI components
    5. Design import (Figma)
    6. AI usage with skill files
    7. Build a mini app live
    8. Exit
```

---

## 12. File & Folder Structure v1.5

```
zolt/
├── pyproject.toml
├── LLMS.txt                              # AI-readable API summary
├── CHANGELOG.md
│
├── src/
│   └── zolt/
│       ├── __init__.py
│       ├── exceptions.py                  # ZOLT-1500 to ZOLT-1599
│       ├── app.py
│       ├── page.py
│       │
│       ├── style/                         # ← LAYER 1: ZoltCSS (built first)
│       │   ├── __init__.py
│       │   ├── tokens.py                  # All design tokens
│       │   ├── rules.py                   # StyleRule dataclass
│       │   ├── resolver.py                # Component prop → StyleRule lists
│       │   ├── css_generator.py           # ZoltCSSGenerator → zolt.min.css
│       │   ├── qt_generator.py            # StyleRules → QSS
│       │   ├── rich_generator.py          # StyleRules → Rich Style objects
│       │   └── theme.py                   # Theme class + 8 built-in themes
│       │
│       ├── build/                         # ← LAYER 2: JS Bundler
│       │   ├── bundler.py                 # zolt-bundler Python wrapper
│       │   ├── pipeline.py                # Orchestrates full build
│       │   └── analyzer.py               # Bundle size report
│       │
│       ├── animate/                       # ← LAYER 3: Animation Engine
│       │   ├── __init__.py                # All animation functions
│       │   ├── specs.py                   # AnimationSpec dataclass
│       │   ├── timeline.py                # Timeline class
│       │   ├── scroll.py                  # ScrollReveal, ScrollLinked
│       │   ├── interactive.py             # magnetic, tilt_3d, parallax
│       │   ├── text.py                    # typewriter, counter, word_by_word
│       │   ├── continuous.py             # float_up, pulse, spin, shimmer
│       │   ├── lottie.py                  # Lottie component
│       │   └── rive.py                    # Rive component
│       │
│       ├── three/                         # ← LAYER 4: 3D Engine
│       │   ├── __init__.py
│       │   ├── scene.py                   # Scene3D
│       │   ├── geometry.py                # All geometry types
│       │   ├── material.py                # All material types
│       │   ├── lights.py                  # All light types
│       │   ├── controls.py                # OrbitControls etc.
│       │   ├── particles.py               # ParticleSystem
│       │   ├── loaders.py                 # GLTFModel
│       │   └── builtin_anims.py           # Float, Rotate, Pulse
│       ├── spline.py                      # Spline component
│       │
│       ├── components/                    # Base components (upgraded from v1.0)
│       │   ├── base.py                    # BaseComponent — all style methods
│       │   ├── layout/
│       │   ├── navigation/
│       │   ├── input/
│       │   ├── display/
│       │   ├── feedback/
│       │   └── data/
│       │
│       ├── import_tools/                  # ← LAYER 6: Design Import
│       │   ├── figma/
│       │   ├── framer/
│       │   └── webflow/
│       │
│       ├── compiler/
│       │   ├── ir.py                      # IRNode + AnimationNode + Scene3DNode
│       │   ├── discovery.py
│       │   ├── walker.py
│       │   └── validator.py               # ZOLT-1500+ error codes
│       │
│       ├── renderers/
│       │   ├── web/
│       │   │   ├── generator.py
│       │   │   ├── animation_codegen.py   # AnimationSpec → GSAP JS
│       │   │   └── scene3d_codegen.py     # Scene3DNode → Three.js JS
│       │   ├── desktop/
│       │   │   ├── tkinter_renderer.py
│       │   │   ├── qt5_renderer.py        # NEW
│       │   │   ├── qt6_renderer.py
│       │   │   └── qt6_webengine.py       # NEW
│       │   └── cli/
│       │       ├── rich_renderer.py
│       │       └── textual_renderer.py    # NEW
│       │
│       ├── schema/                        # ← LAYER 9: AI Compatibility
│       │   ├── generator.py               # zolt.schema.json generator
│       │   └── validator.py
│       │
│       ├── skills/                        # ← LAYER 9: Skill Files
│       │   ├── Button.yaml
│       │   ├── Text.yaml
│       │   ├── Heading.yaml
│       │   ├── Page.yaml
│       │   ├── App.yaml
│       │   ├── Grid.yaml
│       │   ├── Flex.yaml
│       │   ├── Scene3D.yaml
│       │   ├── Spline.yaml
│       │   ├── Lottie.yaml
│       │   └── ... (one per public component/function)
│       │
│       ├── state/                         # v1.0 unchanged
│       ├── server/                        # v1.0 unchanged
│       ├── hotreload/                     # v1.0 unchanged
│       ├── plugins/                       # v1.0 unchanged
│       └── cli/
│           ├── main.py
│           └── commands/
│               ├── run.py, build.py, new.py
│               ├── import_cmd.py          # zolt import figma/framer/webflow
│               ├── studio.py             # zolt studio
│               └── demo.py               # zolt demo
│
├── zolt-ui/                               # ← LAYER 5: Separate Package
│   ├── pyproject.toml
│   └── src/zolt_ui/
│       ├── auth/
│       ├── landing/
│       ├── dashboard/
│       ├── ecommerce/
│       ├── forms/
│       ├── feedback/
│       └── navigation/
│
├── docs-site/                             # ← LAYER 8: Built with Zolt
│   ├── app.py
│   └── pages/
│
├── tests/
│   ├── v1/                                # All v1.0 tests — must pass
│   └── v1_5/
│       ├── test_zoltcss/
│       ├── test_bundler/
│       ├── test_animate/
│       ├── test_three/
│       ├── test_zolt_ui/
│       ├── test_import/
│       ├── test_desktop/
│       ├── test_ai/
│       └── integration/
│
└── examples/v1_5/
    ├── basic-animated-landing/
    ├── 3d-product-hero/
    ├── dashboard-from-prebuilts/
    ├── figma-imported-landing/
    └── full-saas-site/
```

---

## 13. Dependencies & Versions

### Core Runtime — No New External CSS Dependencies

| Package | Version | Purpose |
|---|---|---|
| `textual` | >=0.62 | Interactive TUI renderer |
| `lxml` | >=5.0 | HTML parsing for design import |
| `beautifulsoup4` | >=4.12 | HTML parsing |
| `httpx` | >=0.27 | Figma API calls |
| `PyYAML` | >=6.0 | Skill file parsing |
| `Pillow` | >=10.0 | Image optimisation |

**Removed:** `pytailwindcss` — no longer needed. ZoltCSS generates all CSS natively in Python.

### Optional Extras

| Extra | Packages | Unlocks |
|---|---|---|
| `[web]` | `zolt-bundler` | Full web build with JS bundling |
| `[qt5]` | `PyQt5>=5.15`, `sip>=6.0` | Qt5 desktop |
| `[qt6]` | `PyQt6>=6.6` | Qt6 desktop |
| `[qt6-webengine]` | `PyQt6-WebEngine>=6.6` | Qt6 + full browser |
| `[import]` | `httpx`, `lxml`, `beautifulsoup4` | Figma/Framer/Webflow import |
| `[all]` | Everything | All features |

### Bundled JS (via `zolt-bundler`, never installed by user)

| Library | Version | Gzipped | Included when |
|---|---|---|---|
| Alpine.js | 3.14 | ~15KB | Always |
| GSAP + ScrollTrigger | 3.12 | ~50KB | `.animate()` used |
| Three.js | r169 | ~160KB | `Scene3D` used |
| Lottie-web | 5.12 | ~65KB | `Lottie` used |
| @rive-app/canvas | 2.x | ~40KB | `Rive` used |
| Spline viewer | latest | ~120KB | `Spline` used |
| Tiptap | 2.x | ~80KB | `RichTextEditor` used |

---

## 14. Migration Guide — v1.0 → v1.5

### Zero breaking changes. All v1.0 code works unchanged.

### Install

```bash
pip install --upgrade zolt-framework
pip install zolt[web]           # Required for production web builds
pip install zolt-ui             # Optional — 90 prebuilt components
```

### What changes automatically

- `zolt build --web` now generates `zolt.min.css` via ZoltCSS (not Tailwind). Smaller, faster, no external dependency.
- `zolt run --web` still hot-reloads but no longer calls Tailwind CLI. Faster startup.
- `zolt run --cli` defaults to Textual interactive mode. Use `--static` for Rich output.

### What was removed

- `pytailwindcss` — removed from dependencies, no longer needed
- CDN `<script>` and `<link>` tags — removed from all generated HTML
- `.tailwind.config.js` generation — removed entirely
- `className()` method still works but now emits `[ZOLT-1600]` deprecation warning

### New opt-in capabilities

```python
# Animations — just chain .animate()
Heading("Hello").animate(slide_up(duration=0.8))

# 3D — add Scene3D anywhere
from zolt.three import Scene3D, Torus
home.add(Scene3D(height="400px").add(Torus()))

# Prebuilt components
from zolt_ui.auth import LoginPage
login = LoginPage(providers=["google"])

# Responsive styling — new .on() API
Grid(cols=1).on("md").grid(cols=2).on("lg").grid(cols=3)

# Dark mode — automatic from App.theme = "dark"
# Or per-component: Card().bg("surface").dark().bg("surface-2")

# Import from Figma
# zolt import figma https://figma.com/file/ABC123/MyDesign
```

---

## 15. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ZoltCSS misses edge cases in Phase 0 | High | High | Phase 0 acceptance criteria are strict; no Phase 1 starts until all pass |
| Generated CSS larger than target | Medium | Medium | Deduplication in generator; measure on every CI run |
| Qt QSS doesn't support all CSS properties | High | Medium | `QtStyleGenerator._prop()` has explicit mapping; unsupported props silently ignored |
| esbuild binary not available on exotic platforms | Medium | Low | Fallback: download esbuild from npm at runtime; document requirement |
| Three.js bundle too large for users who don't need 3D | Low | Medium | Auto-detection in compiler: Three.js only bundled when `Scene3D` appears in IR |
| Figma API deprecates node types we depend on | Medium | Medium | Save Figma API responses in test fixtures; integration tests catch breakage early |
| 90-component scope for zolt-ui is too large | High | Medium | Cut to 60 minimum viable set if needed; navigation and e-commerce last priority |
| Docs site reveals missing features | Low | High | Build docs in Phase 8 — after all features are stable |
| GSAP license conflict with PyPI distribution | Low | High | GSAP Business Green license covers distribution; verify before shipping |
| Scope too large for single release | High | High | Phases 5 (import) and 6 (desktop) can slip to v1.6 if needed; Phases 0–4 are non-negotiable |

---

## 16. Glossary

| Term | Definition |
|---|---|
| **ZoltCSS** | Zolt's own styling engine. Takes Python method calls → `StyleRule` objects → outputs `zolt.min.css`. Zero Tailwind, zero CDN, zero CSS knowledge for developers |
| **StyleRule** | An immutable Python dataclass representing one CSS declaration: `{prop, value, pseudo, state, media}` |
| **StyleResolver** | The class that maps component props to `StyleRule` lists. One method per component type |
| **ZoltCSSGenerator** | Takes all `StyleRule`s from the IR tree, deduplicates, assigns atomic class names, outputs CSS |
| **QtStyleGenerator** | Consumes the same `StyleRule`s and outputs QSS for Qt5/Qt6 renderers |
| **RichStyleGenerator** | Consumes the same `StyleRule`s and outputs `rich.Style` objects for CLI rendering |
| **Token** | A named design value in `tokens.py` — e.g., `"color-primary": "#6C63FF"`. Referenced as `var(--z-color-primary)` in CSS |
| **Atomic class** | A single-purpose CSS class generated by `ZoltCSSGenerator` — e.g., `.z42 { background-color: var(--z-color-primary); }` |
| **zolt-bundler** | Internal Python package wrapping esbuild. Bundles GSAP, Three.js, Alpine.js as local assets. No npm for the user |
| **AnimationSpec** | Python dataclass describing one animation: type, parameters, trigger, target ID. Compiled to GSAP JavaScript |
| **Scene3DNode** | IR node representing a Three.js scene. Compiled to a Three.js JavaScript module |
| **Zolt UI** | Separate PyPI package (`zolt-ui`) with 90 production-ready prebuilt components |
| **Skill file** | YAML file in `zolt/skills/` describing one component's API, props, examples, and patterns for AI agents |
| **`zolt.schema.json`** | Machine-readable JSON covering all public classes, methods, and props. Read by Claude Code and VS Code extension |
| **`LLMS.txt`** | AI-readable plain text summary of the entire Zolt API at `zolt.dev/llms.txt` |
| **Design import** | `zolt import figma/framer/webflow` — converts design tool exports to Zolt Python code |
| **Qt WebEngine** | Qt6 mode that embeds Chromium — renders web output (including GSAP + Three.js) inside a native desktop window |
| **Build order principle** | Foundation layers (ZoltCSS, bundler) are built first; features that depend on them (animations, 3D, components) built after |

---

*Zolt v1.5 PRD + TRD — Final Version*
*Zero breaking changes from v1.0.*
*Build order: ZoltCSS → Bundler → Animation → 3D → Zolt UI → Import → Desktop → CLI → AI Skills → Docs → Demo → Launch*
*Cross-reference: Zolt v1.0 PRD (base spec) · Zolt v2.0 PRD (full-stack roadmap)*
