# PyUI — Product & Technical Requirements Document

**Version:** 0.1.0  
**Status:** Phase 3 Complete — Phase 3.5 Stabilization In Progress  
**Author:** PyUI Core Team  
**Last Updated:** April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Requirements (PRD)](#2-product-requirements-prd)
   - 2.1 Problem Statement
   - 2.2 Vision & Goals
   - 2.3 Target Users
   - 2.4 User Personas
   - 2.5 Core Features
   - 2.6 Non-Goals
   - 2.7 Success Metrics
   - 2.8 Competitive Analysis
3. [Technical Requirements (TRD)](#3-technical-requirements-trd)
   - 3.1 System Architecture
   - 3.2 Component Hierarchy & API Design
   - 3.3 Compiler & Renderer Architecture
   - 3.4 State Management System
   - 3.5 Theme Engine
   - 3.6 Component Marketplace
   - 3.7 CLI Toolchain
   - 3.8 Hot Reload System
4. [**Phase 3.5 — Stabilization & Foundation Hardening**](#phase-35--stabilization--foundation-hardening) ← **CURRENT**
5. [Development Phases](#5-development-phases)
6. [Unit Test Plan — Per Phase](#6-unit-test-plan--per-phase)
7. [File & Folder Structure](#7-file--folder-structure)
8. [Dependencies & Third-Party Libraries](#8-dependencies--third-party-libraries)
9. [Risks & Mitigations](#9-risks--mitigations)
10. [Glossary](#10-glossary)
   - 3.9 Plugin System
   - 3.10 Performance Requirements
   - 3.11 Security Requirements
   - 3.12 Accessibility Requirements
4. [Development Phases](#4-development-phases)
   - Phase 0: Project Setup & Foundations (Done)
   - Phase 1: Core Compiler (Web) (Done)
   - Phase 2: Component Library (Done)
   - Phase 3: State & Reactivity (Done)
   - Phase 4: Desktop & CLI Renderers
   - Phase 5: Theme Engine & Marketplace
   - Phase 6: Developer Tooling & Hot Reload
   - Phase 7: Production Hardening
   - Phase 8: Public Launch
5. [Unit Test Plan — Per Phase](#5-unit-test-plan--per-phase)
6. [File & Folder Structure](#6-file--folder-structure)
7. [Dependencies & Third-Party Libraries](#7-dependencies--third-party-libraries)
8. [Risks & Mitigations](#8-risks--mitigations)
9. [Glossary](#9-glossary)

---

## 1. Executive Summary

PyUI is an open-source Python framework that lets developers build beautiful, production-grade user interfaces using only Python — no HTML, no CSS, no JavaScript knowledge required. A single Python codebase compiles to three output targets: web browser (HTML/CSS/JS), desktop application (native via tkinter/PyQt), and terminal UI (Rich-based TUI).

PyUI's philosophy is **"write once, render anywhere"** with a Python-class-based API that reads like natural English, a reactive state system, a built-in theme engine, and a component marketplace.

---

## 2. Product Requirements (PRD)

### 2.1 Problem Statement

Building UIs in Python today is fragmented and painful:

- **Web UIs** require learning HTML, CSS, JavaScript, and a frontend framework (React, Vue, etc.) — a completely separate skill tree from Python.
- **Desktop UIs** with tkinter or PyQt have outdated aesthetics and verbose, unintuitive APIs.
- **CLI UIs** require separate libraries (Rich, Textual) with their own paradigms.
- **No unified solution** exists that targets all three from a single, elegant Python codebase.

Data scientists, backend engineers, and Python learners who have brilliant ideas are blocked by the frontend barrier. They either ship ugly UIs or don't ship at all.

### 2.2 Vision & Goals

**Vision:** Any Python developer should be able to build a production-quality UI in under an hour, without learning a new language or paradigm.

**Primary Goals:**

- Provide a clean, Pythonic class-based API to define UI components and pages
- Compile Python UI code to web (HTML/CSS/JS), desktop (native), and CLI (terminal) targets
- Deliver beautiful default styling out of the box — zero design knowledge needed
- Make state management trivially simple with a `@reactive` decorator pattern
- Support a community component marketplace (`pip install pyui-charts`)

**Secondary Goals:**

- Hot reload during development (save file → UI updates instantly)
- Full accessibility compliance (WCAG 2.1 AA for web output)
- Internationalisation (i18n) support built in
- Exportable static sites from web output

### 2.3 Target Users

| User Type | Description | Pain Today |
|---|---|---|
| Python beginners | Learning Python, want to build something visual | No path from Python to UI without learning JS |
| Data scientists | Build ML models, need dashboards | Streamlit is limited; Gradio is narrow |
| Backend developers | Build APIs, need internal tools | Frontend is a separate project |
| Students | Academic projects, demos | Can't make it look good |
| Indie hackers | Ship products fast | Too slow to learn two stacks |

### 2.4 User Personas

**Persona A — Ayesha, Data Scientist**
Ayesha trains ML models all day. She needs a dashboard to visualise model metrics and let non-technical colleagues run inference. She knows Python deeply but has never written a line of JavaScript. She wants to `pip install pyui` and be done in an afternoon.

**Persona B — Bilal, CS Student**
Bilal is building a final-year project — a task manager app. He wants it to look modern, run as a desktop app, and maybe deploy it to the web. He has 2 weeks and zero frontend experience.

**Persona C — Sara, Backend Engineer**
Sara's team needs an internal admin dashboard for their Django app. She doesn't want to introduce a React frontend or hire a frontend developer. She wants to write it in Python alongside her existing codebase.

### 2.5 Core Features

#### F1 — Python Class-Based UI API
Users define UI using Python classes and method chaining. No templates, no DSLs, no configuration files.

```python
from pyui import App, Page, Button, Grid, Card, Hero, Nav

class MyApp(App):
    nav = Nav(logo="MyApp", links=["Home", "About", "Contact"])
    
    home = Page(title="Home", route="/")
    home.add(
        Hero(title="Hello, World", subtitle="Built with PyUI"),
        Grid(cols=3).add(
            Card(title="Fast", icon="zap", body="Compiles to native code"),
            Card(title="Beautiful", icon="sparkles", body="Gorgeous by default"),
            Card(title="Simple", icon="feather", body="Pure Python"),
        ),
        Button("Get Started").style("primary").size("lg").onClick(go_to_about)
    )
```

#### F2 — Multi-Target Compiler
```bash
pyui run --web        # Starts dev server on localhost:8000
pyui run --desktop    # Opens as native desktop window
pyui run --cli        # Renders in terminal

pyui build --web      # Outputs /dist with static HTML/CSS/JS
pyui build --desktop  # Outputs platform-specific executable
```

#### F3 — Reactive State Management
```python
from pyui import App, Page, Text, Button, reactive

class Counter(App):
    count = reactive(0)
    
    home = Page()
    home.add(
        Text(lambda: f"Count: {Counter.count}"),
        Button("Increment").onClick(lambda: Counter.count.set(Counter.count + 1))
    )
```

Any component bound to a `reactive` variable auto-updates when the value changes.

#### F4 — Theme Engine
```python
# Built-in themes
app.theme("light")     # Default
app.theme("dark")
app.theme("ocean")
app.theme("sunset")
app.theme("forest")

# Custom themes
app.theme({
    "primary": "#6C63FF",
    "background": "#FAFAFA",
    "text": "#1A1A2E",
    "font": "Inter",
    "radius": "8px"
})
```

#### F5 — Built-in Component Library
Full set of production-ready components:

- **Layout:** Page, Grid, Flex, Stack, Divider, Spacer, Container, Sidebar, Split
- **Navigation:** Nav, Tabs, Breadcrumb, Pagination, Sidebar, Menu
- **Input:** Button, Input, Textarea, Select, Checkbox, Radio, Toggle, Slider, DatePicker, FilePicker, Form
- **Display:** Text, Heading, Badge, Tag, Avatar, Icon, Image, Video, Markdown
- **Feedback:** Alert, Toast, Modal, Drawer, Tooltip, Progress, Spinner, Skeleton
- **Data:** Table, DataGrid, Chart (line, bar, pie, area), Stat, KPI, Timeline
- **Advanced:** CodeBlock, Map, Calendar, RichEditor, Kanban, TreeView

#### F6 — Hot Reload
During `pyui run`, the dev server watches for file changes and pushes updates to the browser/window via WebSocket — no manual refresh needed.

#### F7 — Component Marketplace
```bash
pip install pyui-charts      # Advanced chart components
pip install pyui-maps        # Map components
pip install pyui-auth        # Auth UI flows (login, signup, 2FA)
pip install pyui-admin       # Full admin panel components
```

Third-party components register via PyUI's plugin API and appear in the component tree like built-ins.

#### F8 — CLI Toolchain
```bash
pyui new my-app           # Scaffold a new project
pyui new my-app --template dashboard  # From template
pyui run                  # Run dev server (web by default)
pyui build                # Production build
pyui publish              # Publish component to marketplace
pyui doctor               # Check environment health
pyui lint                 # Lint component definitions
```

### 2.6 Non-Goals

The following are explicitly out of scope for v1.0:

- Native mobile (iOS/Android) output — planned for v2.0
- Visual drag-and-drop builder UI
- Server-side rendering (SSR) beyond static export
- Database ORM or backend logic (PyUI is UI-only)
- Full WYSIWYG editor for non-developers
- React or Vue component interoperability in v1.0

### 2.7 Success Metrics

| Metric | Target (6 months post-launch) |
|---|---|
| PyPI downloads | 50,000/month |
| GitHub stars | 5,000 |
| Community components | 50+ packages |
| Docs page visits | 100,000/month |
| Discord members | 2,000 |
| Issues resolved within 7 days | >80% |
| Build time for 50-component app | <3 seconds |
| Hot reload latency | <200ms |

### 2.8 Competitive Analysis

| Tool | Language | Web | Desktop | CLI | Beautiful defaults | Reactive | Verdict |
|---|---|---|---|---|---|---|---|
| **PyUI** | Python | Yes | Yes | Yes | Yes | Yes | Full-stack UI |
| Streamlit | Python | Yes | No | No | Partial | Partial | Data apps only |
| Gradio | Python | Yes | No | No | Limited | No | ML demos only |
| Dash | Python | Yes | No | No | Partial | Partial | Dashboards only |
| tkinter | Python | No | Yes | No | No | No | Outdated |
| Textual | Python | No | No | Yes | Yes | Yes | TUI only |
| Flet | Python | Yes | Yes | No | Partial | Partial | Closest competitor |

**PyUI's unique position:** The only Python UI framework that targets all three output surfaces with a single, beautiful, reactive API.

---

## 3. Technical Requirements (TRD)

### 3.1 System Architecture

PyUI is structured in four layers:

```
┌─────────────────────────────────────────────────────┐
│                  User Python Code                    │
│         (App classes, Pages, Components)             │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                 PyUI Core Layer                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│  │ Component│ │  State   │ │    Theme Engine       │ │
│  │ Registry │ │  Store   │ │                       │ │
│  └──────────┘ └──────────┘ └──────────────────────┘ │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│               Compiler / Parser Layer                │
│  ┌────────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │ AST Walker │ │ IR Tree  │ │  Code Generator   │  │
│  └────────────┘ └──────────┘ └───────────────────┘  │
└─────────┬────────────────────────────┬──────────────┘
          │                            │
┌─────────▼──────┐  ┌────────────┐  ┌─▼─────────────┐
│  Web Renderer  │  │  Desktop   │  │  CLI Renderer  │
│  HTML/CSS/JS   │  │  Renderer  │  │  Rich/Textual  │
│  + Tailwind    │  │  tkinter/  │  │                │
│  + Alpine.js   │  │  PyQt6     │  │                │
└────────────────┘  └────────────┘  └────────────────┘
```

**Layer responsibilities:**

- **User Layer:** Pure Python. Users define `App` subclasses with `Page` attributes and `Component` trees.
- **Core Layer:** Manages the component registry, the reactive state store, theme tokens, and plugin loading.
- **Compiler Layer:** Walks the user's class tree, builds an intermediate representation (IR) tree, then dispatches to the appropriate code generator for the chosen target.
- **Renderer Layer:** Target-specific backends that consume the IR and produce output — HTML files + a dev server (web), a native window (desktop), or a terminal layout (CLI).

### 3.2 Component Hierarchy & API Design

#### Base Class Hierarchy

```
BaseComponent
├── LayoutComponent
│   ├── Page
│   ├── Grid
│   ├── Flex
│   ├── Stack
│   ├── Container
│   ├── Sidebar
│   └── Split
├── NavigationComponent
│   ├── Nav
│   ├── Tabs
│   ├── Breadcrumb
│   └── Pagination
├── InputComponent
│   ├── Button
│   ├── Input
│   ├── Select
│   ├── Checkbox
│   ├── Toggle
│   ├── Slider
│   └── Form
├── DisplayComponent
│   ├── Text
│   ├── Heading
│   ├── Image
│   ├── Badge
│   ├── Icon
│   └── Markdown
├── FeedbackComponent
│   ├── Alert
│   ├── Toast
│   ├── Modal
│   ├── Tooltip
│   └── Progress
└── DataComponent
    ├── Table
    ├── Chart
    └── Stat
```

#### BaseComponent API Contract

Every component inherits from `BaseComponent` and supports the following chainable methods:

```python
class BaseComponent:
    def style(self, variant: str) -> Self          # "primary", "ghost", "danger", etc.
    def size(self, size: str) -> Self              # "xs", "sm", "md", "lg", "xl"
    def margin(self, *args) -> Self                # CSS-like shorthand
    def padding(self, *args) -> Self
    def width(self, value: str | int) -> Self
    def height(self, value: str | int) -> Self
    def hidden(self, condition: bool | Reactive) -> Self
    def disabled(self, condition: bool | Reactive) -> Self
    def id(self, identifier: str) -> Self
    def className(self, *classes: str) -> Self     # Escape hatch for advanced users
    def onClick(self, handler: Callable) -> Self
    def onChange(self, handler: Callable) -> Self
    def onHover(self, handler: Callable) -> Self
    def onMount(self, handler: Callable) -> Self
    def onUnmount(self, handler: Callable) -> Self
    def add(self, *children: BaseComponent) -> Self
    def render(self, target: str) -> IRNode        # Called by compiler, not user
```

#### App Class Contract

```python
class App:
    name: str = "PyUI App"
    version: str = "1.0.0"
    description: str = ""
    icon: str | None = None
    favicon: str | None = None
    theme: str | dict = "light"
    fonts: list[str] = ["Inter"]
    meta: dict = {}
    plugins: list[Plugin] = []
    
    # Pages are declared as class attributes
    # Any attribute that is a Page instance is auto-registered
```

#### Page Class Contract

```python
class Page:
    title: str
    route: str           # e.g. "/", "/about", "/dashboard"
    layout: str = "default"   # "default", "full-width", "sidebar", "auth"
    meta: dict = {}
    guard: Callable | None = None  # Auth guard — if returns False, redirect
    children: list[BaseComponent] = []
    
    def add(self, *components: BaseComponent) -> Self
    def on_enter(self, handler: Callable) -> Self   # Lifecycle hook
    def on_leave(self, handler: Callable) -> Self
```

### 3.3 Compiler & Renderer Architecture

#### Step 1 — Class Tree Discovery

When a user runs `pyui run` or `pyui build`, the CLI entry point imports the user's `App` subclass and triggers the compiler:

```python
# pyui/compiler/discovery.py
def discover_app(module_path: str) -> type[App]:
    """Import the user's module and find the App subclass."""
    spec = importlib.util.spec_from_file_location("user_app", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, App) and obj is not App:
            return obj
    raise PyUIError("No App subclass found in module.")
```

#### Step 2 — IR Tree Construction

The compiler walks the class tree and builds a target-agnostic Intermediate Representation:

```python
# pyui/compiler/ir.py
@dataclass
class IRNode:
    type: str                         # "button", "grid", "text", etc.
    props: dict                       # All resolved properties
    children: list[IRNode]
    events: dict[str, str]            # event_name -> handler_id
    reactive_bindings: list[str]      # Which reactive vars this node watches
    style_variant: str | None
    theme_tokens: dict

@dataclass 
class IRTree:
    app_meta: dict
    pages: list[IRPage]
    theme: dict
    reactive_vars: dict[str, Any]
    event_handlers: dict[str, Callable]

@dataclass
class IRPage:
    route: str
    title: str
    layout: str
    root: IRNode
```

#### Step 3 — Target Code Generators

Each renderer consumes the `IRTree` and produces output:

**Web Generator** (`pyui/renderers/web/`):
- Converts `IRTree` → HTML templates using Jinja2
- Maps component types to Tailwind CSS classes
- Generates Alpine.js directives for reactivity (`x-data`, `x-model`, `x-show`)
- Serialises reactive state to a JSON bootstrap payload
- Wraps output in a single-page shell (`index.html`)
- Event handlers serialised to a generated `app.js`

**Desktop Generator** (`pyui/renderers/desktop/`):
- Converts `IRTree` → tkinter widget tree (default, no extra install)
- Optional PyQt6 renderer for richer widgets (requires `pip install pyui[qt]`)
- Layout mapped via grid/pack geometry managers
- Custom tkinter widget wrappers with modern styling via `sv-ttk` theme
- Reactive state drives `tkinter.StringVar` / `tkinter.IntVar` bindings

**CLI Generator** (`pyui/renderers/cli/`):
- Converts `IRTree` → Rich `Layout` / `Panel` / `Table` tree
- Interactive widgets use `prompt_toolkit` for keyboard navigation
- Reactive updates trigger `Live` context refresh

### 3.4 State Management System

#### Reactive Variables

```python
# pyui/state/reactive.py

class ReactiveVar(Generic[T]):
    """A reactive variable that notifies subscribers on change."""
    
    def __init__(self, initial: T):
        self._value: T = initial
        self._subscribers: list[Callable] = []
    
    def get(self) -> T:
        return self._value
    
    def set(self, value: T) -> None:
        old = self._value
        self._value = value
        if old != value:
            self._notify()
    
    def _notify(self):
        for sub in self._subscribers:
            sub(self._value)
    
    def subscribe(self, handler: Callable) -> Callable:
        """Returns unsubscribe function."""
        self._subscribers.append(handler)
        return lambda: self._subscribers.remove(handler)
    
    def __add__(self, other): return ReactiveVar(self._value + other)
    def __str__(self): return str(self._value)

def reactive(initial: T) -> ReactiveVar[T]:
    return ReactiveVar(initial)
```

#### State Store (Global)

For cross-page / cross-component shared state:

```python
# pyui/state/store.py
class Store:
    """Global state store for app-wide reactive state."""
    
    def __init__(self):
        self._state: dict[str, ReactiveVar] = {}
    
    def define(self, key: str, initial: Any) -> ReactiveVar:
        var = ReactiveVar(initial)
        self._state[key] = var
        return var
    
    def get(self, key: str) -> ReactiveVar:
        return self._state[key]
    
    def snapshot(self) -> dict:
        return {k: v.get() for k, v in self._state.items()}

store = Store()  # Singleton
```

#### Computed Values

```python
from pyui import reactive, computed

count = reactive(0)
doubled = computed(lambda: count.get() * 2)
# doubled auto-updates when count changes
```

### 3.5 Theme Engine

#### Token System

Themes are defined as flat token dictionaries that map to CSS variables, tkinter style settings, and Rich styles:

```python
# pyui/theme/tokens.py
DEFAULT_TOKENS = {
    # Colors
    "color.primary":       "#6C63FF",
    "color.primary.hover": "#5A52E0",
    "color.secondary":     "#F3F4F6",
    "color.background":    "#FFFFFF",
    "color.surface":       "#F9FAFB",
    "color.text":          "#111827",
    "color.text.muted":    "#6B7280",
    "color.border":        "#E5E7EB",
    "color.success":       "#10B981",
    "color.warning":       "#F59E0B",
    "color.danger":        "#EF4444",
    "color.info":          "#3B82F6",
    
    # Typography
    "font.family":         "Inter, system-ui, sans-serif",
    "font.size.xs":        "12px",
    "font.size.sm":        "14px",
    "font.size.md":        "16px",
    "font.size.lg":        "18px",
    "font.size.xl":        "24px",
    "font.size.2xl":       "32px",
    "font.weight.normal":  "400",
    "font.weight.medium":  "500",
    "font.weight.bold":    "700",
    
    # Spacing (8px base grid)
    "space.1": "4px",  "space.2": "8px",  "space.3": "12px",
    "space.4": "16px", "space.6": "24px", "space.8": "32px",
    "space.12": "48px","space.16": "64px",
    
    # Shape
    "radius.sm":  "4px",
    "radius.md":  "8px",
    "radius.lg":  "12px",
    "radius.xl":  "16px",
    "radius.full":"9999px",
    
    # Shadow
    "shadow.sm": "0 1px 2px rgba(0,0,0,0.05)",
    "shadow.md": "0 4px 6px rgba(0,0,0,0.07)",
    "shadow.lg": "0 10px 15px rgba(0,0,0,0.10)",
    
    # Animation
    "transition.fast":   "100ms ease",
    "transition.normal": "200ms ease",
    "transition.slow":   "300ms ease",
}
```

#### Built-in Themes

Each built-in theme overrides only the tokens it changes — the rest inherit from `DEFAULT_TOKENS`:

| Theme | Primary | Background | Personality |
|---|---|---|---|
| `light` | #6C63FF | #FFFFFF | Clean, modern default |
| `dark` | #7C73FF | #0F172A | Elegant dark mode |
| `ocean` | #0EA5E9 | #F0F9FF | Calm, professional |
| `sunset` | #F97316 | #FFF7ED | Warm, energetic |
| `forest` | #10B981 | #F0FDF4 | Natural, calm |
| `rose` | #F43F5E | #FFF1F2 | Bold, expressive |

### 3.6 Component Marketplace

#### Publishing a Component

```bash
pyui publish                  # Publishes current package to PyUI marketplace
pyui publish --name my-chart  # Explicit name
```

A marketplace component is a standard Python package with a `pyui.json` manifest:

```json
{
  "name": "pyui-charts",
  "version": "1.2.0",
  "pyui_version": ">=1.0.0",
  "components": ["LineChart", "BarChart", "PieChart", "AreaChart"],
  "targets": ["web", "desktop"],
  "author": "Your Name",
  "license": "MIT"
}
```

#### Plugin Registration API

```python
# In the third-party package's __init__.py
from pyui.plugins import PyUIPlugin, register_component

class ChartsPlugin(PyUIPlugin):
    name = "pyui-charts"
    version = "1.2.0"
    
    def on_load(self, app):
        register_component("LineChart", LineChartComponent)
        register_component("BarChart", BarChartComponent)
```

### 3.7 CLI Toolchain

#### Command Structure

```
pyui
├── new <name>           # Scaffold project
│   ├── --template       # blank | dashboard | landing | admin | auth
│   └── --target         # web | desktop | cli | all
├── run                  # Start dev server
│   ├── --target         # web (default) | desktop | cli
│   ├── --port           # default 8000
│   └── --host           # default localhost
├── build                # Production build
│   ├── --target         # web | desktop | cli | all
│   └── --out            # output directory (default: ./dist)
├── publish              # Publish component package
├── doctor               # Check environment
├── lint                 # Lint component definitions
└── info                 # Show project info
```

#### `pyui new` Scaffold Output

```
my-app/
├── app.py               # Main App class
├── pages/
│   ├── home.py
│   └── about.py
├── components/          # Custom components
├── assets/
│   ├── images/
│   └── fonts/
├── pyui.config.py       # Project configuration
├── requirements.txt
└── README.md
```

### 3.8 Hot Reload System

The hot reload system uses `watchdog` to monitor file changes and `websockets` to push updates to connected clients:

```
File Change
    │
    ▼
watchdog FileSystemEventHandler
    │
    ▼
Invalidate IR cache for changed module
    │
    ▼
Re-run compiler for changed page(s) only
    │
    ▼
Diff old IR vs new IR → minimal patch
    │
    ▼
Broadcast patch via WebSocket to browser
    │
    ▼
Browser JS applies DOM patch (no full reload)
```

Target latency: <200ms from file save to UI update.

### 3.9 Plugin System

```python
# pyui/plugins/base.py
class PyUIPlugin:
    name: str
    version: str
    
    def on_load(self, app: App) -> None: ...
    def on_compile_start(self, ir: IRTree) -> None: ...
    def on_compile_end(self, ir: IRTree) -> None: ...
    def on_build(self, output_path: Path) -> None: ...
    def on_dev_start(self, server) -> None: ...
```

Plugins hook into the compiler lifecycle. This enables third-party tools like analytics injectors, SEO plugins, and performance profilers.

### 3.10 Performance Requirements

| Metric | Requirement |
|---|---|
| Cold compile time (50 components) | < 3 seconds |
| Hot reload latency | < 200ms |
| Web output First Contentful Paint | < 1.5s on 3G |
| Web output Lighthouse score | > 90 |
| Desktop startup time | < 2 seconds |
| CLI render time | < 500ms |
| Memory usage (dev server) | < 150MB RAM |
| Built web bundle (gzipped) | < 200KB (excluding user assets) |

### 3.11 Security Requirements

- All user event handler code executes server-side only — no arbitrary Python is sent to the browser
- Web output is static HTML/JS — no server required for deployed apps
- The marketplace package registry scans for malware before listing
- `pyui doctor` checks for known vulnerable dependencies
- CSP headers are included in dev server responses
- No `eval()` or dynamic code execution in generated JS
- Marketplace packages must declare all Python dependencies in `pyui.json`

### 3.12 Accessibility Requirements

- All web-rendered components include correct ARIA roles and labels
- Keyboard navigation works out of the box (tab order, focus management)
- Colour contrast meets WCAG 2.1 AA minimum (4.5:1 for text)
- Screen reader support verified with NVDA (Windows) and VoiceOver (macOS)
- All images require `alt` text — compiler warns if missing
- Focus indicators visible on all interactive elements
- Motion reduced when `prefers-reduced-motion` is set

---

## 4. Development Phases

### Phase 0 — Project Setup & Foundations
**Duration:** 1 week  
**Goal:** Working repository, CI/CD, dev environment, and skeleton package.

#### Tasks

1. **Repository setup**
   - Create GitHub repository with `main` and `dev` branches
   - Branch protection: PRs required for `main`, CI must pass
   - MIT license, CODE_OF_CONDUCT.md, CONTRIBUTING.md

2. **Python package skeleton**
   - `pyproject.toml` with `[build-system]` using `hatchling`
   - Package name: `pyui-framework` (PyPI), import as `pyui`
   - Minimum Python version: 3.10 (for structural pattern matching)
   - Entry point: `pyui = pyui.cli.main:main`

3. **Directory structure** (see Section 6)

4. **CI/CD — GitHub Actions**
   - `test.yml` — runs on every PR: `pytest`, `ruff`, `mypy`
   - `publish.yml` — runs on version tag: builds and pushes to PyPI
   - `docs.yml` — builds and deploys docs to GitHub Pages

5. **Development tooling**
   - `ruff` for linting and formatting
   - `mypy` for type checking (strict mode)
   - `pytest` + `pytest-cov` for tests
   - `pre-commit` hooks: ruff, mypy, trailing whitespace
   - `hatch` for environment management

6. **Core exceptions module**
   ```python
   # pyui/exceptions.py
   class PyUIError(Exception): ...
   class CompilerError(PyUIError): ...
   class ComponentError(PyUIError): ...
   class ThemeError(PyUIError): ...
   class PluginError(PyUIError): ...
   ```

7. **Logging setup**
   - Structured logging via `structlog`
   - Log levels: DEBUG (dev), INFO (default), WARNING, ERROR
   - Pretty console output in dev mode, JSON in production

8. **Version management**
   - Single source of truth: `pyui/__init__.py` `__version__`
   - Semantic versioning: MAJOR.MINOR.PATCH

#### Deliverables
- `pip install -e .` works
- `pyui --help` outputs usage
- All CI checks green on an empty test suite
- Pre-commit hooks installed and passing

---

### Phase 1 — Core Compiler (Web Target)
**Duration:** 3 weeks  
**Goal:** Python App class → valid HTML/CSS/JS output for at least 5 components.

#### Tasks

1. **BaseComponent implementation**
   - Chainable builder pattern
   - Props validation (type hints + runtime checks)
   - Child management (`add()`, `remove()`, `clear()`)
   - Event handler registration

2. **App and Page classes**
   - Class attribute discovery (inspect module)
   - Route registration
   - Page lifecycle hooks

3. **IR Tree construction**
   - `IRNode`, `IRPage`, `IRTree` dataclasses
   - Tree walker that traverses user's class hierarchy
   - Props serialisation (handle callables, lambdas, reactive refs)

4. **Web renderer — HTML generation**
   - Jinja2 templates for each component type
   - Tailwind CSS class mapping (`component_type × variant × size → classes`)
   - Output: single `index.html` per page, plus shared `style.css`

5. **Web renderer — JS generation**
   - Alpine.js for reactivity directives
   - Event handler proxy: Python handlers registered as `fetch()` calls to dev server
   - Generated `app.js` bootstrap

6. **Dev server**
   - `aiohttp` or `uvicorn` based
   - Serves static files from build output
   - HTTP endpoint for event handler invocation
   - WebSocket endpoint for hot reload (stub — wired in Phase 6)

7. **First 5 components:** `Page`, `Button`, `Text`, `Heading`, `Grid`

#### Deliverables
- `pyui run --web` opens a working page in the browser
- Button click triggers Python handler and updates the page
- All 5 components render correctly in Chrome, Firefox, Safari

---

### Phase 2 — Full Component Library
**Duration:** 4 weeks  
**Goal:** All 40+ built-in components implemented and documented.

#### Tasks

1. **Layout components:** `Flex`, `Stack`, `Container`, `Sidebar`, `Split`, `Divider`, `Spacer`
2. **Navigation components:** `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu`
3. **Input components:** `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Toggle`, `Slider`, `DatePicker`, `FilePicker`, `Form`
4. **Display components:** `Badge`, `Tag`, `Avatar`, `Icon`, `Image`, `Video`, `Markdown`
5. **Feedback components:** `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`, `Spinner`, `Skeleton`
6. **Data components:** `Table`, `Chart` (line, bar, pie), `Stat`
7. **Component documentation** — docstring + usage example for every component
8. **Storybook-equivalent** — `pyui storybook` command opens all components in isolation

#### Deliverables
- All 40+ components render correctly on web target
- Component gallery demo app runnable from repo
- Every component has at least one screenshot in docs

---

### Phase 3 — State Management & Reactivity
**Duration:** 2 weeks  
**Goal:** `@reactive` system fully wired from Python to web UI.

#### Tasks

1. **ReactiveVar class** — full implementation with subscribers
2. **Computed values** — `computed(fn)` auto-tracks dependencies
3. **Web reactivity wiring**
   - Reactive vars serialised to Alpine.js `x-data` store on page load
   - State changes from Python handlers push via WebSocket patch to browser
   - Browser-side state changes (form inputs) posted back to Python handler
4. **Store (global state)** — `store.define()`, `store.get()`
5. **Reactive conditional rendering** — `component.hidden(reactive_condition)`
6. **Reactive list rendering** — `List(items=reactive_list).render(lambda item: Card(...))`
7. **State persistence** — optional `persist=True` on `ReactiveVar` for localStorage
8. **Time-travel debugger** — dev-mode state history panel in browser (stretch goal)

#### Deliverables
- Counter demo works: click button → Python state changes → browser updates without reload
- Form input in browser → Python handler receives value → state updates → UI re-renders
- Reactive list renders and updates correctly when list changes

---

### Phase 4 — Desktop & CLI Renderers
**Duration:** 3 weeks  
**Goal:** Same App code runs as desktop window and terminal app.

#### Tasks

**Desktop (tkinter):**
1. tkinter renderer consuming IRTree
2. Component → widget mapping (Button→ttk.Button, Grid→grid manager, etc.)
3. `sv-ttk` theme integration for modern look
4. Event loop management (tkinter mainloop compatibility)
5. Reactive state binding to `tkinter.StringVar` / `BooleanVar`
6. Optional PyQt6 renderer (`pip install pyui[qt]`)

**CLI:**
1. Rich renderer consuming IRTree
2. Layout → Rich `Layout` / `Panel` mapping
3. Table, Chart (ASCII), Stat components
4. `prompt_toolkit` for interactive inputs
5. Reactive state drives `Live` context refresh loop

**Cross-target:**
1. `pyui run --target desktop` and `--target cli` wired in CLI
2. Target capability matrix — components that don't support a target show warning
3. `@web_only`, `@desktop_only`, `@cli_only` decorators for conditional components

#### Deliverables
- Full demo app runs identically on all three targets
- `pyui build --target desktop` produces a standalone executable via `PyInstaller`

---

### Phase 5 — Theme Engine & Marketplace
**Duration:** 2 weeks  
**Goal:** Full theme system live, marketplace protocol defined, 3 first-party plugins published.

#### Tasks

**Theme Engine:**
1. Token system fully implemented
2. All 6 built-in themes
3. Custom theme dict validation and merging
4. Dark mode auto-detection (`prefers-color-scheme`)
5. Theme hot-swap at runtime (`app.set_theme()`)
6. Design token export for Figma (JSON format)

**Marketplace:**
1. `pyui publish` command — packages and uploads to PyPI with `pyui.json` manifest
2. `pyui search <query>` — searches PyPI for `pyui-*` packages
3. Plugin loading system — `App.plugins = [ChartsPlugin()]`
4. First-party plugins: `pyui-charts`, `pyui-auth`, `pyui-admin`

#### Deliverables
- Theme switching works at runtime
- `pip install pyui-charts` + one line in App → chart renders
- 3 first-party plugins published to PyPI

---

### Phase 6 — Developer Tooling & Hot Reload
**Duration:** 2 weeks  
**Goal:** World-class developer experience.

#### Tasks

1. **Hot reload — full implementation**
   - `watchdog` file watcher
   - Incremental IR diffing
   - WebSocket patch broadcast
   - <200ms target

2. **`pyui doctor`** — checks Python version, dependencies, port availability, PyUI version

3. **`pyui lint`** — validates component trees, warns on missing `alt`, inaccessible colour contrast, missing route definitions

4. **Error overlay** — when compiler error occurs in dev mode, browser shows a styled error overlay with file + line number (like Vite's error overlay)

5. **Dev tools panel** — in-browser sidebar (dev mode only):
   - Component tree inspector
   - Reactive state viewer
   - Event log
   - Performance timings

6. **`pyui storybook`** — opens all components in an interactive gallery

7. **VS Code extension** — syntax highlighting for PyUI patterns, component autocomplete, inline docs (stretch goal for this phase)

#### Deliverables
- File save → browser update in <200ms
- Error overlay shows on compiler errors
- Dev tools panel functional

---

### Phase 7 — Production Hardening
**Duration:** 3 weeks  
**Goal:** Production-ready quality: performance, security, accessibility, testing.

#### Tasks

1. **Performance optimisation**
   - CSS purging (remove unused Tailwind classes from build output)
   - JS minification and tree shaking
   - Image optimisation pipeline
   - Lazy loading for off-screen components
   - Lighthouse CI integration (fail build if score drops below 90)

2. **Security audit**
   - Dependency vulnerability scan (`pip-audit`)
   - CSP header verification
   - XSS surface review (user-provided strings sanitised in HTML output)
   - CORS configuration for dev server

3. **Accessibility audit**
   - Automated: `axe-core` in Playwright tests
   - Manual: keyboard nav, screen reader testing

4. **Cross-browser testing**
   - Playwright E2E tests across Chrome, Firefox, Safari, Edge
   - Mobile viewport testing

5. **Load testing**
   - Dev server: 50 concurrent connections
   - Build pipeline: 500-component app in <10s

6. **Error handling hardening**
   - All compiler errors have error codes (PYUI-001, etc.)
   - Helpful error messages with suggested fixes
   - Graceful degradation when components fail

7. **Documentation site**
   - Built with PyUI itself (dogfooding)
   - Getting started, API reference, component gallery, cookbook, migration guide

8. **Example apps** — 5 full example apps in `/examples`:
   - `dashboard` — analytics dashboard
   - `todo` — classic todo app
   - `blog` — content site with routing
   - `ml-demo` — ML model inference UI
   - `admin` — CRUD admin panel

#### Deliverables
- Lighthouse score >90 on all example apps
- Zero known security vulnerabilities
- All WCAG 2.1 AA criteria pass
- Documentation site live

---

### Phase 8 — Public Launch
**Duration:** 1 week  
**Goal:** PyPI v1.0.0 release, community launch.

#### Tasks

1. **Version bump** to 1.0.0, full changelog
2. **PyPI release** — `hatch build && hatch publish`
3. **GitHub release** with release notes and install instructions
4. **Launch content:**
   - README with animated demo GIF
   - Blog post: "Introducing PyUI"
   - Hacker News "Show HN" post
   - Reddit: r/Python, r/programming
   - Twitter/X thread
5. **Discord server** launch
6. **Docs site** — final review, go live
7. **First issue triage** — label `good-first-issue` on 20+ issues for community

#### Deliverables
- `pip install pyui-framework` installs v1.0.0
- 1,000 GitHub stars within first week (stretch)
- Discord server with 200+ members

---

## 5. Unit Test Plan — Per Phase

### Phase 0 — Project Setup Tests

```python
# tests/test_setup.py

def test_package_importable():
    import pyui
    assert pyui.__version__ is not None

def test_version_format():
    import re, pyui
    assert re.match(r"^\d+\.\d+\.\d+", pyui.__version__)

def test_cli_entry_point():
    from pyui.cli.main import main
    assert callable(main)

def test_exceptions_importable():
    from pyui.exceptions import (
        PyUIError, CompilerError, ComponentError, ThemeError, PluginError
    )

def test_pyui_error_is_exception():
    from pyui.exceptions import PyUIError
    assert issubclass(PyUIError, Exception)

def test_compiler_error_inherits_pyui_error():
    from pyui.exceptions import CompilerError, PyUIError
    assert issubclass(CompilerError, PyUIError)
```

---

### Phase 1 — Compiler & Web Renderer Tests

```python
# tests/test_compiler/test_discovery.py

def test_discovers_app_subclass(tmp_path):
    app_file = tmp_path / "app.py"
    app_file.write_text("from pyui import App\nclass MyApp(App): pass\n")
    from pyui.compiler.discovery import discover_app
    cls = discover_app(str(app_file))
    assert cls.__name__ == "MyApp"

def test_raises_if_no_app_subclass(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("x = 1\n")
    from pyui.compiler.discovery import discover_app
    from pyui.exceptions import PyUIError
    with pytest.raises(PyUIError):
        discover_app(str(f))

# tests/test_compiler/test_ir.py

def test_button_produces_ir_node():
    from pyui import Button
    from pyui.compiler.ir import build_ir_node
    btn = Button("Click me").style("primary")
    node = build_ir_node(btn)
    assert node.type == "button"
    assert node.props["label"] == "Click me"
    assert node.style_variant == "primary"

def test_grid_children_in_ir():
    from pyui import Grid, Button, Text
    grid = Grid(cols=3).add(Button("A"), Button("B"), Text("Hello"))
    from pyui.compiler.ir import build_ir_node
    node = build_ir_node(grid)
    assert len(node.children) == 3
    assert node.props["cols"] == 3

def test_event_handler_registered():
    from pyui import Button
    from pyui.compiler.ir import build_ir_node
    handler = lambda: None
    btn = Button("Go").onClick(handler)
    node = build_ir_node(btn)
    assert "click" in node.events

# tests/test_renderers/test_web.py

def test_button_renders_html():
    from pyui import Button
    from pyui.renderers.web import render_component
    btn = Button("Submit").style("primary")
    html = render_component(btn)
    assert "Submit" in html
    assert "<button" in html

def test_heading_renders_correct_tag():
    from pyui import Heading
    from pyui.renderers.web import render_component
    h = Heading("Hello", level=2)
    html = render_component(h)
    assert "<h2" in html
    assert "Hello" in html

def test_grid_renders_children():
    from pyui import Grid, Text
    from pyui.renderers.web import render_component
    grid = Grid(cols=2).add(Text("A"), Text("B"))
    html = render_component(grid)
    assert "A" in html
    assert "B" in html

def test_page_title_in_html():
    from pyui import App, Page
    from pyui.renderers.web import render_page
    class TestApp(App):
        home = Page(title="My Page", route="/")
    html = render_page(TestApp.home)
    assert "My Page" in html
```

---

### Phase 2 — Component Library Tests

```python
# tests/test_components/test_inputs.py

def test_button_chain_returns_self():
    from pyui import Button
    btn = Button("Test")
    assert btn.style("primary") is btn
    assert btn.size("lg") is btn
    assert btn.disabled(True) is btn

def test_input_default_props():
    from pyui import Input
    inp = Input(placeholder="Enter text")
    assert inp.props["placeholder"] == "Enter text"
    assert inp.props.get("required") is False

def test_form_collects_children():
    from pyui import Form, Input, Button
    form = Form().add(Input(name="email"), Button("Submit"))
    assert len(form.children) == 2

def test_select_options():
    from pyui import Select
    sel = Select(options=["Option A", "Option B", "Option C"])
    assert len(sel.props["options"]) == 3

# tests/test_components/test_data.py

def test_table_renders_with_data():
    from pyui import Table
    from pyui.renderers.web import render_component
    tbl = Table(
        columns=["Name", "Age"],
        rows=[["Alice", 30], ["Bob", 25]]
    )
    html = render_component(tbl)
    assert "Alice" in html
    assert "Age" in html
    assert "<table" in html

def test_stat_component_props():
    from pyui import Stat
    s = Stat(label="Revenue", value="$12,000", change="+12%", trend="up")
    assert s.props["label"] == "Revenue"
    assert s.props["trend"] == "up"
```

---

### Phase 3 — State Management Tests

```python
# tests/test_state/test_reactive.py

def test_reactive_initial_value():
    from pyui.state.reactive import reactive
    count = reactive(0)
    assert count.get() == 0

def test_reactive_set_updates_value():
    from pyui.state.reactive import reactive
    count = reactive(0)
    count.set(5)
    assert count.get() == 5

def test_reactive_notifies_subscriber():
    from pyui.state.reactive import reactive
    count = reactive(0)
    received = []
    count.subscribe(lambda v: received.append(v))
    count.set(42)
    assert received == [42]

def test_reactive_multiple_subscribers():
    from pyui.state.reactive import reactive
    x = reactive("a")
    log = []
    x.subscribe(lambda v: log.append(f"sub1:{v}"))
    x.subscribe(lambda v: log.append(f"sub2:{v}"))
    x.set("b")
    assert "sub1:b" in log
    assert "sub2:b" in log

def test_reactive_no_notify_if_value_unchanged():
    from pyui.state.reactive import reactive
    x = reactive(10)
    calls = []
    x.subscribe(lambda v: calls.append(v))
    x.set(10)  # Same value
    assert calls == []

def test_reactive_unsubscribe():
    from pyui.state.reactive import reactive
    x = reactive(0)
    calls = []
    unsub = x.subscribe(lambda v: calls.append(v))
    x.set(1)
    unsub()
    x.set(2)
    assert calls == [1]  # Not [1, 2]

# tests/test_state/test_computed.py

def test_computed_updates_with_dependency():
    from pyui.state.reactive import reactive
    from pyui.state.computed import computed
    count = reactive(3)
    doubled = computed(lambda: count.get() * 2)
    assert doubled.get() == 6
    count.set(5)
    assert doubled.get() == 10

# tests/test_state/test_store.py

def test_store_define_and_get():
    from pyui.state.store import Store
    store = Store()
    var = store.define("username", "Alice")
    assert store.get("username").get() == "Alice"

def test_store_snapshot():
    from pyui.state.store import Store
    store = Store()
    store.define("a", 1)
    store.define("b", "hello")
    snap = store.snapshot()
    assert snap == {"a": 1, "b": "hello"}
```

---

### Phase 4 — Desktop & CLI Renderer Tests

```python
# tests/test_renderers/test_desktop.py
# (headless tests using tkinter without display — mock the mainloop)

def test_desktop_renderer_builds_widget_tree():
    from unittest.mock import patch, MagicMock
    with patch("tkinter.Tk") as mock_tk:
        mock_tk.return_value = MagicMock()
        from pyui import Button, Page
        from pyui.renderers.desktop import build_widget_tree
        from pyui.compiler.ir import build_ir_node
        page = Page(title="Test", route="/")
        page.add(Button("Click"))
        ir = build_ir_node(page)
        tree = build_widget_tree(ir, parent=mock_tk())
        assert tree is not None

def test_desktop_renderer_maps_button():
    from pyui.renderers.desktop.mapping import get_widget_class
    assert get_widget_class("button") is not None

# tests/test_renderers/test_cli.py

def test_cli_renderer_produces_renderable():
    from pyui import Button, Page
    from pyui.compiler.ir import build_ir_node
    from pyui.renderers.cli import render_to_rich
    page = Page(title="Test", route="/")
    page.add(Button("Go"))
    ir = build_ir_node(page)
    renderable = render_to_rich(ir)
    assert renderable is not None

def test_cli_text_renders():
    from pyui import Text
    from pyui.renderers.cli import render_component_cli
    t = Text("Hello World")
    result = render_component_cli(t)
    assert "Hello World" in str(result)
```

---

### Phase 5 — Theme Engine Tests

```python
# tests/test_theme/test_tokens.py

def test_default_tokens_complete():
    from pyui.theme.tokens import DEFAULT_TOKENS
    required = ["color.primary", "color.background", "font.family",
                "space.4", "radius.md", "shadow.sm"]
    for key in required:
        assert key in DEFAULT_TOKENS, f"Missing token: {key}"

def test_theme_merges_with_defaults():
    from pyui.theme.engine import build_theme
    custom = {"color.primary": "#FF0000"}
    theme = build_theme(custom)
    assert theme["color.primary"] == "#FF0000"
    assert "color.background" in theme  # Inherited from defaults

def test_dark_theme_has_dark_background():
    from pyui.theme.engine import build_theme, BUILT_IN_THEMES
    theme = build_theme(BUILT_IN_THEMES["dark"])
    bg = theme["color.background"]
    # Dark background should be a dark hex
    r = int(bg[1:3], 16)
    assert r < 50  # Very dark

def test_invalid_theme_name_raises():
    from pyui.theme.engine import build_theme
    from pyui.exceptions import ThemeError
    with pytest.raises(ThemeError):
        build_theme("nonexistent-theme-xyz")

def test_css_variables_generated():
    from pyui.theme.engine import build_theme, tokens_to_css_vars
    theme = build_theme("light")
    css = tokens_to_css_vars(theme)
    assert "--color-primary" in css
    assert "--font-family" in css
    assert ":root" in css
```

---

### Phase 6 — Hot Reload Tests

```python
# tests/test_hotreload/test_watcher.py

def test_file_change_triggers_callback(tmp_path):
    import time
    from pyui.hotreload.watcher import FileWatcher
    
    f = tmp_path / "app.py"
    f.write_text("# version 1")
    
    called = []
    watcher = FileWatcher(str(tmp_path), on_change=lambda p: called.append(p))
    watcher.start()
    time.sleep(0.1)
    f.write_text("# version 2")
    time.sleep(0.5)
    watcher.stop()
    
    assert len(called) > 0

# tests/test_hotreload/test_ir_diff.py

def test_ir_diff_detects_text_change():
    from pyui.compiler.ir import IRNode
    from pyui.hotreload.diff import diff_ir
    
    old = IRNode(type="text", props={"content": "Hello"}, children=[], events={},
                 reactive_bindings=[], style_variant=None, theme_tokens={})
    new = IRNode(type="text", props={"content": "World"}, children=[], events={},
                 reactive_bindings=[], style_variant=None, theme_tokens={})
    
    patch = diff_ir(old, new)
    assert len(patch) == 1
    assert patch[0]["op"] == "update_prop"
    assert patch[0]["key"] == "content"
    assert patch[0]["value"] == "World"

def test_ir_diff_no_changes_empty_patch():
    from pyui.compiler.ir import IRNode
    from pyui.hotreload.diff import diff_ir
    
    node = IRNode(type="button", props={"label": "OK"}, children=[], events={},
                  reactive_bindings=[], style_variant="primary", theme_tokens={})
    patch = diff_ir(node, node)
    assert patch == []
```

---

### Phase 7 — Integration & E2E Tests

```python
# tests/integration/test_full_pipeline.py

def test_full_web_compile_pipeline(tmp_path):
    """End-to-end: App class → HTML file on disk."""
    from pyui import App, Page, Button, Text
    from pyui.compiler import compile_app
    
    class MyApp(App):
        home = Page(title="Test", route="/")
        home.add(
            Text("Welcome"),
            Button("Go").style("primary")
        )
    
    output_dir = tmp_path / "dist"
    compile_app(MyApp, target="web", output_dir=str(output_dir))
    
    index = output_dir / "index.html"
    assert index.exists()
    content = index.read_text()
    assert "Welcome" in content
    assert "Go" in content
    assert "Test" in content

# tests/e2e/test_browser.py  (requires playwright)

@pytest.mark.e2e
def test_button_click_updates_ui(live_server, page):
    """Playwright test: click button → reactive state → UI updates."""
    page.goto(live_server.url)
    
    counter_text = page.locator("[data-testid='counter']")
    assert counter_text.inner_text() == "Count: 0"
    
    page.locator("button", has_text="Increment").click()
    page.wait_for_selector("[data-testid='counter']:has-text('Count: 1')")
    assert counter_text.inner_text() == "Count: 1"

@pytest.mark.e2e
def test_hot_reload_updates_browser(live_server, page, app_file):
    """Playwright test: file change → UI updates without full reload."""
    page.goto(live_server.url)
    initial_title = page.title()
    
    app_file.write_text(app_file.read_text().replace("Old Title", "New Title"))
    page.wait_for_function("document.title === 'New Title'", timeout=3000)
    
    assert page.title() == "New Title"

# tests/e2e/test_accessibility.py  (requires playwright + axe-core)

@pytest.mark.e2e
def test_no_accessibility_violations(live_server, page):
    from axe_playwright_python import Axe
    page.goto(live_server.url)
    axe = Axe()
    results = axe.run(page)
    violations = results["violations"]
    assert violations == [], f"Accessibility violations: {violations}"
```

---

### Continuous Test Metrics Target

| Phase | Min Coverage | Critical Paths |
|---|---|---|
| 0 | 70% | Package import, CLI entry |
| 1 | 75% | Compiler, IR builder, HTML renderer |
| 2 | 80% | All component props and render output |
| 3 | 85% | Reactive subscribe/set/unsubscribe, computed |
| 4 | 80% | Desktop widget mapping, CLI renderable |
| 5 | 85% | Token merging, CSS var generation |
| 6 | 80% | File watcher, IR diff |
| 7 | 90% | Full pipeline, E2E browser tests |

---

## 6. File & Folder Structure

```
pyui/
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── publish.yml
│       └── docs.yml
├── src/
│   └── pyui/
│       ├── __init__.py              # Public API exports + __version__
│       ├── exceptions.py
│       ├── app.py                   # App base class
│       ├── page.py                  # Page class
│       ├── components/
│       │   ├── __init__.py
│       │   ├── base.py              # BaseComponent
│       │   ├── layout/
│       │   │   ├── grid.py, flex.py, stack.py, container.py ...
│       │   ├── navigation/
│       │   │   ├── nav.py, tabs.py, breadcrumb.py ...
│       │   ├── input/
│       │   │   ├── button.py, input.py, form.py, select.py ...
│       │   ├── display/
│       │   │   ├── text.py, heading.py, image.py, badge.py ...
│       │   ├── feedback/
│       │   │   ├── alert.py, modal.py, toast.py, tooltip.py ...
│       │   └── data/
│       │       ├── table.py, chart.py, stat.py ...
│       ├── compiler/
│       │   ├── __init__.py
│       │   ├── discovery.py         # App class discovery
│       │   ├── ir.py                # IRNode, IRPage, IRTree
│       │   ├── walker.py            # Tree walker
│       │   └── validator.py         # Pre-compile validation
│       ├── renderers/
│       │   ├── __init__.py
│       │   ├── web/
│       │   │   ├── __init__.py
│       │   │   ├── generator.py     # HTML/JS generation
│       │   │   ├── templates/       # Jinja2 templates
│       │   │   └── tailwind.py      # Class mapping
│       │   ├── desktop/
│       │   │   ├── __init__.py
│       │   │   ├── tkinter_renderer.py
│       │   │   └── qt_renderer.py   # Optional PyQt6
│       │   └── cli/
│       │       ├── __init__.py
│       │       └── rich_renderer.py
│       ├── state/
│       │   ├── reactive.py
│       │   ├── computed.py
│       │   └── store.py
│       ├── theme/
│       │   ├── tokens.py
│       │   ├── engine.py
│       │   └── built_in/
│       │       ├── light.py, dark.py, ocean.py ...
│       ├── server/
│       │   ├── dev_server.py        # aiohttp dev server
│       │   └── websocket.py         # Hot reload WS
│       ├── hotreload/
│       │   ├── watcher.py
│       │   └── diff.py
│       ├── plugins/
│       │   ├── base.py              # PyUIPlugin base class
│       │   ├── registry.py
│       │   └── loader.py
│       ├── cli/
│       │   ├── main.py              # Click CLI entry point
│       │   ├── commands/
│       │   │   ├── new.py, run.py, build.py, publish.py, doctor.py, lint.py
│       │   └── templates/           # pyui new templates
│       │       ├── blank/, dashboard/, landing/, admin/, auth/
│       └── utils/
│           ├── color.py
│           ├── validators.py
│           └── logging.py
├── tests/
│   ├── conftest.py
│   ├── test_setup.py
│   ├── test_compiler/
│   ├── test_components/
│   ├── test_state/
│   ├── test_renderers/
│   ├── test_theme/
│   ├── test_hotreload/
│   ├── integration/
│   └── e2e/
├── examples/
│   ├── dashboard/
│   ├── todo/
│   ├── blog/
│   ├── ml-demo/
│   └── admin/
└── docs/
    ├── index.md
    ├── getting-started.md
    ├── api-reference/
    ├── components/
    ├── cookbook/
    └── migration/
```

---

## 7. Dependencies & Third-Party Libraries

### Core Runtime Dependencies

| Package | Version | Purpose |
|---|---|---|
| `click` | >=8.1 | CLI framework |
| `jinja2` | >=3.1 | HTML template rendering |
| `aiohttp` | >=3.9 | Dev server + WebSocket |
| `watchdog` | >=3.0 | File system watcher |
| `rich` | >=13.0 | CLI renderer + console output |
| `structlog` | >=24.0 | Structured logging |
| `typing-extensions` | >=4.9 | Python <3.11 type backports |

### Optional Runtime Dependencies

| Package | Extras Key | Purpose |
|---|---|---|
| `PyQt6` | `pyui[qt]` | Rich desktop renderer |
| `sv-ttk` | bundled | Modern tkinter theme |
| `prompt-toolkit` | bundled | CLI interactive input |
| `Pillow` | `pyui[images]` | Image optimisation |
| `playwright` | `pyui[e2e]` | E2E testing |

### Development Dependencies

| Package | Purpose |
|---|---|
| `pytest` + `pytest-cov` | Testing + coverage |
| `pytest-asyncio` | Async test support |
| `ruff` | Linting + formatting |
| `mypy` | Static type checking |
| `pre-commit` | Git hooks |
| `hatch` | Build + env management |
| `sphinx` | Documentation |

### Web Output Dependencies (bundled, not installed)

| Library | Version | Purpose |
|---|---|---|
| Tailwind CSS | 3.x | Utility CSS (CDN in dev, purged in build) |
| Alpine.js | 3.x | Lightweight reactivity |
| Chart.js | 4.x | Charts component |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Desktop renderer inconsistency across OS | High | Medium | Automated CI on Windows, macOS, Linux; screenshot comparison tests |
| Tailwind CSS breaking changes | Low | High | Pin Tailwind version; abstract CSS layer between IR and output |
| Python 3.10/3.11/3.12 compatibility breaks | Medium | High | CI matrix tests all supported versions |
| Component API churn breaking user code | Medium | High | Strict semver; deprecation warnings 2 minor versions before removal |
| PyPI namespace squatting (`pyui`) | High | High | Register package early in Phase 0, even as 0.1.0 placeholder |
| Hot reload causing state corruption | Medium | Medium | IR diff validation; state snapshot/restore on failed reload |
| Third-party plugins with malicious code | Medium | High | Marketplace terms of service; `pip-audit` in `pyui doctor` |
| Performance degradation on large apps | Medium | High | Benchmark CI; incremental compilation; lazy IR evaluation |
| Maintainer burnout (solo/small team) | Medium | High | Clear contribution guide; automate release process; community governance |

---

## 9. Glossary

| Term | Definition |
|---|---|
| **App** | The root Python class the user subclasses to define their application |
| **Page** | A routable screen within an App; maps to a URL in web output |
| **Component** | A reusable UI building block (Button, Grid, Chart, etc.) |
| **IR** | Intermediate Representation — a target-agnostic tree of `IRNode` objects produced by the compiler |
| **Renderer** | A backend that consumes the IR and produces output for a specific target (web, desktop, CLI) |
| **Reactive** | A variable that automatically notifies dependent UI components when its value changes |
| **Store** | A global singleton holding app-wide reactive state |
| **Theme** | A set of design tokens (colours, fonts, spacing, radius) that style the entire application |
| **Token** | An atomic named design value, e.g. `color.primary = #6C63FF` |
| **Plugin** | A third-party extension that integrates with the PyUI compiler lifecycle |
| **Hot Reload** | Instant UI update in the browser/window when source files change, without a full restart |
| **Target** | The output platform — `web`, `desktop`, or `cli` |
| **Marketplace** | The ecosystem of community-published PyUI component packages on PyPI |
| **Guard** | An optional async function on a Page that runs before navigation; can redirect if auth fails |
| **Computed** | A reactive value derived from other reactive values; auto-updates when dependencies change |
| **IR Diff** | The process of comparing two IR trees to produce a minimal set of DOM patch operations |

---

*PyUI PRD + TRD v1.0.0 — This document is a living specification. Update version and changelog on every significant change.*

---

## Phase 3.5 — Stabilization & Foundation Hardening

**Status:** 🚧 In Progress  
**Goal:** Make every existing feature production-reliable before adding new targets. No new features — only correctness, consistency, test coverage, and developer experience.

This phase exists because Phases 0–3 moved fast. The foundation is solid but has rough edges: inconsistent styling tokens, missing test coverage on renderers, a broken `__all__` export, storybook layout issues, and no formal contract for what "production-ready" means for each component. Phase 3.5 closes all of that before Phase 4 begins.

---

### 3.5.1 — Full Audit Results (April 2026)

The following issues were identified during the Phase 3.5 audit:

#### Critical Bugs Fixed
| # | Issue | File | Fix |
|---|---|---|---|
| 1 | `__all__` contained comment strings (`"# Layout"`) causing `from pyui import *` to crash with `AttributeError` | `src/pyui/__init__.py` | Replaced string comments with real Python comments |
| 2 | `Tabs.add_tab()` stored raw `BaseComponent` children; renderer called `_render_node()` on them directly, crashing with `AttributeError: 'Text' object has no attribute 'type'` | `src/pyui/renderers/web/generator.py` | Added `isinstance(child, IRNode)` guard — converts `BaseComponent` to `IRNode` before rendering |
| 3 | Shimmer keyframe only had `100%` stop — animation never played | `src/pyui/renderers/web/generator.py` | Fixed to `0% → 100%` |
| 4 | Radio input used hardcoded `text-violet-600` / `focus:ring-violet-500` — inconsistent with new design system | `src/pyui/renderers/web/generator.py` | Updated to `text-gray-900` / `focus:ring-gray-900/20` |
| 5 | Form title used `text-lg font-medium` — inconsistent with design system | `src/pyui/renderers/web/generator.py` | Updated to `text-base font-semibold tracking-tight` |
| 6 | Alert icon used `mr-3` margin — inconsistent with gap-based layout | `src/pyui/renderers/web/generator.py` | Replaced with `alert-icon` class, gap handled by parent flex |

#### Design System Issues Fixed
| # | Issue | Fix |
|---|---|---|
| 7 | Button primary used `bg-violet-600` — not aligned with premium design direction | Redesigned to `bg-gray-950` with `active:scale-[0.97]` |
| 8 | All inputs used `rounded-md` — inconsistent with card `rounded-2xl` | Updated to `rounded-xl` across all inputs |
| 9 | `full-width` page layout had `px-4 py-8` padding — broke full-bleed designs | Removed padding, now `w-full` only |
| 10 | Container missing `6xl` size for wide layouts | Added `max-w-[1400px]` as `6xl` |
| 11 | Skeleton used `animate-pulse` — generic, not premium | Replaced with shimmer animation via `before:` pseudo-element |
| 12 | Progress bar used flat `bg-violet-600` | Replaced with `bg-gradient-to-r from-gray-700 to-gray-900` |

#### Storybook Issues Fixed
| # | Issue | Fix |
|---|---|---|
| 13 | Sidebar had `min-h-screen` but no `h-screen sticky` — didn't stay fixed while scrolling | Changed to `h-screen sticky top-0 overflow-y-auto self-start` |
| 14 | Main content had no max-width — stretched to full viewport on wide screens | Added `max-w-5xl` cap on content area |
| 15 | Sidebar nav items had `px-5` — too much padding for 220px sidebar | Reduced to `px-4` |
| 16 | No active state on sidebar links while scrolling | Added GSAP + IntersectionObserver scroll-spy with `.sb-active` CSS class |
| 17 | Spinner section showed spinners but they appeared static | Fixed by showing all 5 sizes explicitly with `Spinner(size=...)` |

---

### 3.5.2 — Remaining Stabilization Tasks

These tasks must be completed before Phase 4 begins. Each has a clear acceptance criterion.

#### T1 — Test Coverage: Renderer
**Priority:** High  
**Status:** Pending

The renderer has 0 tests for most components. Add a test for every `_render_*` function.

Acceptance criteria:
- Every component in the dispatch table has at least one render test
- Tests verify: HTML is non-empty, key attributes are present, no exceptions thrown
- Coverage on `generator.py` reaches ≥ 80%

```python
# Example test pattern
def test_render_alert_info():
    from pyui import Alert
    from pyui.renderers.web import render_component
    html = render_component(Alert("Title", "Body", variant="info"))
    assert "role=\"alert\"" in html
    assert "Title" in html
    assert "border-l-sky-500" in html

def test_render_spinner_sizes():
    from pyui import Spinner
    from pyui.renderers.web import render_component
    for size in ["xs", "sm", "md", "lg", "xl"]:
        html = render_component(Spinner(size=size))
        assert "animate-spin" in html
        assert f"h-" in html
```

#### T2 — Test Coverage: State System
**Priority:** High  
**Status:** Pending

The state system (`reactive`, `computed`, `store`) has minimal tests. Add edge case coverage.

Acceptance criteria:
- `ReactiveVar` arithmetic operators tested
- `ComputedVar` dependency re-tracking tested (conditional deps)
- `Store` duplicate key error tested
- `persist=True` flag tested (IR includes var in `persistent_vars`)
- Thread-safety note documented (not thread-safe — single-user dev server only)

#### T3 — Test Coverage: Compiler IR
**Priority:** Medium  
**Status:** Partial (discovery + basic IR tests exist)

Acceptance criteria:
- `build_ir_node` tested for every component type
- Reactive lambda resolution tested
- `ReactiveVar` direct prop binding tested
- Event handler registration and retrieval tested
- `build_ir_tree` tested with multi-page App

#### T4 — Component API Consistency Audit
**Priority:** High  
**Status:** Pending

Every component must follow the same API contract. Current inconsistencies:

| Component | Issue | Fix |
|---|---|---|
| `Spinner` | Constructor param is `size` but prop stored as `spinner_size` — confusing | Document clearly, add `size()` chainable method |
| `Avatar` | `src()` and `name()` methods shadow constructor params | Rename chainable methods to `set_src()` / `set_name()` or remove duplicates |
| `Chart` | `line()`, `bar()`, `pie()` methods exist but constructor also takes `type=` | Remove redundant methods, keep constructor param only |
| `Skeleton` | No constructor param for `variant` — must use `Skeleton(variant="circle")` but `variant` is not in `__init__` signature | Add `variant` to `__init__` signature |
| `Badge` | Constructor takes `variant` as second positional arg — inconsistent with other components that use `.style()` | Keep for now, document as intentional shorthand |
| `Form` | `title` is a constructor param but `Form` is also a context manager — title renders as `h3` inside the form | Consistent, document it |

#### T5 — `pyui new` Command Implementation
**Priority:** Medium  
**Status:** Stub only

The `pyui new <name>` command currently prints a placeholder message. Implement the minimal scaffold.

Acceptance criteria:
- Creates a directory with `app.py`, `requirements.txt`, `README.md`
- `app.py` contains a working `App` + `Page` + `Button` example
- `pyui run` works immediately after `pyui new`
- `--template blank` (default) works
- `--template dashboard` creates a 3-page app with Nav, Stats, Table

#### T6 — Hot Reload WebSocket (Partial)
**Priority:** Medium  
**Status:** Stub (WebSocket connects but sends only `{"type": "connected"}`)

Implement file-watching hot reload for the web target.

Acceptance criteria:
- `watchdog` monitors the user's app file for changes
- On change: re-runs `build_ir_tree`, diffs against previous IR
- Sends `{"type": "reload"}` via WebSocket to connected browsers
- Browser JS receives message and calls `window.location.reload()`
- Full DOM-patch diffing is Phase 6 — simple full reload is acceptable here

#### T7 — Storybook: Production-Quality Redesign
**Priority:** High  
**Status:** In Progress

The storybook must be the definitive showcase of PyUI's quality. It is the first thing a new user sees.

Acceptance criteria:
- Every component is shown with all its variants and states
- Preview cards have consistent label bars with variant hints
- Sidebar scroll-spy works correctly (active link highlighted as you scroll)
- GSAP entrance animations fire on scroll for all preview cards
- Spinner, Progress, and Skeleton all visually work correctly
- No raw HTML (`RawHTML`, `inject_html`) used anywhere in storybook
- Renders in < 500ms
- No layout overflow or spacing issues at 1280px, 1440px, 1920px viewport widths

#### T8 — `pyui doctor` Enhancements
**Priority:** Low  
**Status:** Partial

Current `pyui doctor` only checks Python version. Extend it.

Acceptance criteria:
- Checks Python >= 3.10
- Checks all required dependencies are installed and at correct versions
- Checks port 8000 is available
- Checks `watchdog` is installed (needed for hot reload)
- Reports PyUI version and latest available version from PyPI

#### T9 — AGENT_CONTEXT.md Sync
**Priority:** Low  
**Status:** Pending

`AGENT_CONTEXT.md` must reflect all Phase 3.5 changes.

Acceptance criteria:
- Phase 3.5 section added with all bug fixes documented
- Known gaps section updated
- Component API inconsistencies documented

---

### 3.5.3 — Definition of Done for Phase 3.5

Phase 3.5 is complete when ALL of the following are true:

- [ ] All 9 tasks above are marked complete
- [ ] `python -m pytest tests/ -q` shows **0 failures**
- [ ] `ruff check src/` shows **0 errors**
- [ ] `mypy src/` shows **0 errors** (strict mode)
- [ ] `from pyui import *` works without any `AttributeError`
- [ ] `pyui storybook` renders without errors and looks premium
- [ ] `pyui run app.py` works on a fresh `pip install -e .`
- [ ] `pyui new my-app && cd my-app && pyui run` works end-to-end
- [ ] Every component in `__all__` renders without exception
- [ ] Renderer test coverage ≥ 80%
- [ ] No `RawHTML` or `inject_html` in storybook or any example file
- [ ] `AGENT_CONTEXT.md` is up to date

---

### 3.5.4 — What Phase 3.5 Does NOT Include

To keep scope tight, the following are explicitly deferred to Phase 4+:

- Desktop renderer (Phase 4)
- CLI/TUI renderer (Phase 4)
- Hot reload DOM diffing (Phase 6)
- Component marketplace (Phase 5)
- `pyui build` static export improvements (Phase 6)
- i18n / accessibility audit (Phase 7)
- Performance profiling (Phase 7)

---

### 3.5.5 — Phase 3.5 Progress Tracker

| Task | Owner | Status | Notes |
|---|---|---|---|
| T1 — Renderer test coverage | — | 🔴 Not started | Priority: start here |
| T2 — State system tests | — | 🟡 Partial | Basic tests exist |
| T3 — Compiler IR tests | — | 🟡 Partial | discovery + basic IR done |
| T4 — Component API audit | — | 🟡 In progress | Issues documented above |
| T5 — `pyui new` implementation | — | 🔴 Not started | |
| T6 — Hot reload WebSocket | — | 🔴 Not started | Simple reload only |
| T7 — Storybook redesign | — | 🟡 In progress | Layout fixed, needs polish |
| T8 — `pyui doctor` enhancements | — | 🔴 Not started | Low priority |
| T9 — AGENT_CONTEXT.md sync | — | 🔴 Not started | Do last |

**Legend:** 🔴 Not started · 🟡 In progress · 🟢 Complete

---

### 3.5.6 — Entry Criteria for Phase 4

Phase 4 (Desktop + CLI Renderers) begins only when:

1. All Phase 3.5 tasks are 🟢 Complete
2. The storybook passes the Definition of Done above
3. A clean `pip install pyui-framework` + `pyui storybook` works on a fresh machine
4. The IR tree is confirmed stable — no breaking changes to `IRNode`, `IRPage`, `IRTree` dataclasses
5. At least one team member has done a full end-to-end test: `pyui new` → `pyui run` → `pyui build`

---
