---
inclusion: always
---

# Zolt — AI Agent Context

Zolt is a production-ready Python UI framework. Install: `pip install zolt`. CLI: `zolt`.

## Core concept

Write your entire UI in pure Python. One codebase compiles to three targets:
- **Web** — HTML + Tailwind CSS (CDN) + Alpine.js (dev server with hot reload)
- **Desktop** — native tkinter window
- **CLI** — Rich TUI in the terminal

## Package structure

```
src/pyui/          ← import name is pyui (from pyui import App)
├── app.py         ← App base class + AppMeta metaclass
│                     App.extra_css (str), App.head_scripts (list[str]) — v1.2
├── page.py        ← Page class
├── exceptions.py  ← PyUIError hierarchy with PYUI-NNN error codes
├── linter.py      ← lint_app()
├── scaffold.py    ← create_project() for zolt new + zolt templates
├── components/    ← 47+ components (layout, display, input, feedback, nav, data, media)
│   ├── base.py    ← BaseComponent.inlineStyle(css) added v1.2
│   ├── layout/    ← Flex, Grid, Stack, Container, Section*, Sidebar, Split, Divider, Spacer, List
│   ├── display/   ← Text, Heading, BlurHeading*, Badge, Tag, Avatar, Icon, Image, Link*, Markdown, RawHTML
│   ├── input/     ← Button, Input, Textarea, Select, Checkbox, Radio, Toggle, Slider, DatePicker, FilePicker, Form
│   ├── feedback/  ← Alert, Toast, Modal, Drawer, Tooltip, Progress, Spinner, Skeleton
│   ├── navigation/← Nav, FloatingNav*, Tabs, Breadcrumb, Pagination, Menu
│   ├── data/      ← Table, Stat, Chart
│   └── media/     ← Video, VideoBg*
│   (* = new in v1.2)
├── compiler/      ← IR pipeline: build_ir_node → build_ir_page → build_ir_tree
├── renderers/     ← web/, desktop/, cli/
├── server/        ← aiohttp dev server with hot reload + WebSocket
├── state/         ← reactive.py, computed.py, store.py
├── theme/         ← engine.py (build_theme, tokens_to_css_vars, tokens_to_figma)
├── plugins/       ← PyUIPlugin base, registry, loader
├── hotreload/     ← FileWatcher, diff_ir
└── cli/           ← main.py (zolt command), storybook.py
```

## Minimal app

```python
from pyui import App, Button, Flex, Heading, Page, Text, reactive

_count = reactive(0)

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self):
        with Flex(direction="col", align="center", gap=6):
            Heading("Hello from Zolt", level=1)
            Text(lambda: f"Count: {_count.get()}").style("muted")
            Button("+").style("primary").onClick(lambda: _count.set(_count.get() + 1))

class MyApp(App):
    name = "My App"
    count = _count
    home = HomePage()
```

Run: `zolt run app.py`

## CRITICAL: Page registration rule

Pages MUST be declared as class attributes inside the App class body.
`AppMeta` metaclass scans at class definition time — post-assignment does NOT work.

```python
# ✅ CORRECT
class MyApp(App):
    home = HomePage()   # registered at class creation

# ❌ WRONG — causes 404
class MyApp(App):
    home = None
MyApp.home = HomePage()  # too late, AppMeta already ran
```

## Reactive state pattern

Always define reactive vars at module level, then reference them in the App class:

```python
_count = reactive(0)          # module level

class MyApp(App):
    count = _count             # reference in App for IR registration
    home = CounterPage()
```

## Component API

All components use fluent chaining. Every method returns `self`:

```python
Button("Save").style("primary").size("lg").disabled(False).onClick(handler)
Text("Hello").style("muted").paragraph()
Grid(cols=3, gap=6).add(Card(...), Card(...), Card(...))
Flex(direction="col").className("my-class").inlineStyle("z-index:10;")
```

Style variants: `primary`, `secondary`, `ghost`, `danger`, `success`, `gradient`, `link`
Sizes: `xs`, `sm`, `md`, `lg`, `xl`

## New in v1.2 — key components

```python
# BlurHeading — word-by-word blur-reveal, Instrument Serif italic, fluid sizing
BlurHeading("The Website Your Brand Deserves", level=1, delay_ms=100)

# Link — semantic <a> with style variants
Link("Get Started", href="#").style("glass").icon("arrow-up-right")
Link("Privacy", href="/privacy").style("footer")

# Section — <section> with position:relative for video-background layouts
with Section(min_height=560, bg="#000"):
    VideoBg(src="https://stream.mux.com/...", hls=True, fade_height=160)
    Flex(...).inlineStyle("position:absolute;inset:0;z-index:10;")

# VideoBg — absolutely-positioned background video with HLS support
VideoBg(src=MUX_URL, hls=True, desaturate=True, fade_height=160)

# FloatingNav — fixed glassmorphism pill navigation bar
FloatingNav(
    logo_src="/images/logo.png",
    links=["Home", "Services", "Work"],
    cta_text="Get Started",
)

# inlineStyle() — raw CSS on any component (clamp, text-shadow, z-index)
Flex(direction="col").inlineStyle("padding-top:clamp(6rem,14vh,10rem);")
```

## App class — full attributes

```python
class MyApp(App):
    name = "My App"
    theme = "dark"                    # light|dark|ocean|sunset|forest|rose or dict
    extra_css = "/* custom CSS */"    # injected into <style> block
    head_scripts = ["https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"]
    favicon = "/images/favicon.ico"
    plugins = [MyPlugin()]
    home = HomePage()
```

## Declarative composition (preferred)

```python
class MyPage(Page):
    def compose(self):
        with Flex(direction="col", gap=6):
            Heading("Title")          # auto-added to Flex
            with Grid(cols=2):
                Text("A")             # auto-added to Grid
                Text("B")
```

## Adding a new component — checklist

1. Create file in `src/pyui/components/<category>/`
2. Inherit from `BaseComponent`, set `component_type = "my_type"`
3. Export from category `__init__.py`
4. Export from `src/pyui/__init__.py` (import + `__all__`)
5. Add `"my_type": _render_my_type` to dispatch dict in `renderers/web/generator.py`
6. Add `_render_my_type(node: IRNode) -> str` in `generator.py`
   - **Do NOT read `class_name` manually** — post-processor injects it automatically
   - Use `node.props.get("inline_style", "")` only if you need to merge into a style attr
7. Add widget builder in `renderers/desktop/tkinter_renderer.py`
8. Add renderer in `renderers/cli/generator.py`

## class_name post-processor (CRITICAL)

After every `_render_*` returns HTML, the post-processor runs:
```python
custom_class = node.props.get("class_name", "").strip()
if custom_class and ' class="' in html:
    html = html.replace(' class="', f' class="{custom_class} ', 1)
```
**Never manually include `class_name` in renderer output — it will be doubled.**

## Theme system

```python
class MyApp(App):
    theme = "dark"   # light · dark · ocean · sunset · forest · rose

# Custom tokens
class MyApp(App):
    theme = {"color.primary": "#FF6B6B", "color.background": "#FFF5F5"}
```

Built-in themes: `light`, `dark`, `ocean`, `sunset`, `forest`, `rose`

Runtime swap: `POST /pyui-api/theme/{name}` → reloads page with new theme

## Plugin system

```python
from pyui.plugins import PyUIPlugin, register_component

class MyPlugin(PyUIPlugin):
    name = "zolt-charts"
    version = "1.0.0"

    def on_load(self, app):
        register_component("LineChart", LineChartComponent)

class MyApp(App):
    plugins = [MyPlugin()]
```

Lifecycle hooks: `on_load`, `on_compile_start`, `on_compile_end`, `on_build`, `on_dev_start`

## Error codes

All exceptions carry `PYUI-NNN` codes:
- `PYUI-002` AppNotFoundError — no App subclass in file
- `PYUI-003` ModuleImportError — file can't be imported
- `PYUI-004` MissingRouteError — Page missing `route=`
- `PYUI-201` UnknownThemeError — unknown theme name
- `PYUI-301` PluginConflictError — duplicate component registration

## CLI commands

```bash
zolt new <name>              # scaffold project (--template blank|dashboard|landing|admin|auth|agency)
zolt templates               # interactive template browser + scaffold
zolt run [app.py]            # dev server with hot reload (--target web|desktop|cli)
zolt build [app.py]          # production build (--target web|desktop|cli|all)
zolt storybook               # component gallery on port 9000
zolt doctor                  # environment health check
zolt lint [app.py]           # validate component trees
zolt search <query>          # search PyPI for zolt-* packages
zolt publish                 # publish component package (requires pyui.json)
zolt info                    # version info
```

## Dev server endpoints

- `GET /{path}` — serve HTML page
- `POST /pyui-api/event/{handler_id}` — invoke Python event handler
- `POST /pyui-api/theme/{name}` — hot-swap theme (reloads page)
- `GET /pyui-api/ws` — WebSocket for hot reload
- `GET /pyui-api/devtools/state` — reactive state snapshot

## Agency template

`zolt new my-site --template agency` or `zolt templates` → select agency

Produces exact same structure as `examples/agency/`:
- `app.py`, `styles.py`, `sections/` with 8 section files
- Uses: `Section`, `VideoBg`, `BlurHeading`, `FloatingNav`, `Link`
- Requires hls.js (added to `App.head_scripts` automatically)

## Known constraints

- Import name is `pyui` (not `zolt`) — `from pyui import App` — intentional
- `AppMeta` runs at class definition time — pages must be in the class body
- `REACTIVE_VAR_REGISTRY` is module-level — not thread-safe for multi-user servers
- Hot reload re-imports the module on every file change
- `RawHTML` / `Text.inject_html()` bypass XSS protection — only use with trusted content
- Tailwind loaded from CDN — use `zolt build` for production static output
- `zolt build` produces static HTML — no server required for deployed apps

## v1.5 roadmap

ZoltCSS (replaces Tailwind), GSAP animations, Three.js 3D, 80+ Zolt UI components,
Figma import, Qt5/Qt6 desktop, AI skill files.
See `docs/Zolt_v1_5_PRD_TRD_Final.md`.
