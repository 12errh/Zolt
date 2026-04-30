# Zolt v1.5 — "Production UI" Release
## Product & Technical Requirements Document

**Framework name:** Zolt (formerly PyUI)  
**Version:** 1.5.0  
**Status:** Pre-development  
**Prerequisite:** Zolt v1.0 complete (Phase 1 done, framework live)  
**Author:** Zolt Core Team  
**Last Updated:** April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What v1.0 Got Right & What It Lacks](#2-what-v10-got-right--what-it-lacks)
3. [The v1.5 Manifesto — What Changes](#3-the-v15-manifesto--what-changes)
4. [Product Requirements (PRD)](#4-product-requirements-prd)
   - 4.1 Problem Statement
   - 4.2 Vision & Goals
   - 4.3 Target Users
   - 4.4 Core Features — The Six Pillars
   - 4.5 Non-Goals
   - 4.6 Success Metrics
5. [Technical Requirements (TRD)](#5-technical-requirements-trd)
   - 5.1 Architecture Overview
   - 5.2 Build System — No More CDN
   - 5.3 Animation Engine
   - 5.4 3D Engine
   - 5.5 Design Import System (Figma / Framer / Webflow)
   - 5.6 Prebuilt Component Library — Zolt UI
   - 5.7 Desktop Renderer v1.5 — Qt5 + Qt6
   - 5.8 CLI Renderer Upgrade
   - 5.9 AI-First Architecture
   - 5.10 Skill Files System
   - 5.11 Performance Requirements
   - 5.12 Accessibility Requirements
6. [API Design — Full Reference](#6-api-design--full-reference)
   - 6.1 Animation API
   - 6.2 3D API
   - 6.3 Design Import API
   - 6.4 Zolt UI Prebuilt Components
   - 6.5 Theme Engine v2
   - 6.6 Build System API
7. [Development Phases](#7-development-phases)
   - Phase 0: Architecture Upgrade & Build System
   - Phase 1: Animation Engine
   - Phase 2: 3D Engine
   - Phase 3: Zolt UI — Prebuilt Component Library
   - Phase 4: Design Import System
   - Phase 5: Desktop v1.5 — Qt5 + Qt6
   - Phase 6: AI-First — Skills & Docs Infrastructure
   - Phase 7: Docs Website (built with Zolt)
   - Phase 8: Demo Artifacts (.exe + CLI)
   - Phase 9: Production Hardening & Launch
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

Zolt v1.5 is the "Production UI" release. V1.0 proved the concept — Python compiles to UI. V1.5 makes the output genuinely beautiful, animated, 3D-capable, and indistinguishable from sites built by professional frontend teams.

The six pillars of v1.5:

1. **No CDN** — Tailwind, GSAP, Three.js, and all dependencies are installed Python packages, bundled at build time, zero external runtime calls.
2. **Animation engine** — GSAP-powered scroll animations, page transitions, micro-interactions, and timeline control from pure Python.
3. **3D engine** — Three.js scenes, Spline embeds, and WebGL shaders declared in Python.
4. **Design import** — `zolt import figma <url>` converts a Figma file to a working Zolt component tree. Framer, Webflow, and Sketch also supported.
5. **Zolt UI** — 80+ prebuilt production components: auth pages, pricing, dashboards, landing sections, onboarding — all beautiful by default, fully customisable.
6. **AI-first** — Every component ships with a skill file. Claude Code, Cursor, and any AI agent can build production Zolt UIs without a single hallucinated API.

Deliverables at the end of v1.5:
- Zolt v1.5.0 on PyPI
- `zolt-ui` package on PyPI (80+ prebuilt components)
- Complete docs website at `zolt.dev`, built entirely with Zolt, deployed on Vercel
- `.exe` desktop demo (Windows/macOS/Linux) showcasing framework capabilities
- `zolt demo` CLI command that runs an interactive showcase
- AI skill files for every component and API

---

## 2. What v1.0 Got Right & What It Lacks

### What works well in v1.0

- Core Python class-based API is clean and intuitive
- Compiler pipeline (class tree → IR → HTML output) is solid
- Reactive state system works correctly
- Hot reload is functional
- Basic component library covers layout and content
- Theme engine token system is well-designed

### What is missing or broken

| Problem | Impact | Root cause |
|---|---|---|
| Tailwind loaded from CDN | Production apps break if CDN is down; unused CSS bloated | Architecture decision — needs full fix |
| No animations | UIs look static and unprofessional | Never implemented |
| No 3D support | Cannot build modern marketing sites | Never implemented |
| No design import | Designers work in Figma; gap between design and code | Never implemented |
| No prebuilt components | Every user starts from scratch | Backlogged |
| Qt5 not supported | Users on older systems/Linux locked out | Only Qt6 in v1.0 |
| No AI skills | AI agents hallucinate Zolt APIs | Never implemented |
| Docs are minimal | Adoption blocked by poor documentation | Resource constraint |
| No showcase demos | Hard to demonstrate framework capability | Never built |

---

## 3. The v1.5 Manifesto — What Changes

### 1. CDN is dead. Bundle everything.

V1.0 loaded Tailwind, Alpine.js, and other libraries from CDNs at runtime. This is wrong for three reasons: production apps cannot depend on external uptime; CDN loading adds latency on every page load; and CDN-loaded Tailwind includes all 3MB of CSS instead of only what the app uses.

V1.5 fix: Tailwind is installed as a Python extra (`pip install zolt[web]` pulls `pytailwindcss`). On `zolt build`, the Tailwind CLI scans all compiled templates and produces a minified, purged CSS file — often under 10KB. GSAP, Three.js, and Lottie are bundled via a Node.js build step (managed transparently by Zolt's build system). The user never touches any of this.

### 2. Animation is a first-class citizen

Animations are not a nice-to-have — they are what separates a professional UI from a static page. In v1.5, every component has an `animate` method. Scroll-triggered animations use GSAP ScrollTrigger. Page transitions use GSAP timelines. Micro-interactions on hover, click, and focus are declarative. The user writes Python; Zolt generates the GSAP JavaScript.

### 3. 3D is possible

Three.js scenes are declared as Python components. Spline 3D models are embedded with `Spline(url="...")`. Particle systems, rotating logos, 3D product viewers — all from Python. No JavaScript required.

### 4. Design tools are the source of truth

Designers do not use Python. They use Figma, Framer, and Webflow. The v1.5 design import system bridges this gap: `zolt import figma <file-url>` calls the Figma API, parses the node tree, maps Figma components to Zolt components, and writes a `.py` file with the component tree. The output is not perfect — it requires review — but it captures layout, typography, colours, spacing, and component structure accurately enough to save 80% of the implementation time.

### 5. Everything is prebuilt and beautiful by default

A developer should be able to ship a login page with `from zolt_ui import AuthPage` — not build one from scratch. Zolt UI is a separate package containing 80+ production-grade components: auth flows, pricing tables, dashboards, hero sections, feature grids, onboarding flows, settings pages, and more. All follow the Zolt design system. All are customisable. All look impressive with zero styling work.

### 6. AI agents are first-class users

Claude Code, Cursor, GitHub Copilot, and any other AI coding agent should be able to build production Zolt UIs on the first attempt. This requires skill files — structured YAML/JSON files that describe every component, every method, every prop, and common usage patterns. Skill files ship inside the Zolt package and are updated on every release.

---

## 4. Product Requirements (PRD)

### 4.1 Problem Statement

Zolt v1.0 proved that Python can compile to UI. But the output is not yet competitive with what a frontend developer builds manually. A developer choosing between Zolt and React + Framer Motion today would choose React — because it gives them:

- Smooth, professional animations out of the box
- Access to Three.js for 3D
- A rich ecosystem of prebuilt components (shadcn/ui, Radix, Headless UI)
- The ability to start from a Figma design
- Tools that AI agents can use correctly

V1.5 closes every one of these gaps. By the end of v1.5, a Python developer using Zolt should be able to produce UI output that wins Awwwards nominations — purely from Python.

### 4.2 Vision & Goals

**Vision:** Any person — developer, designer, non-technical founder, or AI agent — should be able to build a world-class production UI in Zolt without knowing JavaScript, CSS, or any frontend tooling.

**Primary Goals:**

- Zero CDN dependencies at runtime — all assets bundled at build time
- Animation system that produces GSAP-quality output from Python declarations
- 3D component system that wraps Three.js completely
- Design import from Figma, Framer, and Webflow in a single CLI command
- 80+ prebuilt production components in `zolt-ui`
- Qt5 and Qt6 desktop support
- AI skill files for 100% of public API surface
- Complete, beautiful docs site built with Zolt itself
- `.exe` demo and `zolt demo` CLI command

**Secondary Goals:**

- Lottie animation support (`Lottie(src="animation.json")`)
- Rive animation support (`Rive(src="animation.riv")`)
- CSS-in-Python: every component accepts raw CSS properties as keyword args
- Motion-safe defaults: all animations respect `prefers-reduced-motion`
- Dark mode on all 80+ Zolt UI components, auto-detected
- `zolt eject` command: output raw HTML/CSS/JS from any Zolt project for teams that need to hand off to frontend

### 4.3 Target Users

**All v1.0 users (unchanged).** V1.5 additionally targets:

**Designers who code:** Know Figma deeply, write some Python, want to go directly from design to live UI without a handoff process.

**Non-technical founders:** Can describe what they want, use `zolt-ui` prebuilt components, and ship a professional SaaS landing page without writing any CSS.

**AI coding agents (Claude Code, Cursor, Copilot):** Given a design brief, generate a complete production Zolt UI that compiles and renders correctly on the first attempt, using skill files as the source of truth.

**Frontend developers evaluating Python:** Sceptical that Python can produce quality UI. The Awwwards-level output, the Three.js support, and the Figma import are what convert them.

### 4.4 Core Features — The Six Pillars

#### Pillar 1 — Build System: No More CDN

```bash
# What happens when user runs:
pip install zolt[web]
# → installs: pytailwindcss, zolt-bundler (our Node.js bridge)

zolt run    # Development
# → Tailwind CLI watches and rebuilds CSS on file change
# → GSAP + Three.js served from local node_modules (managed by Zolt)
# → No external network calls during development

zolt build  # Production
# → Tailwind CLI scans all templates → purged, minified CSS (often < 15KB)
# → GSAP, Three.js, Alpine.js bundled via esbuild → single app.js
# → Output: /dist with zero external dependencies
```

The user never runs npm, never touches a package.json, never configures webpack. Zolt manages the Node.js toolchain internally via a Python subprocess wrapper.

#### Pillar 2 — Animation Engine

```python
from zolt import Page, Hero, Heading, Text, Button
from zolt.animate import fade_in, slide_up, stagger, Timeline, ScrollReveal

class LandingPage(Page):
    hero = Hero().add(
        Heading("Build anything.").animate(
            slide_up(duration=0.8, delay=0.1)
        ),
        Text("In pure Python.").animate(
            fade_in(duration=0.6, delay=0.4)
        ),
        Button("Get started").animate(
            slide_up(duration=0.5, delay=0.6)
        )
    )

    # Scroll-triggered section
    features = Section().add(
        Grid(cols=3).children(
            [FeatureCard(f) for f in features_list]
        ).animate(
            stagger(each=slide_up(duration=0.7), interval=0.15, trigger="scroll")
        )
    )

    # Custom timeline
    intro_timeline = (
        Timeline()
        .add(logo, fade_in(duration=0.5))
        .add(headline, slide_up(duration=0.8), offset="-=0.3")
        .add(subline, fade_in(duration=0.6), offset="-=0.4")
        .play_on("load")
    )
```

**Supported animations:**
- `fade_in / fade_out` — opacity
- `slide_up / slide_down / slide_left / slide_right` — translate + opacity
- `scale_in / scale_out` — scale + opacity
- `blur_in` — blur + opacity (modern effect)
- `clip_reveal` — text clip reveal (editorial style)
- `counter(start, end, duration)` — number counter animation
- `typewriter(text, speed)` — character-by-character reveal
- `parallax(speed)` — scroll-speed offset
- `magnetic(strength)` — cursor-following magnetic effect
- `tilt_3d(max_angle)` — 3D tilt on mouse move
- `stagger(each, interval)` — sequential animation of children
- `Timeline()` — full GSAP timeline control
- `ScrollReveal()` — IntersectionObserver-triggered animations
- `PageTransition(enter, leave)` — between-page animations

All animations compile to GSAP JavaScript. If the user has `prefers-reduced-motion: reduce`, all animations are disabled automatically.

#### Pillar 3 — 3D Engine

```python
from zolt import Page
from zolt.three import Scene3D, Mesh, Sphere, Box, Torus, AmbientLight, PointLight
from zolt.three import OrbitControls, Float, ParticleSystem
from zolt.spline import Spline

class HomePage(Page):
    # Full Three.js scene in Python
    hero_3d = Scene3D(
        background="transparent",
        camera=dict(fov=75, position=(0, 0, 5))
    ).add(
        AmbientLight(intensity=0.5),
        PointLight(color="#ffffff", position=(10, 10, 10), intensity=1.0),

        Mesh(
            geometry=Torus(radius=1, tube=0.3, segments=100),
            material=dict(
                type="MeshStandardMaterial",
                color="#6C63FF",
                metalness=0.8,
                roughness=0.2,
            )
        ).animate(Float(speed=1.5, amplitude=0.3)).rotate(y=0.01),

        ParticleSystem(count=200, color="#ffffff", size=0.02)
    ).controls(OrbitControls(auto_rotate=True, enable_zoom=False))

    # Spline embed — zero-config 3D models
    product_viewer = Spline(
        url="https://prod.spline.design/your-scene-id/scene.splinecode",
        width="100%",
        height="600px"
    )

    # Lottie animation
    loader = Lottie(src="/assets/loading.json", loop=True, autoplay=True)
```

**3D features:**
- `Scene3D` — full Three.js canvas with camera, lights, and controls
- All Three.js geometry primitives: `Sphere`, `Box`, `Torus`, `Cylinder`, `Plane`, `Text3D`
- Materials: `MeshStandardMaterial`, `MeshBasicMaterial`, `MeshPhysicalMaterial`, `ShaderMaterial`
- Lights: `AmbientLight`, `DirectionalLight`, `PointLight`, `SpotLight`, `HemisphereLight`
- Controls: `OrbitControls`, `TrackballControls`
- Built-in animation helpers: `Float`, `Rotate`, `Pulse`, `Oscillate`
- `ParticleSystem` — configurable particle field
- `GLTFLoader` — load external `.gltf` / `.glb` 3D model files
- `Spline` — embed Spline.design scenes
- `Lottie` — embed Lottie JSON animations
- `Rive` — embed Rive interactive animations
- Scroll-linked 3D: `ScrollLinked3D(scene, progress_to_camera_path)`

#### Pillar 4 — Design Import System

```bash
# Figma import
zolt import figma https://figma.com/file/ABC123/MyDesign --output components/design.py

# Framer import (from exported HTML)
zolt import framer ./framer-export/ --output components/framer.py

# Webflow import (from exported ZIP)
zolt import webflow ./webflow-export.zip --output components/webflow.py

# Sketch import (from exported assets)
zolt import sketch ./sketch-export/ --output components/sketch.py
```

**What Figma import produces:**

Input: A Figma file with frames, components, and auto-layout groups.

Process:
1. Calls Figma REST API with user's personal access token
2. Walks the Figma node tree (FRAME → GROUP → COMPONENT → TEXT/RECTANGLE/etc.)
3. Maps Figma auto-layout → Zolt `Flex` / `Grid`
4. Maps Figma text styles → Zolt `Text`, `Heading` with extracted typography
5. Maps Figma colour styles → Zolt theme tokens
6. Maps Figma components → Zolt custom components
7. Writes `.py` file with full component tree

Output example:
```python
# Auto-generated by: zolt import figma — review before using in production
from zolt import Flex, Stack, Text, Heading, Button, Image, Divider
from zolt.theme import color, font, spacing

class HeroSection(Component):
    """Imported from Figma: Landing Page / Hero"""

    def compose(self):
        with Flex(direction="col", align="center", gap=spacing("8")).className("pt-24 pb-16"):
            Heading(
                "The future of Python UI",
                level=1,
                font_size="72px",
                font_weight=900,
                color=color("neutral-900"),
                text_align="center",
                max_width="800px"
            )
            Text(
                "Build beautiful interfaces in pure Python.",
                font_size="20px",
                color=color("neutral-500"),
                text_align="center"
            )
            with Flex(gap=spacing("4")):
                Button("Get started").style("primary").size("lg")
                Button("Learn more").style("ghost").size("lg")
```

**Import accuracy targets:**

| Element | Expected accuracy |
|---|---|
| Layout structure (flex/grid) | 90%+ |
| Typography (size, weight, family) | 95%+ |
| Colours | 98%+ |
| Spacing and padding | 85%+ |
| Component names and hierarchy | 80%+ |
| Interactive states (hover, active) | 60%+ |
| Complex animations | 30% (manual review required) |

#### Pillar 5 — Zolt UI: 80+ Prebuilt Components

A separate PyPI package: `pip install zolt-ui`

Every component is production-ready, dark mode compatible, fully accessible, and animates with Zolt's animation engine automatically.

**Component catalogue:**

```
Authentication (8 components)
├── LoginPage           — Email/password login with social buttons
├── SignupPage          — Registration with validation
├── ForgotPasswordPage  — Password reset flow
├── MagicLinkPage       — Passwordless email link
├── TwoFactorPage       — 2FA verification
├── OnboardingFlow      — Multi-step user onboarding
├── ProfileSetupPage    — Post-signup profile completion
└── AuthLayout          — Wrapper with logo, background

Landing / Marketing (18 components)
├── HeroSection         — 6 variants (centered, split, video, 3D, minimal, bold)
├── FeatureGrid         — Icon + title + description grid
├── FeatureShowcase     — Large alternating feature rows
├── PricingTable        — Monthly/annual toggle, 3 tiers
├── TestimonialsGrid    — Quote cards with avatars
├── TestimonialsCarousel — Auto-scrolling testimonials
├── LogoCloud           — Partner/customer logo marquee
├── StatsRow            — Animated number counters
├── CTASection          — 4 variants (centered, split, dark, gradient)
├── FAQAccordion        — Animated accordion
├── TeamGrid            — Team member cards
├── BlogGrid            — Article preview cards
├── NewsletterSection   — Email capture with validation
├── BentoGrid           — Asymmetric feature showcase grid
├── ComparisonTable     — Feature comparison vs competitors
├── TimelineSection     — Vertical / horizontal timeline
├── VideoSection        — Lightbox video player
└── MapSection          — Embedded map with marker

Dashboard / App UI (22 components)
├── AppLayout           — Sidebar + topbar + content shell
├── Sidebar             — Collapsible navigation sidebar
├── Topbar              — App header with search + notifications + avatar
├── StatsGrid           — KPI cards with trend indicators
├── DataTable           — Sortable, filterable, paginated table
├── AreaChart           — Recharts area chart wrapper
├── BarChart            — Grouped/stacked bar chart
├── LineChart           — Multi-series line chart
├── DonutChart          — Donut / pie chart
├── ActivityFeed        — Timestamped event list
├── NotificationPanel   — Notification drawer
├── CommandPalette      — Cmd+K quick action modal
├── UserTable           — User management table with actions
├── SettingsLayout      — Settings page with section nav
├── BillingSection      — Plan cards + payment method + invoice table
├── EmptyState          — Illustrated empty state with CTA
├── LoadingState        — Skeleton loaders for all components
├── ErrorState          — Error boundary UI
├── SearchResults       — Instant search result list
├── FilterBar           — Multi-filter chip bar
├── Breadcrumbs         — Navigational breadcrumb trail
└── Kanban              — Drag-and-drop kanban board

E-commerce (8 components)
├── ProductCard         — Image + title + price + CTA
├── ProductGrid         — Responsive product listing
├── ProductDetail       — Hero image + specs + add to cart
├── CartDrawer          — Slide-out cart panel
├── CheckoutFlow        — Multi-step checkout
├── OrderSummary        — Order review card
├── ReviewsSection      — Star ratings + review cards
└── WishlistGrid        — Saved items grid

Forms & Input (12 components)
├── ContactForm         — Name + email + message + send
├── MultiStepForm       — Step indicator + validation
├── SearchBar           — Autocomplete search input
├── DateRangePicker     — Calendar-based date range
├── FileUpload          — Drag-and-drop file upload zone
├── RichTextEditor      — Formatted text editor (Tiptap)
├── CodeEditor          — Syntax-highlighted code input
├── AddressForm         — Address fields with country detection
├── PaymentForm         — Stripe Elements wrapper
├── TagInput            — Multi-tag input with autocomplete
├── ColorPicker         — Hex/HSL colour picker
└── RatingInput         — Star/emoji rating widget

Feedback & Overlays (8 components)
├── Toast               — Notification toast (top/bottom, variants)
├── Modal               — Accessible dialog with animations
├── Drawer              — Slide-in side panel
├── ConfirmDialog       — Destructive action confirmation
├── Tooltip             — Rich tooltip with arrow
├── Popover             — Positioned floating panel
├── ContextMenu         — Right-click context menu
└── CommandMenu         — Slash-command menu

Navigation (4 components)
├── MegaNav             — Full-featured navigation bar with dropdowns
├── TabBar              — Animated tab navigation
├── BottomNav           — Mobile bottom navigation bar
└── FloatingNav         — Scroll-aware floating navigation
```

**Using Zolt UI:**

```python
from zolt import App
from zolt_ui.auth import LoginPage, SignupPage
from zolt_ui.landing import HeroSection, PricingTable, FAQAccordion, CTASection
from zolt_ui.dashboard import AppLayout, StatsGrid, DataTable

class MySaaSApp(App):
    # Landing page — assembled from prebuilts
    home = Page(title="My SaaS", route="/")
    home.add(
        HeroSection(
            title="Build anything.",
            subtitle="In pure Python.",
            cta_primary=Button("Start free").onClick(go_to_signup),
            cta_secondary=Button("See demo"),
            variant="centered",
            background="gradient"
        ),
        PricingTable(
            plans=pricing_data,
            on_select=handle_plan_select
        ),
        FAQAccordion(items=faq_data),
        CTASection(title="Ready?", variant="dark")
    )

    # Auth pages — single line each
    login  = LoginPage(providers=["google", "github"], on_success=go_to_dashboard)
    signup = SignupPage(providers=["google"], on_success=go_to_onboarding)

    # App dashboard — fully prebuilt
    dashboard = AppLayout(
        sidebar=Sidebar(items=nav_items),
        content=Page().add(
            StatsGrid(stats=stats_data),
            DataTable(route="/api/users")
        )
    )
```

#### Pillar 6 — AI-First Architecture

Every public component, every API method, every design pattern ships with a structured skill file. The skill file format is YAML and is designed to be read by Claude Code, Cursor, GitHub Copilot, and any LLM with tool-use capability.

Full specification in Section 9.

---

### 4.5 Non-Goals for v1.5

- React or Vue component interoperability (v2.0 scope)
- Native iOS/Android apps (v2.0 scope)
- Visual drag-and-drop builder UI (v2.x scope)
- Full Figma plugin (export directly from Figma — v1.6 scope)
- WebGL shader editor (advanced Three.js — v2.0 scope)
- Server-side rendering / SSR (v2.0 scope)
- Zolt Cloud hosting (v2.0 scope)
- GraphQL API (v2.0 scope)

### 4.6 Success Metrics

| Metric | Target (6 months post v1.5 launch) |
|---|---|
| PyPI downloads (`zolt-framework`) | 100,000/month |
| PyPI downloads (`zolt-ui`) | 40,000/month |
| GitHub stars | 12,000 |
| Awwwards / CSS Design Awards submissions built with Zolt | 5+ |
| Figma imports completed successfully | >80% accuracy rating from users |
| AI agent first-attempt correctness (Claude Code) | >95% |
| Docs site Lighthouse score | >95 on all categories |
| Build output Lighthouse score (default app) | >90 |
| `.exe` demo downloads in first month | 5,000+ |
| Discord members | 3,000 |

---

## 5. Technical Requirements (TRD)

### 5.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Python Code                            │
│  from zolt import App, Page, Heading, Scene3D                   │
│  from zolt_ui import LoginPage, HeroSection, PricingTable       │
│  from zolt.animate import fade_in, stagger, Timeline            │
│  from zolt.three import Scene3D, Torus, PointLight              │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │     Zolt Compiler v1.5       │
              │  Class tree → IR (extended)  │
              │  Animation node resolver     │
              │  3D scene serialiser         │
              │  Design import parser        │
              └──┬──────────────────────┬───┘
                 │                      │
    ┌────────────▼───────┐  ┌───────────▼────────────┐
    │   Build System     │  │    IR → Renderer        │
    │                    │  │                         │
    │  Tailwind CLI      │  │  Web: HTML+CSS+GSAP+3JS │
    │  esbuild bundler   │  │  Desktop: Qt5 / Qt6     │
    │  Asset pipeline    │  │  CLI: Rich TUI          │
    │  Image optimiser   │  │                         │
    └────────────────────┘  └─────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              AI Compatibility Layer                              │
│  zolt-skills/ · zolt.schema.json · LLMS.txt                    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Build System — No More CDN

#### The Problem with CDN

Zolt v1.0 included this in generated HTML:
```html
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

This is wrong because:
1. **Runtime dependency** — if CDN is down, app breaks
2. **No tree-shaking** — Tailwind CDN loads all 3MB of CSS every time
3. **Privacy** — CDN requests leak user data to third parties
4. **CSP violations** — many enterprises block external script loading
5. **Offline** — desktop apps cannot use CDN

#### The Fix: Python-managed build toolchain

```python
# pyproject.toml extras
[project.optional-dependencies]
web = [
    "pytailwindcss>=0.2.0",       # Tailwind CLI as Python package
    "zolt-bundler>=1.5.0",         # Our esbuild wrapper
]
```

**`zolt-bundler`** is a small Python package that:
- Ships pre-compiled `esbuild` binaries for Windows/macOS/Linux (like esbuild npm package does)
- Bundles GSAP, Alpine.js, Three.js, and other JS dependencies
- Exposes a Python API: `Bundle(entry="app.js", output="dist/app.bundle.js").run()`
- Managed entirely by Zolt's build system — user never touches it

**Development flow:**

```bash
zolt run --web
# 1. Zolt compiler generates HTML templates to /tmp/zolt-build/
# 2. Tailwind CLI (pytailwindcss) watches templates → outputs style.css
# 3. zolt-bundler watches JS → bundles → outputs app.js
# 4. aiohttp dev server serves from /tmp/zolt-build/
# 5. File watcher → IR diff → patch → hot reload
```

**Production build flow:**

```bash
zolt build --web
# 1. Compiler generates all HTML pages to /build/
# 2. Tailwind CLI: scan /build/ → purge → minify → /dist/style.min.css
# 3. esbuild: bundle GSAP + Alpine.js + Three.js + app.js → /dist/app.min.js
# 4. Image optimisation: all images compressed via Pillow
# 5. Output /dist/ — fully self-contained, zero external dependencies
# 6. Optional: zolt build --web --upload (pushes to PyUI Cloud / Vercel)
```

**Output size targets:**

| Asset | Target size (gzipped) |
|---|---|
| style.min.css (Tailwind purged) | < 15KB |
| app.min.js (Alpine.js only, no 3D) | < 45KB |
| app.min.js (with GSAP) | < 90KB |
| app.min.js (with GSAP + Three.js) | < 280KB |
| Total (typical app, no 3D) | < 120KB |
| Total (with 3D) | < 350KB |

#### Tailwind Configuration

Zolt manages `tailwind.config.js` internally. User customises through the Python theme API:

```python
class MyApp(App):
    theme = {
        "color.primary": "#6C63FF",
        "font.family": "Geist, Inter, sans-serif",
        "radius.md": "8px"
    }
```

Zolt translates this to `tailwind.config.js` and regenerates CSS. The user never edits a config file.

### 5.3 Animation Engine

#### Architecture

Zolt's animation engine works in two phases:

**Phase A (compile time):** The Zolt compiler walks the IR tree and collects all `.animate()` calls. Each animation is an `AnimationNode` with a target component ID, animation type, and parameters.

**Phase B (code generation):** The web renderer converts `AnimationNode` objects to GSAP JavaScript. The generated JS is appended to `app.js` by the bundler.

```python
# Python API
Heading("Hello").animate(slide_up(duration=0.8, delay=0.2, ease="power3.out"))

# Generates this GSAP JavaScript (user never sees it):
gsap.from("#comp-a1b2", {
  duration: 0.8,
  delay: 0.2,
  y: 48,
  opacity: 0,
  ease: "power3.out"
});
```

#### Animation Node IR

```python
# zolt/compiler/ir.py — extended for animations

@dataclass
class AnimationNode:
    target_id: str
    animation_type: str          # "fade_in", "slide_up", "stagger", etc.
    params: dict                 # duration, delay, ease, etc.
    trigger: str                 # "load", "scroll", "hover", "click"
    trigger_params: dict         # scroll margin, threshold, etc.
    children: list[AnimationNode] = field(default_factory=list)  # For stagger
```

#### ScrollReveal Implementation

ScrollReveal uses IntersectionObserver (compiled to JS) triggered by GSAP ScrollTrigger:

```python
# Python
Grid(cols=3).add(
    *[FeatureCard(f) for f in features]
).animate(
    stagger(
        each=slide_up(duration=0.7, ease="power2.out"),
        interval=0.12,
        trigger="scroll",
        threshold=0.2
    )
)

# Generated JS:
gsap.from(".comp-grid-x1 > *", {
  scrollTrigger: {
    trigger: ".comp-grid-x1",
    start: "top 80%",
    toggleActions: "play none none none"
  },
  duration: 0.7,
  y: 48,
  opacity: 0,
  ease: "power2.out",
  stagger: 0.12
});
```

#### Page Transitions

```python
class MyApp(App):
    transitions = PageTransition(
        enter=slide_up(duration=0.5, ease="power3.out"),
        leave=fade_out(duration=0.3)
    )
```

Generated as a route-change listener in Alpine.js that triggers GSAP on navigation.

#### `prefers-reduced-motion` Compliance

All generated GSAP code is wrapped:

```javascript
const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
if (!motion.matches) {
  // All GSAP animations here
}
```

Users can override: `animation.ignore_reduced_motion(True)` (use with caution, documented as accessibility risk).

### 5.4 3D Engine

#### Architecture

Three.js scenes are declared as a Python component tree → compiled to an IR `Scene3DNode` → the web renderer generates a `<canvas>` element and a Three.js JavaScript module.

```python
# zolt/compiler/ir.py

@dataclass
class Scene3DNode:
    width: str
    height: str
    background: str
    camera: CameraConfig
    lights: list[LightNode]
    objects: list[Object3DNode]
    controls: ControlsConfig | None
    animation_loop: list[AnimationLoopNode]

@dataclass
class Object3DNode:
    geometry: GeometryConfig     # type + params
    material: MaterialConfig     # type + props
    position: tuple[float,float,float]
    rotation: tuple[float,float,float]
    scale: tuple[float,float,float]
    animations: list[Object3DAnimation]
    children: list[Object3DNode]
```

#### GLTF Model Loading

```python
from zolt.three import Scene3D, GLTFModel, AmbientLight, OrbitControls

product_viewer = Scene3D(height="500px").add(
    AmbientLight(intensity=0.6),
    GLTFModel(
        src="/assets/product.glb",
        auto_rotate=True,
        loading=Spinner()          # Shown while model loads
    )
).controls(OrbitControls(enable_zoom=True, auto_rotate_speed=1.0))
```

#### Scroll-Linked 3D

```python
from zolt.three import Scene3D, ScrollLinked3D, Sphere

hero_scene = Scene3D().add(
    Sphere(radius=1).material(color="#6C63FF").animate(
        ScrollLinked3D(
            rotation_y=(0, Math.PI * 2),    # Full rotation on scroll
            position_y=(0, -3),             # Moves down as user scrolls
            scroll_range=(0, 1000)          # Pixel range
        )
    )
)
```

#### Spline Integration

Spline is the easiest path to stunning 3D — designers build in Spline, developers embed in one line:

```python
from zolt.spline import Spline

hero = Spline(
    url="https://prod.spline.design/abc123/scene.splinecode",
    width="100%",
    height="600px",
    loading=Spinner(),          # Shown while Spline loads
    events={                    # Spline event binding
        "mouseDown-logo": handle_logo_click,
        "scroll": handle_scroll
    }
)
```

Spline scenes are loaded as iframes with the Spline viewer runtime — bundled locally, not from CDN.

### 5.5 Design Import System

#### Figma Import Pipeline

```
zolt import figma <url>
         │
         ▼
1. Parse URL → extract file_key and node_id
         │
         ▼
2. Figma API: GET /v1/files/{file_key}
   - Requires FIGMA_ACCESS_TOKEN env var
   - Fetches entire file node tree as JSON
         │
         ▼
3. Node tree walker (zolt/import/figma/walker.py)
   - Walk DOCUMENT → CANVAS → FRAME → COMPONENT → ...
   - Build intermediate ImportNode tree
         │
         ▼
4. Node mapper (zolt/import/figma/mapper.py)
   - FRAME → Page or Component
   - AUTO_LAYOUT horizontal → Flex(direction="row")
   - AUTO_LAYOUT vertical → Flex(direction="col")
   - GRID → Grid(cols=n)
   - TEXT → Text() or Heading() based on font size
   - RECTANGLE with fill → Div with background
   - INSTANCE → ZoltUI component match (fuzzy name match)
   - IMAGE → Image(src=...)
   - VECTOR/GROUP → SVG embed
         │
         ▼
5. Style extractor (zolt/import/figma/styles.py)
   - Typography → font_size, font_weight, line_height
   - Colours → hex values mapped to theme tokens where possible
   - Spacing → margin, padding (converted from Figma px to rem)
   - Effects → box_shadow, border_radius
         │
         ▼
6. Code generator (zolt/import/figma/codegen.py)
   - Writes .py file with Zolt component tree
   - Includes TODOs where manual review is needed
   - Adds import statements for all used components
         │
         ▼
7. Output: components/design.py
   # Auto-generated by: zolt import figma
   # Review the following before using in production:
   # TODO: Verify interactive states on Button components
   # TODO: Replace placeholder images with actual assets
```

#### Framer Import Pipeline

Framer exports clean HTML/CSS. Zolt's Framer importer:

1. Unzips exported HTML directory
2. Parses HTML with `lxml` / `BeautifulSoup`
3. Maps CSS classes to Tailwind utilities (reverse-mapping table)
4. Maps DOM structure to Zolt component tree
5. Preserves Framer's animation classes as Zolt animate() calls
6. Writes `.py` output

#### Webflow Import Pipeline

Same as Framer but Webflow export structure differs. Webflow exports include CMS data — Zolt maps this to reactive data sources.

#### Import Configuration

```python
# zolt.config.py
import_config = ImportConfig(
    figma_token=env("FIGMA_ACCESS_TOKEN"),
    auto_map_colors=True,        # Map Figma colours to theme tokens
    component_fuzzy_match=True,  # Try to match Figma components to zolt-ui
    output_format="class",       # "class" | "function" | "dict"
    add_review_comments=True,    # TODOs where manual review needed
)
```

### 5.6 Prebuilt Component Library — Zolt UI

#### Architecture

`zolt-ui` is a separate PyPI package that depends on `zolt-framework`. Each component is a Python class that inherits from `Component` and uses only the public Zolt v1.5 API — so it always works with any Zolt v1.5+ app.

```
zolt-ui/
├── auth/         LoginPage, SignupPage, etc.
├── landing/      HeroSection, PricingTable, etc.
├── dashboard/    AppLayout, DataTable, etc.
├── ecommerce/    ProductGrid, CartDrawer, etc.
├── forms/        ContactForm, MultiStepForm, etc.
├── feedback/     Toast, Modal, Drawer, etc.
└── navigation/   MegaNav, TabBar, etc.
```

Every component:
- Has full type hints on all props
- Supports dark mode (auto-detected)
- Has a `.variant(n)` method for style variants
- Integrates with Zolt's animation engine
- Has a corresponding skill file
- Has Storybook-equivalent in `zolt studio`
- Has a screenshot in the docs

#### Design System

All Zolt UI components share a unified design system:

```python
# zolt_ui/design_system.py

DESIGN_TOKENS = {
    # Spacing — 4px base grid
    "space": {
        "1": "4px",   "2": "8px",   "3": "12px",  "4": "16px",
        "5": "20px",  "6": "24px",  "8": "32px",  "10": "40px",
        "12": "48px", "16": "64px", "20": "80px", "24": "96px"
    },
    # Typography scale
    "font_size": {
        "xs": "12px",  "sm": "14px",  "base": "16px",
        "lg": "18px",  "xl": "20px",  "2xl": "24px",
        "3xl": "30px", "4xl": "36px", "5xl": "48px",
        "6xl": "60px", "7xl": "72px", "8xl": "96px"
    },
    # Radius
    "radius": {
        "sm": "4px", "md": "8px", "lg": "12px",
        "xl": "16px", "2xl": "24px", "full": "9999px"
    },
    # Shadow
    "shadow": {
        "sm":  "0 1px 2px rgba(0,0,0,0.05)",
        "md":  "0 4px 6px rgba(0,0,0,0.07)",
        "lg":  "0 10px 25px rgba(0,0,0,0.10)",
        "xl":  "0 20px 40px rgba(0,0,0,0.15)",
        "2xl": "0 40px 80px rgba(0,0,0,0.20)"
    }
}
```

### 5.7 Desktop Renderer v1.5 — Qt5 + Qt6

V1.0 supported tkinter (default) and PyQt6 (optional). V1.5 adds PyQt5 for backward compatibility and richer widget support.

```bash
pip install zolt[qt5]   # PyQt5 renderer
pip install zolt[qt6]   # PyQt6 renderer (default enhanced)

zolt run --desktop --qt5    # Force Qt5
zolt run --desktop --qt6    # Force Qt6 (default)
zolt run --desktop --tk     # Legacy tkinter (v1.0 path, kept)
```

#### Qt5 vs Qt6 Feature Matrix

| Feature | tkinter | Qt5 | Qt6 |
|---|---|---|---|
| Animated widgets | No | Partial | Yes |
| WebEngine (full web renderer) | No | Yes | Yes |
| 3D via WebEngine | No | Yes | Yes |
| Custom fonts | Limited | Yes | Yes |
| Dark mode native | No | Partial | Yes |
| Deployment size | Small | 35MB | 40MB |
| Python support | Any | 3.8+ | 3.10+ |

#### Qt WebEngine Mode

For Qt5/Qt6 desktop, Zolt offers a **WebEngine mode** that embeds a full Chromium WebView inside the Qt window, rendering the same HTML/CSS/JS output as the web target:

```bash
zolt run --desktop --qt6 --webengine
```

This gives full animation, 3D, and visual parity with the web output inside a native window. The Python backend runs as a local FastAPI server (from v2 backend, or just a file server for v1.5).

Benefits: pixel-perfect with web output, full GSAP/Three.js support in desktop.
Trade-off: larger binary (includes Chromium, ~120MB) vs pure Qt widgets (~40MB).

#### Animation Support in Qt

For pure Qt widget mode (no WebEngine), animations use Qt's native `QPropertyAnimation`:

```python
# Python animation declaration — same API as web
Button("Click").animate(fade_in(duration=0.4))

# For Qt5/Qt6 — compiles to QPropertyAnimation:
anim = QPropertyAnimation(button, b"windowOpacity")
anim.setDuration(400)
anim.setStartValue(0.0)
anim.setEndValue(1.0)
anim.setEasingCurve(QEasingCurve.OutCubic)
anim.start()
```

### 5.8 CLI Renderer Upgrade

V1.0 CLI renderer was basic. V1.5 upgrades:

- **Textual** as the primary TUI framework (replaces plain Rich for interactive apps)
- Rich retained for static output and logging
- New interactive CLI components: `CLIModal`, `CLIMenu`, `CLIProgress`, `CLITable`
- Mouse support in Textual renderer
- Dark/light terminal theme detection
- `zolt run --cli --interactive` for full Textual mode
- `zolt run --cli --static` for plain Rich output (pipe-friendly)

### 5.9 AI-First Architecture

Every design decision in v1.5 is made with AI agents as first-class users. The rules:

1. **One way to do each thing.** No three different ways to add a click handler. `onClick()` is always `onClick()`.
2. **All props typed, all types exported.** `Button("text", size="lg")` — `size` is `Literal["xs","sm","md","lg","xl"]`. The type is in `zolt.types`. AI agents can read it.
3. **No positional-only args after first.** `Heading("text", level=2)` not `Heading("text", 2)`. Named args are readable by agents.
4. **Consistent event naming.** `onClick`, `onChange`, `onSubmit`, `onHover`, `onFocus`, `onBlur`, `onMount`, `onUnmount` — exact same names everywhere.
5. **Error messages suggest the fix.** `[ZOLT-1501] Button.size must be one of: "xs", "sm", "md", "lg", "xl". Got: "large"`.
6. **Skill files ship with the package.** See Section 9.
7. **`zolt.schema.json` published with every release.**
8. **`LLMS.txt` at `zolt.dev/llms.txt`.**

### 5.10 Skill Files System

Full specification in Section 9.

### 5.11 Performance Requirements

| Metric | Target |
|---|---|
| Production CSS size (Tailwind purged, gzip) | < 15KB |
| Production JS (no 3D, gzip) | < 90KB |
| Production JS (with GSAP + Three.js, gzip) | < 350KB |
| First Contentful Paint (web, simulated 4G) | < 1.2s |
| Lighthouse Performance score | > 90 |
| Lighthouse Accessibility score | > 95 |
| Lighthouse Best Practices score | > 95 |
| Lighthouse SEO score | > 90 |
| `zolt build` time (50-component app) | < 8s |
| Hot reload latency | < 200ms |
| Figma import time (100-node file) | < 30s |
| Qt5/Qt6 desktop startup time | < 1.5s |

### 5.12 Accessibility Requirements

- All Zolt UI components pass axe-core automated audit
- All interactive components keyboard-navigable (tab, enter, space, escape, arrows)
- All images require `alt` text — compiler emits `[ZOLT-1510]` warning if missing
- All colour combinations meet WCAG 2.1 AA (4.5:1 text, 3:1 UI components)
- `aria-live` regions for dynamic content updates
- Focus management in modals and drawers (focus trap)
- All form inputs associated with labels
- `prefers-reduced-motion` respected by all animations
- Screen reader testing: NVDA (Windows), VoiceOver (macOS), TalkBack (Android via PWA)

---

## 6. API Design — Full Reference

### 6.1 Animation API

```python
# zolt/animate/__init__.py

# Basic animations
def fade_in(duration=0.5, delay=0, ease="power2.out") -> Animation: ...
def fade_out(duration=0.5, delay=0, ease="power2.in") -> Animation: ...
def slide_up(duration=0.6, delay=0, distance=48, ease="power3.out") -> Animation: ...
def slide_down(duration=0.6, delay=0, distance=48, ease="power3.out") -> Animation: ...
def slide_left(duration=0.6, delay=0, distance=48, ease="power3.out") -> Animation: ...
def slide_right(duration=0.6, delay=0, distance=48, ease="power3.out") -> Animation: ...
def scale_in(duration=0.5, delay=0, from_scale=0.92, ease="back.out(1.7)") -> Animation: ...
def scale_out(duration=0.4, delay=0, to_scale=0.92, ease="power2.in") -> Animation: ...
def blur_in(duration=0.6, delay=0, from_blur=8, ease="power2.out") -> Animation: ...
def clip_reveal(duration=0.8, delay=0, direction="up", ease="power3.inOut") -> Animation: ...

# Text animations
def typewriter(speed=0.05, cursor=True) -> Animation: ...
def counter(start=0, end=100, duration=2.0, suffix="") -> Animation: ...
def word_by_word(duration=0.6, stagger=0.1) -> Animation: ...

# Interactive
def magnetic(strength=0.3, ease=0.15) -> Animation: ...
def tilt_3d(max_angle=10, perspective=1000) -> Animation: ...
def parallax(speed=0.3) -> Animation: ...
def hover_lift(amount=4, shadow=True) -> Animation: ...

# Compound
def stagger(each: Animation, interval=0.1, trigger="scroll", from_="start") -> Animation: ...

# Timeline
class Timeline:
    def add(self, component, animation, offset="+=0") -> Timeline: ...
    def play_on(self, trigger: Literal["load","scroll","click","hover"]) -> Timeline: ...
    def repeat(self, times=-1, yoyo=False) -> Timeline: ...
    def pause() -> Timeline: ...
    def resume() -> Timeline: ...
    def seek(progress: float) -> Timeline: ...

# Scroll-linked
class ScrollReveal:
    trigger: str = "top 80%"
    end: str = "bottom 20%"
    scrub: bool | float = False
    pin: bool = False
    markers: bool = False     # Dev mode debug markers

class ScrollLinked3D:
    property: str             # "rotation.y", "position.x", etc.
    from_value: float
    to_value: float
    scroll_start: int = 0
    scroll_end: int = 1000
    ease: str = "none"

# Page transitions
class PageTransition:
    enter: Animation
    leave: Animation
    duration: float = 0.4
```

### 6.2 3D API

```python
# zolt/three/__init__.py

class Scene3D(Component):
    width: str = "100%"
    height: str = "400px"
    background: str = "transparent"
    camera: CameraConfig = CameraConfig(fov=75, position=(0, 0, 5))
    antialias: bool = True
    shadow: bool = True
    pixel_ratio: float = 2.0     # window.devicePixelRatio capped at 2

    def add(self, *objects) -> Scene3D: ...
    def controls(self, controls) -> Scene3D: ...
    def on_created(self, handler: Callable) -> Scene3D: ...

# Geometry
class Sphere(Geometry):
    radius: float = 1
    width_segments: int = 64
    height_segments: int = 64

class Box(Geometry):
    width: float = 1
    height: float = 1
    depth: float = 1

class Torus(Geometry):
    radius: float = 1
    tube: float = 0.4
    radial_segments: int = 16
    tubular_segments: int = 100

class Cylinder(Geometry): ...
class Cone(Geometry): ...
class Plane(Geometry): ...
class Ring(Geometry): ...
class Text3D(Geometry):
    text: str
    font: str = "/assets/fonts/inter_bold.json"
    size: float = 0.5
    depth: float = 0.1
class CustomGeometry(Geometry):
    vertices: list[tuple[float,float,float]]
    faces: list[tuple[int,int,int]]

# Mesh
class Mesh(Component):
    geometry: Geometry
    material: dict | Material
    position: tuple = (0, 0, 0)
    rotation: tuple = (0, 0, 0)
    scale: tuple = (1, 1, 1)
    cast_shadow: bool = True
    receive_shadow: bool = True

    def animate(self, *animations) -> Mesh: ...
    def rotate(self, x=0, y=0, z=0) -> Mesh: ...    # Per-frame rotation speed
    def position_at(self, x, y, z) -> Mesh: ...

# Materials
class MeshStandardMaterial:
    color: str = "#ffffff"
    metalness: float = 0.0
    roughness: float = 0.5
    wireframe: bool = False
    transparent: bool = False
    opacity: float = 1.0

class MeshPhysicalMaterial(MeshStandardMaterial):
    transmission: float = 0.0   # Glass effect
    ior: float = 1.5
    thickness: float = 0.5

class ShaderMaterial:
    vertex_shader: str
    fragment_shader: str
    uniforms: dict

# Lights
class AmbientLight:
    color: str = "#ffffff"
    intensity: float = 0.5

class PointLight:
    color: str = "#ffffff"
    intensity: float = 1.0
    position: tuple = (0, 10, 0)
    cast_shadow: bool = True

class DirectionalLight(PointLight): ...
class SpotLight(PointLight): ...
class HemisphereLight:
    sky_color: str = "#ffffff"
    ground_color: str = "#444444"
    intensity: float = 0.6

# Controls
class OrbitControls:
    enable_zoom: bool = True
    enable_pan: bool = True
    auto_rotate: bool = False
    auto_rotate_speed: float = 1.0
    damping: bool = True
    min_distance: float = 1
    max_distance: float = 100

# Helpers
class ParticleSystem(Component):
    count: int = 1000
    color: str = "#ffffff"
    size: float = 0.01
    spread: float = 5.0
    animate_flow: bool = True
    flow_speed: float = 0.3

class Float:
    speed: float = 1.0
    amplitude: float = 0.3
    rotation_intensity: float = 0.5

class GLTFModel(Component):
    src: str
    auto_rotate: bool = False
    auto_rotate_speed: float = 1.0
    loading: Component | None = None
    cast_shadow: bool = True

# Spline
class Spline(Component):
    url: str
    width: str = "100%"
    height: str = "400px"
    loading: Component | None = None
    events: dict[str, Callable] = {}

# Lottie
class Lottie(Component):
    src: str
    loop: bool = True
    autoplay: bool = True
    speed: float = 1.0
    width: str = "100%"
    height: str = "auto"

# Rive
class Rive(Component):
    src: str
    animation: str | None = None
    state_machine: str | None = None
    autoplay: bool = True
```

### 6.3 Design Import API

```python
# zolt/import/__init__.py

class FigmaImporter:
    token: str = env("FIGMA_ACCESS_TOKEN")
    auto_map_colors: bool = True
    component_fuzzy_match: bool = True
    output_format: Literal["class", "function"] = "class"
    add_review_comments: bool = True

    def import_file(self, url: str, output: str) -> ImportResult: ...
    def import_node(self, url: str, node_id: str, output: str) -> ImportResult: ...
    def import_component(self, url: str, component_name: str) -> Component: ...

class FramerImporter:
    def import_export(self, path: str, output: str) -> ImportResult: ...

class WebflowImporter:
    def import_export(self, path: str, output: str) -> ImportResult: ...

@dataclass
class ImportResult:
    success: bool
    output_path: str
    components_generated: int
    warnings: list[str]    # TODOs, manual review needed
    errors: list[str]
    accuracy_estimate: float    # 0.0 – 1.0
```

### 6.4 Theme Engine v2

```python
# zolt/theme/__init__.py

# V2 theme system — full design token control
class Theme:
    # Color palette (semantic)
    primary:          str = "#6C63FF"
    primary_hover:    str = "#5A52E0"
    primary_fg:       str = "#FFFFFF"
    secondary:        str = "#F3F4F6"
    secondary_fg:     str = "#111827"
    accent:           str = "#FF5C1A"
    background:       str = "#FFFFFF"
    surface:          str = "#F9FAFB"
    surface_2:        str = "#F3F4F6"
    border:           str = "#E5E7EB"
    text:             str = "#111827"
    text_muted:       str = "#6B7280"
    success:          str = "#10B981"
    warning:          str = "#F59E0B"
    danger:           str = "#EF4444"
    info:             str = "#3B82F6"

    # Dark mode overrides
    dark: DarkTheme | None = None

    # Typography
    font_sans:        str = "Inter, system-ui, sans-serif"
    font_serif:       str = "Playfair Display, Georgia, serif"
    font_mono:        str = "JetBrains Mono, Courier New, monospace"

    # Shape
    radius_sm:  str = "4px"
    radius_md:  str = "8px"
    radius_lg:  str = "12px"
    radius_xl:  str = "16px"
    radius_full:str = "9999px"

    # Animation
    duration_fast:   str = "150ms"
    duration_normal: str = "250ms"
    duration_slow:   str = "400ms"
    ease_default:    str = "cubic-bezier(0.16, 1, 0.3, 1)"

# Built-in themes
THEMES = {
    "default":   Theme(),
    "dark":      Theme(background="#0A0A0A", surface="#111111", text="#F0EDE6", ...),
    "ocean":     Theme(primary="#0EA5E9", background="#F0F9FF", ...),
    "forest":    Theme(primary="#10B981", background="#F0FDF4", ...),
    "sunset":    Theme(primary="#F97316", background="#FFF7ED", ...),
    "rose":      Theme(primary="#F43F5E", background="#FFF1F2", ...),
    "midnight":  Theme(primary="#7C3AED", background="#0D0D1A", ...),
    "terminal":  Theme(primary="#00FF88", background="#0A0A0A", font_mono="JetBrains Mono", ...),
}
```

### 6.5 Build System API

```python
# zolt/build/__init__.py

class BuildConfig:
    target: Literal["web", "desktop", "cli", "all"] = "web"
    output_dir: str = "./dist"
    minify: bool = True
    source_maps: bool = False
    optimize_images: bool = True
    bundle_3d: bool = "auto"     # True if Scene3D used, else False
    bundle_gsap: bool = "auto"   # True if animations used
    analyze: bool = False        # Output bundle analysis report
    desktop_engine: Literal["tk", "qt5", "qt6", "qt6-webengine"] = "qt6"
    desktop_icon: str | None = None
    desktop_name: str | None = None    # From App.name if None
```

---

## 7. Development Phases

### Phase 0 — Architecture Upgrade & Build System
**Duration:** 2 weeks  
**Goal:** Kill the CDN. Tailwind and all JS dependencies bundled locally.

#### Tasks

1. **`zolt-bundler` package**
   - Python wrapper around esbuild binary (ship pre-compiled for Win/Mac/Linux)
   - `Bundle` class: entry point, output path, minify, source maps
   - GSAP, Alpine.js, Three.js, Spline runtime as bundled assets in the package
   - Exposed to Zolt's build system — user never touches it

2. **`pytailwindcss` integration**
   - Add to `zolt[web]` extras
   - `TailwindBuilder` class wraps `pytailwindcss.run()`
   - Content scanning: pass all compiled HTML templates to Tailwind
   - Output: purged, minified `style.min.css`
   - Dev mode: watch mode, instant rebuilds

3. **Remove all CDN references**
   - Audit v1.0 generated HTML — remove all `<script src="https://...">` tags
   - Replace with local bundled assets
   - Add CI test: scan built output for external URLs, fail if found

4. **Build pipeline orchestration**
   - `zolt run` → starts Tailwind watch + JS bundler watch + aiohttp dev server
   - `zolt build` → full production pipeline with size reporting
   - `zolt build --analyze` → opens bundle analyser in browser

5. **Node.js toolchain management**
   - `zolt doctor` checks Node.js availability (required for esbuild)
   - `zolt install-deps` — downloads and installs JS build tools
   - All Node.js interaction via Python subprocess — user never types npm

6. **Error codes for build system**
   - Reserve codes 1500–1599 for v1.5 errors
   - `ZOLT-1500`: Tailwind not installed — run `pip install zolt[web]`
   - `ZOLT-1501`: Invalid prop value
   - `ZOLT-1502`: Missing `alt` text on Image
   - `ZOLT-1503`: External URL found in build output (CDN leak)

#### Deliverables
- `zolt build` produces fully self-contained `/dist` with zero external URLs
- CSS output < 15KB gzipped for a 20-component app
- All v1.0 tests pass
- CI test blocks any CDN reference from appearing in build output

---

### Phase 1 — Animation Engine
**Duration:** 3 weeks  
**Goal:** Full GSAP animation system accessible from Python.

#### Tasks

1. **Animation IR nodes**
   - `AnimationNode` dataclass extending IR
   - Animation type registry (all animation functions → IR params)
   - Target ID system: every animated component gets a stable `data-zolt-id`

2. **Component `.animate()` method**
   - Added to `BaseComponent`
   - Accepts any `Animation` object
   - Supports chaining: `.animate(fade_in()).animate(slide_up())`
   - Multiple animations on one component → GSAP timeline

3. **GSAP code generator**
   - `AnimationCodegen` class in `zolt/renderers/web/`
   - Walks IR animation nodes → GSAP JavaScript
   - Appended to bundled `app.js`
   - Handles all animation types, triggers, and eases

4. **ScrollReveal system**
   - IntersectionObserver + GSAP ScrollTrigger integration
   - `stagger` with scroll trigger
   - Configurable threshold, rootMargin

5. **Timeline implementation**
   - `Timeline` Python class → GSAP `gsap.timeline()` JavaScript
   - `play_on` trigger system

6. **Page transitions**
   - Route change detection in Alpine.js
   - Enter/leave animation execution
   - Scroll-to-top on navigation

7. **`prefers-reduced-motion` wrapper**
   - All generated GSAP wrapped in motion preference check
   - Documented override for accessibility-aware use

8. **Text animations**
   - `typewriter` — character-by-character
   - `counter` — number animation
   - `word_by_word` — staggered word reveal
   - `clip_reveal` — CSS clip-path text reveal

9. **Interactive animations**
   - `magnetic` — cursor-following (mousemove → JavaScript)
   - `tilt_3d` — mouse tilt (perspective transform)
   - `parallax` — scroll-speed CSS transform
   - `hover_lift` — translateY + shadow on hover

10. **Lottie component**
    - `Lottie(src, loop, autoplay, speed)` — bundled lottie-web

11. **Rive component**
    - `Rive(src, animation, state_machine)` — bundled @rive-app/canvas

#### Deliverables
- All animation types compile to correct GSAP
- ScrollReveal works in Chrome, Firefox, Safari
- `prefers-reduced-motion` disables all animations correctly
- Animation demo page: all 20+ animation types showcased

---

### Phase 2 — 3D Engine
**Duration:** 3 weeks  
**Goal:** Three.js scenes declared in Python. Spline embeds. GLTF loading.

#### Tasks

1. **Scene3D IR node**
   - Full IR representation of Three.js scene
   - Camera config, lights, objects, controls, animation loop

2. **Three.js JavaScript generator**
   - `Scene3DCodegen` class
   - Generates: Three.js canvas setup, camera, renderer, lights, objects, animation loop
   - `requestAnimationFrame` loop for per-frame animations

3. **Geometry components**
   - All primitive geometries (Sphere, Box, Torus, Cylinder, Plane, Ring, Text3D)
   - `CustomGeometry` from vertex/face data

4. **Material system**
   - `MeshStandardMaterial`, `MeshPhysicalMaterial`, `MeshBasicMaterial`
   - `ShaderMaterial` for custom GLSL (advanced)
   - Environment map support

5. **Lighting system**
   - All light types with full parameters
   - Shadow maps enabled by default

6. **Controls**
   - `OrbitControls` with full config
   - Auto-rotate, damping, zoom limits

7. **Object animations**
   - `Float` — sinusoidal up/down
   - `Rotate` — per-frame rotation speed
   - `Pulse` — scale oscillation
   - Scroll-linked via `ScrollLinked3D`

8. **GLTF model loader**
   - `GLTFModel(src)` — async load with loading state component
   - Draco compression support
   - Cast/receive shadow

9. **ParticleSystem**
   - Configurable count, color, size, spread
   - Flow animation

10. **Spline integration**
    - Spline viewer runtime bundled locally
    - Event binding to Python handlers
    - Loading state component

11. **Responsive 3D**
    - Scene3D resizes with container
    - Pixel ratio capped at 2 for performance
    - Fallback: `Scene3D(fallback=Image(...))` for environments without WebGL

#### Deliverables
- Three.js scene renders correctly from Python declarations
- GLTF model loads from local and remote paths
- Spline embed works with event binding
- 3D scene performance: 60fps on mid-range device
- Desktop 3D: works via Qt6 WebEngine mode

---

### Phase 3 — Zolt UI: Prebuilt Component Library
**Duration:** 5 weeks  
**Goal:** 80+ production components in `zolt-ui` package. All dark-mode compatible.

#### Tasks (by week)

**Week 1 — Auth + Foundation**
- `LoginPage` (3 variants: centered, split, minimal)
- `SignupPage` (3 variants)
- `ForgotPasswordPage`
- `MagicLinkPage`
- `TwoFactorPage`
- `OnboardingFlow` (multi-step with progress)
- `AuthLayout` (wrapper)
- Design system tokens shared by all components

**Week 2 — Landing / Marketing**
- `HeroSection` (6 variants)
- `FeatureGrid`
- `FeatureShowcase`
- `PricingTable`
- `TestimonialsGrid` + `TestimonialsCarousel`
- `LogoCloud` (marquee)
- `StatsRow` (counter animation)
- `CTASection` (4 variants)
- `FAQAccordion`

**Week 3 — Dashboard**
- `AppLayout` (sidebar + topbar + content)
- `Sidebar` (collapsible)
- `Topbar`
- `StatsGrid`
- `DataTable` (sort, filter, paginate)
- `AreaChart`, `BarChart`, `LineChart`, `DonutChart`
- `ActivityFeed`
- `CommandPalette` (Cmd+K)

**Week 4 — Forms + Feedback**
- `ContactForm`
- `MultiStepForm`
- `SearchBar`
- `DateRangePicker`
- `FileUpload`
- `RichTextEditor` (Tiptap)
- `Toast`
- `Modal`
- `Drawer`
- `Tooltip`
- `ContextMenu`

**Week 5 — Navigation + E-commerce + Polish**
- `MegaNav`
- `TabBar`
- `BottomNav`
- `FloatingNav`
- `ProductCard`
- `ProductGrid`
- `CartDrawer`
- `CheckoutFlow`
- Dark mode for all 80+ components
- `zolt studio` command to browse all components
- Screenshot generation for docs

#### Deliverables
- 80+ components in `zolt-ui` PyPI package
- Every component: dark mode, accessible, animated, typed
- `zolt studio` browser shows all components with code examples
- Every component has a screenshot (auto-generated for docs)

---

### Phase 4 — Design Import System
**Duration:** 3 weeks  
**Goal:** `zolt import figma <url>` produces working Zolt component Python code.

#### Tasks

**Week 1 — Figma importer**
- Figma API client (`zolt/import/figma/api.py`)
- Node tree walker for all Figma node types
- Auto-layout → Flex/Grid mapper
- Typography extractor
- Color extractor + theme token mapper
- Code generator (class-based output)
- `zolt import figma` CLI command

**Week 2 — Framer + Webflow importers**
- HTML parser (BeautifulSoup)
- CSS → Tailwind utility reverse mapper
- Framer animation class → Zolt animate() mapper
- Webflow CMS data → Zolt reactive data mapper
- `zolt import framer` + `zolt import webflow` CLI commands

**Week 3 — Accuracy improvements + review workflow**
- Component fuzzy matcher (Figma component names → zolt-ui components)
- Confidence scoring for each mapped element
- `# TODO: [REVIEW]` comment insertion
- `zolt import review ./components/design.py` — interactive CLI review
- Import accuracy test suite (Figma test files with known outputs)

#### Deliverables
- Figma import: 85%+ accuracy on layout, typography, colours
- Framer import: 70%+ accuracy
- `zolt import review` CLI guides user through manual fixes
- Test suite with 10 real-world Figma files as test cases

---

### Phase 5 — Desktop v1.5 (Qt5 + Qt6 + WebEngine)
**Duration:** 2 weeks  
**Goal:** Qt5 fully supported. Qt6 WebEngine mode for pixel-perfect desktop apps.

#### Tasks

1. **PyQt5 renderer**
   - Full widget mapping (same as Qt6 renderer, different import paths)
   - `zolt[qt5]` extra: `pip install PyQt5 sip`
   - CI test: build desktop app with Qt5 on Ubuntu + Windows

2. **Qt6 WebEngine mode**
   - `QWebEngineView` full screen wrapper
   - Python FastAPI local server (minimal — serves static files)
   - Port management (random available port)
   - `zolt run --desktop --qt6 --webengine`
   - GSAP + Three.js work via WebEngine (full browser rendering)

3. **Qt animation bridge**
   - Pure Qt widget mode: GSAP animations translated to `QPropertyAnimation`
   - Fade, slide, scale support via Qt property animation
   - `QGraphicsEffect` for more complex effects

4. **Textual TUI upgrade**
   - Migrate CLI renderer from plain Rich to Textual
   - Mouse support, interactive forms, keyboard nav
   - `zolt run --cli --interactive` (Textual) vs `--static` (Rich)

5. **Build targets**
   - `zolt build --desktop --qt5` → PyInstaller bundle
   - `zolt build --desktop --qt6` → PyInstaller bundle
   - `zolt build --desktop --qt6-webengine` → PyInstaller + Chromium

#### Deliverables
- Qt5 renderer passes all existing Qt6 component tests
- Qt6 WebEngine demo: Three.js scene runs inside desktop app
- Textual TUI demo: interactive form submission works in terminal

---

### Phase 6 — AI-First: Skills & Docs Infrastructure
**Duration:** 2 weeks  
**Goal:** Every component has a skill file. `zolt.schema.json` covers 100% of API. LLMS.txt live.

#### Tasks

1. **Skill file format** (see Section 9 for full spec)
   - YAML format for each component
   - Auto-generated base from type hints + docstrings
   - Hand-curated examples and common patterns
   - `zolt skills validate` — checks all skill files are complete

2. **`zolt.schema.json` generator**
   - Introspects all public classes and methods
   - Generates machine-readable JSON schema
   - Published to PyPI at `zolt/schema.json`
   - Served at `zolt.dev/schema.json`

3. **`LLMS.txt` file**
   - Hand-written AI-readable summary of entire Zolt API
   - Includes common patterns, anti-patterns, and examples
   - Published at `zolt.dev/llms.txt`
   - Bundled with package at `zolt/LLMS.txt`

4. **AI correctness benchmark**
   - 20 test specs (natural language UI descriptions)
   - Feed each to Claude Code with `zolt.schema.json` context
   - Verify: output compiles, renders, matches spec
   - Target: >95% pass rate
   - Runs in CI on every release

5. **VS Code extension v1.5**
   - Schema-powered autocomplete for all Zolt classes
   - Inline prop documentation on hover
   - Error squiggles for wrong prop types
   - `ZOLT-xxxx` error codes link to docs

6. **Error code documentation**
   - Every error code has a docs page: cause, example, fix
   - Error codes searchable at `zolt.dev/errors`

#### Deliverables
- Skill files for 100% of public components (core + zolt-ui)
- `zolt.schema.json` covers 100% of API surface
- AI benchmark: >95% first-attempt correctness
- VS Code extension published to marketplace

---

### Phase 7 — Docs Website (built with Zolt)
**Duration:** 3 weeks  
**Goal:** Complete, beautiful docs site at `zolt.dev`, built entirely with Zolt v1.5, deployed on Vercel.

Full specification in Section 10.

#### Tasks

**Week 1 — Content + Structure**
- Information architecture: all pages planned and outlined
- All code examples written and tested
- Component gallery page (all 80+ zolt-ui components live)
- Getting started guide: zero to running app in 5 minutes

**Week 2 — Design + Build**
- Design: editorial dark aesthetic (Zolt's own design language)
- Hero with Three.js 3D scene
- All animations with Zolt's animation engine
- Search (Algolia DocSearch integration)
- Syntax-highlighted code blocks (Shiki)

**Week 3 — Polish + Deploy**
- Dark mode toggle
- Mobile responsive
- Lighthouse >95 on all categories
- Vercel deployment with `zolt build --web` + Vercel output
- Custom domain `zolt.dev`
- sitemap.xml + robots.txt + Open Graph images

#### Deliverables
- `zolt.dev` live and serving
- All docs pages complete
- Lighthouse score >95 on Performance, Accessibility, Best Practices, SEO
- Source code published in `zolt-framework` repo under `/docs-site`

---

### Phase 8 — Demo Artifacts (.exe + CLI Demo)
**Duration:** 2 weeks  
**Goal:** `.exe` desktop app + `zolt demo` CLI that showcase every v1.5 capability.

Full specification in Section 11.

#### Tasks

**Week 1 — Demo app design + build**
- 8-section showcase app (see Section 11)
- All animations, 3D, prebuilt components demonstrated
- Dark theme, smooth page transitions
- Built entirely with Zolt v1.5 (dogfooding)

**Week 2 — Binary packaging**
- `zolt build --desktop --qt6-webengine` → showcases 3D in desktop
- PyInstaller packaging: Windows `.exe`, macOS `.app`, Linux `.deb`
- Code-signed (Windows: signtool, macOS: notarisation)
- CI build matrix: all three platforms
- `zolt demo` CLI: interactive terminal showcase
- GitHub Releases: binaries attached on every release tag

#### Deliverables
- Windows `.exe` demo (< 120MB including Chromium)
- macOS `.app` demo
- Linux `.deb` demo
- `zolt demo` CLI command
- GitHub Release page with all artifacts

---

### Phase 9 — Production Hardening & Launch
**Duration:** 2 weeks  
**Goal:** Production quality across the board.

#### Tasks

1. **Lighthouse CI** — all example apps score >90, fail build if regression
2. **Axe accessibility audit** — all zolt-ui components pass automated audit
3. **Cross-browser testing** — Playwright: Chrome, Firefox, Safari, Edge
4. **Bundle size CI** — fail build if output size exceeds targets
5. **AI benchmark CI** — Claude Code benchmark runs on every release
6. **Performance profiling** — identify and fix any components with reflow/repaint issues
7. **Design review** — third-party design critique of all 80+ zolt-ui components
8. **Security audit** — check Figma importer does not leak tokens, bundled JS has no vulns
9. **Changelog** — complete, well-written CHANGELOG.md
10. **PyPI release** — `zolt-framework==1.5.0` and `zolt-ui==1.5.0`
11. **Launch** — HN, Reddit, Twitter, demo video, blog post

#### Deliverables
- `pip install zolt-framework==1.5.0` live
- `pip install zolt-ui==1.5.0` live
- Zero known regressions from v1.0
- All acceptance criteria met

---

## 8. Unit Test Plan — Per Phase

### Phase 0 — Build System Tests

```python
# tests/test_build/test_no_cdn.py

import subprocess, pathlib

def test_build_output_has_no_cdn_urls(tmp_app):
    """Critical: built output must contain zero external URLs."""
    result = subprocess.run(["zolt", "build", "--web"], cwd=tmp_app)
    assert result.returncode == 0

    dist = pathlib.Path(tmp_app) / "dist"
    for file in dist.rglob("*.html"):
        content = file.read_text()
        assert "cdn.tailwindcss.com" not in content
        assert "unpkg.com" not in content
        assert "cdnjs.cloudflare.com" not in content
        assert "cdn.jsdelivr.net" not in content

def test_tailwind_purges_unused_classes(tmp_app):
    from zolt.build.tailwind import TailwindBuilder
    builder = TailwindBuilder(content_dirs=[str(tmp_app / "build")])
    css = builder.build()
    # Unused class should not be in output
    assert "flex-col-reverse" not in css  # Not used in test app

def test_css_output_size_within_target(tmp_app):
    import gzip
    css_path = pathlib.Path(tmp_app) / "dist" / "style.min.css"
    compressed = len(gzip.compress(css_path.read_bytes()))
    assert compressed < 15_000, f"CSS too large: {compressed} bytes gzipped"

def test_js_bundle_no_external_imports(tmp_app):
    js = (pathlib.Path(tmp_app) / "dist" / "app.min.js").read_text()
    assert "https://" not in js
    assert "http://" not in js
```

### Phase 1 — Animation Tests

```python
# tests/test_animate/test_compile.py

def test_fade_in_compiles_to_gsap():
    from zolt import Button
    from zolt.animate import fade_in
    from zolt.renderers.web import render_animations

    btn = Button("Click").animate(fade_in(duration=0.5, delay=0.2))
    js = render_animations(btn)

    assert "gsap.from" in js
    assert "opacity: 0" in js
    assert "duration: 0.5" in js
    assert "delay: 0.2" in js

def test_stagger_compiles_correctly():
    from zolt import Grid, Text
    from zolt.animate import stagger, slide_up
    from zolt.renderers.web import render_animations

    grid = Grid(cols=3).add(Text("A"), Text("B"), Text("C")).animate(
        stagger(each=slide_up(duration=0.7), interval=0.15, trigger="scroll")
    )
    js = render_animations(grid)

    assert "scrollTrigger" in js
    assert "stagger: 0.15" in js

def test_scroll_trigger_generated():
    from zolt import Heading
    from zolt.animate import slide_up, ScrollReveal
    from zolt.renderers.web import render_animations

    h = Heading("Hello").animate(slide_up().on(ScrollReveal()))
    js = render_animations(h)
    assert "ScrollTrigger" in js
    assert "start:" in js

def test_reduced_motion_wrapper_present():
    from zolt import Button
    from zolt.animate import fade_in
    from zolt.renderers.web import render_animations

    btn = Button("X").animate(fade_in())
    js = render_animations(btn)
    assert "prefers-reduced-motion" in js
    assert "!motion.matches" in js

def test_timeline_compiles():
    from zolt import Heading, Text
    from zolt.animate import fade_in, slide_up, Timeline

    tl = (
        Timeline()
        .add(Heading("Hi"), fade_in(duration=0.5))
        .add(Text("Sub"), slide_up(duration=0.6), offset="-=0.3")
        .play_on("load")
    )
    from zolt.renderers.web import render_timeline
    js = render_timeline(tl)
    assert "gsap.timeline" in js
    assert '"-=0.3"' in js

def test_lottie_component_renders():
    from zolt.animate import Lottie
    from zolt.renderers.web import render_component

    lottie = Lottie(src="/assets/anim.json", loop=True, autoplay=True)
    html = render_component(lottie)
    assert "lottie" in html.lower()
    assert "/assets/anim.json" in html
```

### Phase 2 — 3D Engine Tests

```python
# tests/test_three/test_scene.py

def test_scene3d_generates_canvas():
    from zolt.three import Scene3D, Sphere, AmbientLight
    from zolt.renderers.web import render_component

    scene = Scene3D(height="400px").add(
        AmbientLight(intensity=0.5),
        Sphere(radius=1)
    )
    html = render_component(scene)
    assert "<canvas" in html
    assert 'height="400px"' in html or "400px" in html

def test_scene3d_generates_threejs_js():
    from zolt.three import Scene3D, Box, PointLight
    from zolt.renderers.web import render_scene_js

    scene = Scene3D().add(PointLight(), Box(width=1, height=1, depth=1))
    js = render_scene_js(scene)

    assert "THREE.Scene" in js
    assert "THREE.BoxGeometry" in js
    assert "THREE.PointLight" in js
    assert "requestAnimationFrame" in js

def test_orbit_controls_included():
    from zolt.three import Scene3D, Sphere, OrbitControls
    from zolt.renderers.web import render_scene_js

    scene = Scene3D().add(Sphere()).controls(OrbitControls(auto_rotate=True))
    js = render_scene_js(scene)
    assert "OrbitControls" in js
    assert "autoRotate = true" in js

def test_particle_system_generates():
    from zolt.three import Scene3D, ParticleSystem
    from zolt.renderers.web import render_scene_js

    scene = Scene3D().add(ParticleSystem(count=500, color="#ffffff"))
    js = render_scene_js(scene)
    assert "THREE.BufferGeometry" in js
    assert "500" in js

def test_spline_component_renders():
    from zolt.spline import Spline
    from zolt.renderers.web import render_component

    spline = Spline(url="https://prod.spline.design/abc/scene.splinecode")
    html = render_component(spline)
    assert "spline" in html.lower()
    assert "abc/scene.splinecode" in html

def test_scene3d_webgl_fallback():
    from zolt.three import Scene3D, Sphere
    from zolt import Image
    from zolt.renderers.web import render_component

    scene = Scene3D(fallback=Image(src="/fallback.png")).add(Sphere())
    html = render_component(scene)
    assert "fallback.png" in html
    assert "WebGL" in html or "webgl" in html.lower()
```

### Phase 3 — Zolt UI Tests

```python
# tests/test_zolt_ui/test_auth.py

def test_login_page_renders():
    from zolt_ui.auth import LoginPage
    from zolt.renderers.web import render_page

    page = LoginPage(providers=["google", "github"])
    html = render_page(page)
    assert "email" in html.lower()
    assert "password" in html.lower()
    assert "google" in html.lower()
    assert "github" in html.lower()

def test_login_page_variants():
    from zolt_ui.auth import LoginPage
    from zolt.renderers.web import render_page

    for variant in ["centered", "split", "minimal"]:
        page = LoginPage(variant=variant)
        html = render_page(page)
        assert html  # Should render without error

def test_pricing_table_renders_tiers():
    from zolt_ui.landing import PricingTable
    from zolt.renderers.web import render_component

    plans = [
        {"name": "Free", "price": 0, "features": ["Feature A"]},
        {"name": "Pro", "price": 29, "features": ["Feature A", "Feature B"]},
    ]
    comp = PricingTable(plans=plans)
    html = render_component(comp)
    assert "Free" in html
    assert "Pro" in html
    assert "$29" in html or "29" in html

def test_dark_mode_class_present():
    from zolt_ui.dashboard import AppLayout, StatsGrid
    from zolt.renderers.web import render_component

    layout = AppLayout(content=StatsGrid(stats=[]))
    html = render_component(layout)
    assert "dark:" in html

def test_data_table_accessibility():
    from zolt_ui.dashboard import DataTable
    from zolt.renderers.web import render_component

    table = DataTable(columns=["Name", "Email"], rows=[["Alice", "a@test.com"]])
    html = render_component(table)
    assert "<table" in html
    assert "scope=" in html      # Column headers have scope
    assert "role=" in html or "<thead" in html

# tests/test_zolt_ui/test_all_render.py — smoke test all 80+ components

def test_all_zolt_ui_components_render_without_error():
    """Every component must render to HTML without raising an exception."""
    from zolt.renderers.web import render_component
    import zolt_ui
    import inspect

    components = []
    for module_name in zolt_ui.__all__:
        module = getattr(zolt_ui, module_name)
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if hasattr(cls, "compose") or hasattr(cls, "render"):
                components.append(cls)

    errors = []
    for ComponentClass in components:
        try:
            instance = ComponentClass()  # default props only
            html = render_component(instance)
            assert html and len(html) > 10
        except Exception as e:
            errors.append(f"{ComponentClass.__name__}: {e}")

    assert not errors, f"Components failed to render:\n" + "\n".join(errors)
```

### Phase 4 — Design Import Tests

```python
# tests/test_import/test_figma.py

def test_figma_importer_maps_autolayout_to_flex(mock_figma_api):
    from zolt.import_tools.figma import FigmaImporter

    mock_figma_api.return_value = {
        "document": {
            "children": [{
                "type": "FRAME",
                "layoutMode": "HORIZONTAL",
                "itemSpacing": 16,
                "children": [
                    {"type": "TEXT", "characters": "Hello", "style": {"fontSize": 16}},
                    {"type": "RECTANGLE", "fills": [{"color": {"r": 1, "g": 0, "b": 0}}]}
                ]
            }]
        }
    }
    importer = FigmaImporter(token="test")
    result = importer._parse_node(mock_figma_api.return_value["document"]["children"][0])

    assert result.component_type == "Flex"
    assert result.props.get("direction") == "row"
    assert len(result.children) == 2

def test_figma_text_maps_to_heading_for_large_size(mock_figma_api):
    from zolt.import_tools.figma.mapper import map_text_node
    node = {"type": "TEXT", "characters": "Big Title", "style": {"fontSize": 48, "fontWeight": 700}}
    result = map_text_node(node)
    assert result.component_type in ("Heading", "Text")
    assert "48" in str(result.props) or result.component_type == "Heading"

def test_import_generates_valid_python(tmp_path, mock_figma_api):
    from zolt.import_tools.figma import FigmaImporter
    output = tmp_path / "output.py"
    importer = FigmaImporter(token="test")
    result = importer.import_file("https://figma.com/file/TEST/Mock", str(output))

    assert output.exists()
    code = output.read_text()
    # Must be valid Python
    compile(code, str(output), "exec")
    assert "from zolt" in code
    assert "class" in code or "def" in code
```

### Phase 6 — AI Skills Tests

```python
# tests/test_ai/test_skills.py

def test_all_public_components_have_skill_files():
    import zolt, zolt_ui
    from pathlib import Path

    skills_dir = Path(zolt.__file__).parent / "skills"
    public_components = [
        "Button", "Text", "Heading", "Grid", "Flex", "Stack",
        "Page", "App", "Image", "Input", "Form", "Table",
        "Scene3D", "Spline", "Lottie",
    ]
    for comp in public_components:
        skill_file = skills_dir / f"{comp}.yaml"
        assert skill_file.exists(), f"Missing skill file: {comp}.yaml"

def test_skill_file_structure_valid():
    import yaml
    from pathlib import Path
    import zolt

    skills_dir = Path(zolt.__file__).parent / "skills"
    required_keys = ["name", "description", "props", "examples", "common_patterns"]

    for skill_file in skills_dir.glob("*.yaml"):
        data = yaml.safe_load(skill_file.read_text())
        for key in required_keys:
            assert key in data, f"{skill_file.name} missing required key: {key}"

def test_schema_json_covers_all_classes():
    import json
    from pathlib import Path
    import zolt

    schema_path = Path(zolt.__file__).parent / "schema.json"
    schema = json.loads(schema_path.read_text())

    required_classes = ["App", "Page", "Button", "Text", "Heading",
                        "Grid", "Flex", "Scene3D", "Spline", "Lottie"]
    for cls in required_classes:
        assert cls in schema["classes"], f"Missing from schema: {cls}"

def test_all_props_have_types_in_schema():
    import json
    from pathlib import Path
    import zolt

    schema = json.loads((Path(zolt.__file__).parent / "schema.json").read_text())
    for cls_name, cls_def in schema["classes"].items():
        for prop_name, prop_def in cls_def.get("props", {}).items():
            assert "type" in prop_def, f"{cls_name}.{prop_name} missing type"
```

---

## 9. AI Skills System — Full Specification

### Overview

Skill files are the mechanism by which AI coding agents understand Zolt. They are structured YAML files — one per component — that describe the component's purpose, props, defaults, examples, common patterns, and anti-patterns.

Every skill file is:
- Written in YAML (machine-parseable and human-readable)
- Located at `zolt/skills/{ComponentName}.yaml`
- Bundled with the Python package
- Published at `zolt.dev/skills/{ComponentName}`
- Indexed in `zolt.schema.json`
- Listed in `LLMS.txt`

### Skill File Format

```yaml
# zolt/skills/Button.yaml

name: Button
version: "1.5.0"
description: >
  An interactive button component. Renders as an HTML <button> element on web,
  a QPushButton on Qt desktop, and a styled button in Textual TUI.
  Supports variants, sizes, icons, loading states, and animation.

category: input

props:
  label:
    type: str
    required: true
    description: The text displayed inside the button.
    example: '"Get started"'

  style:
    type: "Literal['primary', 'secondary', 'ghost', 'danger', 'success', 'outline', 'link']"
    required: false
    default: '"primary"'
    description: Visual variant of the button.
    example: '.style("primary")'

  size:
    type: "Literal['xs', 'sm', 'md', 'lg', 'xl']"
    required: false
    default: '"md"'
    description: Size of the button controlling padding and font size.
    example: '.size("lg")'

  icon:
    type: "str | None"
    required: false
    default: "None"
    description: >
      Lucide icon name displayed before the label.
      See lucide.dev for all available names.
    example: '.icon("arrow-right")'

  icon_position:
    type: "Literal['left', 'right']"
    required: false
    default: '"left"'
    description: Position of the icon relative to the label.

  loading:
    type: bool
    required: false
    default: "False"
    description: >
      When True, shows a spinner and disables the button.
      Bind to a reactive variable for async loading states.
    example: '.loading(is_submitting)'

  disabled:
    type: "bool | ReactiveVar[bool]"
    required: false
    default: "False"
    description: >
      Disables the button when True. Accepts a reactive variable
      for computed disabled states.

  full_width:
    type: bool
    required: false
    default: "False"
    description: When True, button stretches to fill its container width.

methods:
  onClick:
    signature: "onClick(handler: Callable[[], None]) -> Button"
    description: Handler called when the button is clicked.
    example: '.onClick(lambda: print("clicked"))'
    note: For async handlers use async def.

  animate:
    signature: "animate(animation: Animation) -> Button"
    description: Apply an entrance animation to the button.
    example: '.animate(fade_in(duration=0.4, delay=0.6))'

  className:
    signature: "className(*classes: str) -> Button"
    description: >
      Escape hatch for applying raw Tailwind classes.
      Use only when the built-in props are insufficient.
    example: '.className("mt-8 mx-auto")'

examples:
  basic: |
    Button("Get started")

  with_style_and_size: |
    Button("Learn more").style("ghost").size("lg")

  with_icon: |
    Button("Continue").style("primary").icon("arrow-right").icon_position("right")

  with_click_handler: |
    Button("Submit").style("primary").onClick(handle_submit)

  with_async_loading: |
    is_loading = reactive(False)

    async def handle_submit():
        is_loading.set(True)
        await save_data()
        is_loading.set(False)

    Button("Save").loading(is_loading).onClick(handle_submit)

  with_animation: |
    Button("Start").style("primary").size("lg").animate(
        slide_up(duration=0.5, delay=0.8)
    )

  disabled_state: |
    form_valid = reactive(False)
    Button("Submit").disabled(lambda: not form_valid.get())

common_patterns:
  - name: CTA button pair
    description: Primary + ghost button side by side (common hero/CTA pattern)
    code: |
      with Flex(gap=4):
          Button("Get started").style("primary").size("lg")
          Button("Learn more").style("ghost").size("lg")

  - name: Loading on submit
    description: Disable button and show spinner while async operation runs
    code: |
      submitting = reactive(False)

      async def on_submit():
          submitting.set(True)
          await api.call()
          submitting.set(False)

      Button("Submit").loading(submitting).onClick(on_submit)

  - name: Icon button
    description: Button with trailing arrow icon
    code: |
      Button("Next step").icon("arrow-right").icon_position("right")

anti_patterns:
  - name: Do not use className for spacing
    wrong: 'Button("Click").className("mt-8")'
    correct: 'Button("Click").margin(top=8)'
    reason: >
      margin() and padding() props are type-safe and target-aware.
      className() only applies to web output.

  - name: Do not hardcode colors
    wrong: 'Button("Click").className("bg-[#6C63FF] text-white")'
    correct: 'Button("Click").style("primary")'
    reason: >
      Hardcoded colors break dark mode and theme switching.
      style() variants use theme tokens automatically.

targets:
  web: full
  desktop_qt5: full
  desktop_qt6: full
  desktop_tk: partial     # loading state not animated
  cli_textual: full
  cli_rich: basic         # no loading state, no icon

related_components:
  - IconButton
  - ButtonGroup
  - LinkButton

since: "1.0.0"
last_updated: "1.5.0"
```

### LLMS.txt Format

Published at `zolt.dev/llms.txt` and bundled at `zolt/LLMS.txt`:

```
# Zolt Framework v1.5 — AI-Readable API Reference
# Generated: 2026-04-01
# Full schema: https://zolt.dev/schema.json
# Skill files: https://zolt.dev/skills/

## CORE RULES (read first)
1. Every Zolt app inherits from App. Pages are class attributes.
2. All component methods are chainable and return Self.
3. Event handlers: onClick, onChange, onSubmit, onHover, onFocus, onBlur, onMount, onUnmount
4. Never use className() for spacing — use margin() and padding()
5. Never hardcode colors — use style() variants which respect the theme
6. All sizes: "xs", "sm", "md", "lg", "xl" — consistent across all components
7. Animations: always import from zolt.animate — never write JavaScript
8. 3D: always import from zolt.three — never write Three.js manually

## MINIMAL EXAMPLE
from zolt import App, Page, Heading, Button, Text

class MyApp(App):
    home = Page(title="Home", route="/")
    home.add(
        Heading("Hello World", level=1),
        Text("Built with Zolt."),
        Button("Get started").style("primary").onClick(go_somewhere)
    )

## ANIMATED EXAMPLE
from zolt import App, Page, Heading, Button
from zolt.animate import fade_in, slide_up, stagger

class AnimatedApp(App):
    home = Page(title="Home", route="/")
    home.add(
        Heading("Hello").animate(slide_up(duration=0.8)),
        Button("Start").animate(fade_in(duration=0.5, delay=0.4))
    )

## 3D EXAMPLE
from zolt import App, Page
from zolt.three import Scene3D, Torus, PointLight, OrbitControls

class ThreeDApp(App):
    home = Page(title="3D Demo", route="/")
    home.add(
        Scene3D(height="500px").add(
            PointLight(intensity=1.0),
            Torus(radius=1).material(color="#6C63FF").animate(Float(speed=1.5))
        ).controls(OrbitControls(auto_rotate=True))
    )

## PREBUILT COMPONENTS
from zolt_ui import LoginPage, HeroSection, PricingTable, AppLayout

class SaaSApp(App):
    home = Page(route="/")
    home.add(
        HeroSection(title="My SaaS", subtitle="Description", variant="centered"),
        PricingTable(plans=my_plans)
    )
    login = LoginPage(providers=["google"], on_success=go_to_dashboard)

## IMPORT FROM FIGMA
# Run in terminal:
# zolt import figma https://figma.com/file/ABC123/MyDesign
# This generates components/design.py with your Figma design as Zolt code.

## ERROR CODE FORMAT
# ZOLT-1501: Button.size must be one of: "xs", "sm", "md", "lg", "xl". Got: "large"
# Fix: change to .size("lg")
```

### Schema Generator

```python
# zolt/schema/generator.py

def generate_schema() -> dict:
    """
    Introspects all public Zolt classes and generates pyui.schema.json.
    Run automatically on every zolt build and zolt release.
    """
    schema = {
        "version": zolt.__version__,
        "generated": datetime.utcnow().isoformat(),
        "classes": {},
        "patterns": {},
        "error_codes": {}
    }

    for cls in get_all_public_components():
        schema["classes"][cls.__name__] = {
            "description": cls.__doc__ or "",
            "category": getattr(cls, "__category__", "component"),
            "since": getattr(cls, "__since__", "1.0.0"),
            "props": extract_props(cls),
            "methods": extract_methods(cls),
            "targets": getattr(cls, "__targets__", {
                "web": "full", "desktop_qt5": "full",
                "desktop_qt6": "full", "cli": "partial"
            })
        }

    return schema
```

---

## 10. Docs Website Specification

### Overview

The Zolt docs site is built entirely with Zolt v1.5. It is the most visible demonstration of what Zolt can produce — it must be Awwwards-quality. It serves as both documentation and marketing.

**URL:** `zolt.dev`  
**Deployment:** Vercel (via `zolt build --web` output)  
**Source:** `/docs-site/` in the main repo  
**Framework:** Zolt v1.5 (obviously)  

### Page Architecture

```
/ (home)
├── /docs
│   ├── /docs/getting-started
│   │   ├── /docs/getting-started/installation
│   │   ├── /docs/getting-started/your-first-app
│   │   └── /docs/getting-started/concepts
│   ├── /docs/components
│   │   ├── /docs/components/[component-name]  (80+ pages, one per component)
│   ├── /docs/animation
│   │   ├── /docs/animation/overview
│   │   ├── /docs/animation/[animation-name]
│   ├── /docs/3d
│   │   ├── /docs/3d/overview
│   │   ├── /docs/3d/scene3d
│   │   ├── /docs/3d/spline
│   ├── /docs/design-import
│   │   ├── /docs/design-import/figma
│   │   ├── /docs/design-import/framer
│   ├── /docs/themes
│   ├── /docs/ai-usage
│   └── /docs/deployment
├── /components   (live gallery — all 80+ zolt-ui components)
├── /showcase     (community showcase — sites built with Zolt)
├── /errors       (every error code, searchable)
└── /changelog
```

### Design Specification

**Aesthetic:** Dark editorial. Deep obsidian background, phosphor green accents, chalk-white typography. Premium, confident, developer-focused.

**Typography:**
- Display: Playfair Display (editorial headlines)
- Code: JetBrains Mono (all code blocks)
- Body: Geist (clean, modern, reads well at 14–16px)

**Key sections on home page:**

1. **Hero** — Three.js particle field background, animated headline reveal, `pip install zolt-framework` terminal block, two CTAs
2. **Code demo** — Live split-screen: Python on left, rendered output on right (interactive, tabbed)
3. **Animation showcase** — Each animation type demonstrated in cards that trigger on scroll
4. **3D showcase** — Three.js torus, particle system, Spline embed, all live
5. **Zolt UI gallery** — Grid of 12 component screenshots with hover previews
6. **Design import demo** — Before/after: Figma screenshot → Zolt component code
7. **AI section** — "Claude Code builds this with zero errors" demo
8. **Testimonials** — Early adopters

**Component docs page structure:**

Each component at `/docs/components/Button`:
1. Hero: component name, description, `from zolt import Button`
2. Live demo: interactive component preview
3. Props table: all props with types, defaults, descriptions
4. Code examples: tabbed, multiple variants
5. Animation section: how to animate this component
6. Accessibility notes
7. Target compatibility table
8. Related components

### Vercel Deployment

```python
# docs-site/app.py — the Zolt app that IS the docs site

class ZoltDocs(App):
    name = "Zolt Documentation"
    theme = "dark"
    fonts = ["Geist", "Playfair Display", "JetBrains Mono"]

    # All pages auto-discovered from /docs-site/pages/
    # Zolt's router maps .py files to routes automatically

# vercel.json — generated by `zolt build --web --vercel`
{
  "buildCommand": "pip install zolt-framework && zolt build --web",
  "outputDirectory": "dist",
  "framework": null
}
```

### Lighthouse Targets

| Category | Target |
|---|---|
| Performance | > 95 |
| Accessibility | > 97 |
| Best Practices | > 95 |
| SEO | > 95 |

---

## 11. Demo Artifacts Specification

### Desktop Demo App

**Name:** Zolt Demo  
**Purpose:** Show every v1.5 capability in one beautiful native app  
**Build:** `zolt build --desktop --qt6-webengine` (full browser in native window)

**App sections (8 screens, navigated via sidebar):**

1. **Welcome** — Full-screen 3D hero with rotating torus, particle system, animated headline
2. **Components** — Live showcase of all major components with code toggle
3. **Animation** — Every animation type demonstrated with controls (duration, ease sliders)
4. **3D** — Interactive Three.js scene, Spline embed, GLTF model viewer
5. **Zolt UI** — Live preview of auth pages, dashboards, pricing tables
6. **Design Import** — Side-by-side: Figma JSON → Zolt code → rendered output
7. **Themes** — Real-time theme switcher across all 8 built-in themes
8. **Build Output** — Show bundle sizes, Lighthouse scores, output files

**Distribution:**

| Platform | Format | Size target |
|---|---|---|
| Windows | `ZoltDemo-1.5.0-win64.exe` | < 120MB |
| macOS | `ZoltDemo-1.5.0-macos.dmg` | < 130MB |
| Linux | `ZoltDemo-1.5.0-amd64.deb` | < 115MB |

All binaries attached to GitHub Release `v1.5.0`.

### CLI Demo

**Command:** `zolt demo`  
**Mode:** Interactive Textual TUI  
**Purpose:** Demonstrate framework capabilities without opening a browser

**CLI demo flow:**

```
$ zolt demo

╔══════════════════════════════════════════╗
║        ZOLT v1.5 — Interactive Demo      ║
╚══════════════════════════════════════════╝

What would you like to explore?

  ▸ 1. Components overview
    2. Animation system
    3. 3D capabilities
    4. Zolt UI — prebuilt components
    5. Design import (Figma)
    6. AI usage with skill files
    7. Build a mini app live
    8. Exit

> 7

Building a mini app live — type your spec and watch it compile...
Spec: "A landing page with a hero, pricing table, and contact form"

✓ Generating component tree...
✓ Compiling to HTML...
✓ Starting dev server at http://localhost:9999

Opening in browser... (press Ctrl+C to return to demo)
```

---

## 12. File & Folder Structure v1.5

```
zolt/
├── pyproject.toml
├── LLMS.txt                          # AI-readable API summary
├── schema.json                       # Auto-generated API schema
├── CHANGELOG.md
│
├── src/
│   └── zolt/
│       ├── __init__.py               # Public exports
│       ├── exceptions.py             # ZOLT-1500 to ZOLT-1599
│       │
│       ├── app.py                    # App base class
│       ├── page.py                   # Page class
│       │
│       ├── components/               # V1.0 components (unchanged)
│       │   ├── base.py
│       │   ├── layout/
│       │   ├── navigation/
│       │   ├── input/
│       │   ├── display/
│       │   ├── feedback/
│       │   └── data/
│       │
│       ├── animate/                  # NEW — Animation engine
│       │   ├── __init__.py           # All animation functions exported
│       │   ├── animations.py         # fade_in, slide_up, etc.
│       │   ├── timeline.py           # Timeline class
│       │   ├── scroll_reveal.py      # ScrollReveal, ScrollLinked3D
│       │   ├── interactive.py        # magnetic, tilt_3d, parallax
│       │   ├── text.py               # typewriter, counter, word_by_word
│       │   └── lottie.py             # Lottie, Rive components
│       │
│       ├── three/                    # NEW — 3D engine
│       │   ├── __init__.py
│       │   ├── scene.py              # Scene3D class
│       │   ├── geometry.py           # Sphere, Box, Torus, etc.
│       │   ├── material.py           # MeshStandardMaterial, etc.
│       │   ├── lights.py             # All light types
│       │   ├── controls.py           # OrbitControls
│       │   ├── particles.py          # ParticleSystem
│       │   ├── loaders.py            # GLTFModel
│       │   └── helpers.py            # Float, Rotate, Pulse
│       │
│       ├── spline.py                 # NEW — Spline component
│       │
│       ├── import_tools/             # NEW — Design import
│       │   ├── __init__.py
│       │   ├── figma/
│       │   │   ├── api.py            # Figma REST client
│       │   │   ├── walker.py         # Node tree walker
│       │   │   ├── mapper.py         # Figma → Zolt mapping
│       │   │   ├── styles.py         # Style extractor
│       │   │   └── codegen.py        # Python code generator
│       │   ├── framer/
│       │   │   ├── parser.py         # HTML parser
│       │   │   └── mapper.py
│       │   └── webflow/
│       │       ├── parser.py
│       │       └── mapper.py
│       │
│       ├── compiler/                 # Extended from v1.0
│       │   ├── ir.py                 # AnimationNode, Scene3DNode added
│       │   ├── discovery.py
│       │   ├── walker.py
│       │   └── validator.py          # ZOLT-1500+ error codes
│       │
│       ├── renderers/
│       │   ├── web/
│       │   │   ├── generator.py      # Extended for animation + 3D
│       │   │   ├── animation_codegen.py  # NEW — GSAP JS generator
│       │   │   ├── scene3d_codegen.py    # NEW — Three.js JS generator
│       │   │   └── templates/
│       │   ├── desktop/
│       │   │   ├── tkinter_renderer.py   # V1.0 (kept)
│       │   │   ├── qt5_renderer.py       # NEW
│       │   │   ├── qt6_renderer.py       # Extended from v1.0
│       │   │   └── qt6_webengine.py      # NEW
│       │   └── cli/
│       │       ├── rich_renderer.py      # V1.0 (kept, for --static)
│       │       └── textual_renderer.py   # NEW (for --interactive)
│       │
│       ├── build/                    # NEW — Production build
│       │   ├── tailwind.py           # TailwindBuilder
│       │   ├── bundler.py            # esbuild wrapper
│       │   ├── images.py             # Image optimiser (Pillow)
│       │   └── pipeline.py           # Orchestrates all build steps
│       │
│       ├── theme/                    # Extended from v1.0
│       │   ├── tokens.py             # Extended token set
│       │   ├── engine.py             # Theme v2
│       │   └── built_in/             # 8 themes
│       │
│       ├── schema/                   # NEW — AI compatibility
│       │   ├── generator.py          # Generates schema.json
│       │   └── validator.py
│       │
│       ├── skills/                   # NEW — AI skill files
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
│       │   ├── fade_in.yaml
│       │   ├── slide_up.yaml
│       │   ├── Timeline.yaml
│       │   └── ... (one per public component/function)
│       │
│       ├── state/                    # V1.0 (unchanged)
│       ├── server/                   # V1.0 (unchanged)
│       ├── hotreload/                # V1.0 (unchanged)
│       ├── plugins/                  # V1.0 (unchanged)
│       └── cli/
│           ├── main.py               # Extended
│           └── commands/
│               ├── run.py, build.py, new.py  # Extended
│               ├── import_cmd.py     # NEW — zolt import
│               ├── studio.py         # NEW — zolt studio
│               └── demo.py           # NEW — zolt demo
│
├── zolt-ui/                          # Separate package
│   ├── pyproject.toml
│   └── src/zolt_ui/
│       ├── __init__.py
│       ├── auth/
│       ├── landing/
│       ├── dashboard/
│       ├── ecommerce/
│       ├── forms/
│       ├── feedback/
│       └── navigation/
│
├── docs-site/                        # The docs website (built with Zolt)
│   ├── app.py
│   └── pages/
│
├── tests/
│   ├── v1/                           # All v1.0 tests (must pass)
│   └── v1_5/
│       ├── test_build/
│       ├── test_animate/
│       ├── test_three/
│       ├── test_zolt_ui/
│       ├── test_import/
│       ├── test_ai/
│       └── integration/
│
└── examples/
    ├── v1/                           # V1.0 examples
    └── v1_5/
        ├── animated-landing/
        ├── 3d-hero/
        ├── dashboard-with-ui/
        ├── figma-imported/
        └── full-saas-landing/
```

---

## 13. Dependencies & Versions

### Core Runtime (added in v1.5)

| Package | Version | Purpose |
|---|---|---|
| `pytailwindcss` | >=0.2.0 | Tailwind CSS CLI as Python package |
| `textual` | >=0.62 | Interactive TUI renderer |
| `lxml` | >=5.0 | Figma/Framer HTML parsing |
| `beautifulsoup4` | >=4.12 | HTML parsing for import |
| `httpx` | >=0.27 | Figma API calls |
| `PyYAML` | >=6.0 | Skill file parsing |
| `Pillow` | >=10.0 | Image optimisation |

### Optional Extras

| Extra | Packages | Unlocks |
|---|---|---|
| `[web]` | `pytailwindcss` + `zolt-bundler` | Full web build (required for production) |
| `[qt5]` | `PyQt5>=5.15`, `sip>=6.0` | Qt5 desktop renderer |
| `[qt6]` | `PyQt6>=6.6` | Qt6 desktop renderer (default enhanced) |
| `[qt6-webengine]` | `PyQt6-WebEngine>=6.6` | Qt6 desktop with full browser |
| `[import]` | `httpx`, `lxml`, `beautifulsoup4` | Design import (Figma, Framer, Webflow) |
| `[all]` | Everything above | All features |

### Separate Package: `zolt-ui`

```toml
[project]
name = "zolt-ui"
dependencies = ["zolt-framework>=1.5.0"]
```

### Bundled JavaScript (managed by `zolt-bundler`, not installed by user)

| Library | Version | Size (gzip) | Purpose |
|---|---|---|---|
| GSAP | 3.12 | ~38KB | Animation engine |
| GSAP ScrollTrigger | 3.12 | ~12KB | Scroll animations |
| Three.js | r169 | ~160KB | 3D engine |
| Alpine.js | 3.14 | ~15KB | Reactivity |
| Lottie-web | 5.12 | ~65KB | Lottie animations |
| @rive-app/canvas | 2.x | ~40KB | Rive animations |
| Spline viewer | latest | ~120KB | Spline 3D embeds |
| Tiptap | 2.x | ~80KB | Rich text editor |

Note: Three.js, Lottie, Rive, and Spline are only bundled when the corresponding components are used (tree-shaken by esbuild).

---

## 14. Migration Guide — V1.0 → V1.5

### Zero breaking changes

All v1.0 code works in v1.5 without modification. V1.5 only adds.

### What you need to do

```bash
# 1. Update the package
pip install --upgrade zolt-framework

# 2. Install web extras (required for production builds)
pip install zolt[web]

# 3. Optionally install Zolt UI
pip install zolt-ui
```

### What changes automatically

- `zolt run --web` now uses local Tailwind (no CDN). First run slightly slower (Tailwind downloads).
- `zolt build --web` output is now fully self-contained. Verify with `zolt build --analyze`.
- `zolt run --cli` now defaults to Textual interactive mode. Use `--static` for old Rich output.

### New capabilities (opt-in)

```python
# Add animations to existing components — just chain .animate()
Heading("Hello").animate(slide_up(duration=0.8))  # No other changes needed

# Add 3D to existing pages — just add Scene3D
home.add(Scene3D(height="400px").add(Sphere()))

# Use prebuilt components
from zolt_ui import LoginPage
login = LoginPage(providers=["google"])

# Import your Figma design
# zolt import figma https://figma.com/file/...
```

---

## 15. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Figma API changes break importer | Medium | High | Version-lock Figma API version; integration tests with saved API responses |
| esbuild binary fails on niche platforms | Medium | Medium | Ship binaries for Win/Mac/Linux x64 and ARM; fallback to npm esbuild |
| Three.js bundle size too large | Low | Medium | Code-split: only bundle Three.js when Scene3D is used; document size impact |
| Qt5 EOL / incompatibility issues | Medium | Low | Qt5 support is best-effort; Qt6 is primary; tkinter always available as fallback |
| Zolt UI components don't match user expectations | Medium | High | Public preview of all 80 components before launch; community feedback period |
| Figma import accuracy disappoints users | High | Medium | Set clear expectations (80% accuracy, always needs review); frame as a time-saver not perfect converter |
| Docs site build reveals framework gaps | Low | High | Build docs site in Phase 7 — late enough that all v1.5 features are stable |
| Demo .exe too large to download | Low | Medium | Qt6 WebEngine adds Chromium (~100MB); offer lightweight version without WebEngine |
| GSAP licensing | Low | High | GSAP is free for personal and commercial use (GreenSock Public License); verify for PyPI distribution |
| Scope too large for one release | High | High | Phase 9 can cut mobile/Rive/Webflow import if needed; core (build system + animation + 3D + Zolt UI) is non-negotiable |

---

## 16. Glossary

| Term | Definition |
|---|---|
| **Zolt** | The framework name (formerly PyUI). Python → UI framework targeting web, desktop, and CLI |
| **zolt-ui** | Separate PyPI package containing 80+ prebuilt production components |
| **zolt-bundler** | Internal Python package wrapping esbuild for JavaScript bundling |
| **pytailwindcss** | Third-party Python package wrapping the Tailwind CSS CLI |
| **Animation engine** | Zolt's Python-to-GSAP compilation layer for all animations |
| **3D engine** | Zolt's Python-to-Three.js compilation layer for 3D scenes |
| **Skill file** | A YAML file describing one Zolt component's API, props, examples, and patterns — consumed by AI agents |
| **LLMS.txt** | An AI-readable plain text file summarising Zolt's entire API, following the emerging web standard |
| **Design import** | The `zolt import` CLI command that converts Figma/Framer/Webflow designs to Zolt Python code |
| **Scene3D** | A Zolt component that renders a Three.js canvas with lights, objects, and controls |
| **Spline** | A Zolt component that embeds a Spline.design 3D scene |
| **Lottie** | A Zolt component that renders Lottie JSON animations |
| **Rive** | A Zolt component that renders Rive interactive animations |
| **Timeline** | A GSAP timeline declared in Python — sequences multiple animations |
| **ScrollReveal** | Animation trigger that fires when a component enters the viewport |
| **Qt5 renderer** | Desktop renderer using PyQt5 widgets |
| **Qt6 WebEngine** | Desktop renderer using PyQt6 with embedded Chromium — full browser inside a native window |
| **Textual renderer** | Interactive CLI renderer using the Textual TUI framework |
| **Bundle** | The esbuild-produced JavaScript output: GSAP + Alpine.js + Three.js + app logic in one file |
| **Purged CSS** | Tailwind CSS output with all unused classes removed — typically < 15KB gzipped |
| **zolt studio** | CLI command that opens a browser gallery of all Zolt and Zolt UI components |
| **zolt demo** | CLI command that opens an interactive Textual TUI demo of framework capabilities |
| **Tree-shaking** | esbuild feature that removes unused JavaScript from the bundle output |
| **IR** | Intermediate Representation — the target-agnostic tree built by the Zolt compiler before rendering |

---

*Zolt v1.5 PRD + TRD — Version 1.5.0-draft*  
*Zero breaking changes from v1.0.*  
*Cross-reference with Zolt v1.0 PRD for base specification.*  
*Cross-reference with Zolt v2.0 PRD for full-stack roadmap.*
