# Zolt — Complete Agent Context

> Single source of truth for any AI agent working on this codebase.
> Read this before touching anything.

---

## What Is Zolt

Zolt is an open-source Python UI framework. Write your entire UI in pure Python — no HTML, no CSS, no JavaScript. One codebase compiles to web (HTML + Tailwind CSS + Alpine.js), desktop (tkinter), and terminal (Rich TUI).

- **Version:** 1.2.1
- **Python:** 3.10+
- **License:** MIT
- **Repo:** https://github.com/12errh/Zolt
- **PyPI:** `pip install zolt`
- **Import name:** `from pyui import App` (package is `zolt`, import is `pyui`)
- **Status:** v1.2.1 live on PyPI

---

## Project Structure

```
src/pyui/                        ← import name is pyui
├── __init__.py                  ← Public API — all user-facing exports
├── app.py                       ← App base class + AppMeta metaclass
│                                   App.extra_css, App.head_scripts added in v1.2
├── page.py                      ← Page class (routable screen)
├── exceptions.py                ← PyUIError hierarchy, PYUI-NNN error codes
├── linter.py                    ← lint_app()
├── scaffold.py                  ← create_project() — zolt new + zolt templates
│                                   agency template copies examples/agency/ directly
│
├── components/
│   ├── base.py                  ← BaseComponent — inlineStyle() added in v1.2
│   ├── layout/
│   │   ├── flex.py, grid.py, stack.py, container.py
│   │   ├── section.py           ← NEW v1.2: <section> with position:relative
│   │   ├── sidebar.py, split.py, divider.py, spacer.py, list.py
│   ├── display/
│   │   ├── text.py, heading.py, badge.py, tag.py, avatar.py
│   │   ├── blur_heading.py      ← NEW v1.2: word-by-word blur-reveal heading
│   │   ├── link.py              ← NEW v1.2: semantic <a> component
│   │   ├── icon.py, image.py, markdown.py, rawhtml.py
│   ├── input/
│   │   ├── button.py, input.py, textarea.py, select.py
│   │   ├── checkbox.py, radio.py, toggle.py, slider.py
│   │   ├── datepicker.py, filepicker.py, form.py
│   ├── feedback/
│   │   ├── alert.py, toast.py, modal.py, drawer.py
│   │   ├── tooltip.py, progress.py, spinner.py, skeleton.py
│   ├── navigation/
│   │   ├── nav.py, tabs.py, breadcrumb.py, pagination.py, menu.py
│   │   ├── floating_nav.py      ← NEW v1.2: fixed glassmorphism pill nav
│   ├── data/
│   │   ├── table.py, stat.py, chart.py
│   └── media/
│       ├── video.py
│       └── video_bg.py          ← NEW v1.2: absolutely-positioned bg video + HLS
│
├── compiler/
│   ├── ir.py                    ← build_ir_node/page/tree → IRTree
│   │                               stores inline_style, head_scripts in props/app_meta
│   └── discovery.py             ← discover_app() — imports user .py, finds App subclass
│
├── renderers/
│   ├── web/
│   │   ├── generator.py         ← WebGenerator — IRTree → full HTML
│   │   │   Dispatches: link, section, video_bg, blur_heading, floating_nav (v1.2)
│   │   │   _render_flex: supports inline_style prop
│   │   │   _render_text: supports inline_style prop
│   │   │   class_name post-processor: injects .className() into first class=""
│   │   └── tailwind.py          ← Tailwind CSS class mappings
│   ├── desktop/
│   │   └── tkinter_renderer.py  ← tkinter widget tree
│   └── cli/
│       └── generator.py         ← Rich TUI renderer
│
├── server/
│   └── dev_server.py            ← aiohttp dev server
│   CSP allows: media-src https:, connect-src https: (for HLS/video)
│
├── state/
│   ├── reactive.py              ← ReactiveVar + reactive()
│   ├── computed.py              ← ComputedVar + computed()
│   └── store.py                 ← Global Store singleton
│
├── theme/
│   ├── engine.py                ← build_theme, tokens_to_css_vars, tokens_to_figma
│   │   theme_swap_script(): pyuiSetTheme() — calls API then reloads page
│   │   dark_mode_script(): loads stored theme from localStorage on page load
│   └── tokens.py                ← DEFAULT_TOKENS + 6 built-in themes
│
├── plugins/
│   ├── base.py, registry.py, loader.py
│
├── hotreload/
│   ├── watcher.py               ← FileWatcher (watchdog-based)
│   └── diff.py                  ← diff_ir() — minimal IR patch generation
│
└── cli/
    ├── main.py                  ← Click CLI: new, run, build, storybook,
    │                               doctor, lint, search, publish, info, templates
    └── storybook.py             ← Component gallery (port 9000, hot reload enabled)
```

---

## Compilation Pipeline

```
User Python file
      │
      ▼
compiler/discovery.py
  discover_app("app.py")
  → adds file's parent dir to sys.path
  → imports module, finds App subclass
      │
      ▼
compiler/ir.py
  build_ir_tree(AppClass)
  → collects ReactiveVars, head_scripts, extra_css from App
  → calls build_ir_page() for each Page
  → build_ir_page() calls page.compose(), then build_ir_node() per child
  → build_ir_node() resolves props, stores class_name + inline_style,
    detects ReactiveVars/lambdas, registers event handlers
  → returns IRTree
      │
      ▼
renderers/web/generator.py
  WebGenerator(ir_tree).render_ir_page(ir_page)
  → dispatches each IRNode to _render_* function
  → post-processor injects class_name into first class="" attribute
  → scripts injected via sentinels (__PYUI_DARK_SCRIPT__, __PYUI_ALPINE_DATA__)
    to avoid .format() brace conflicts with JS code
  → returns complete HTML string
```

---

## Core Data Structures

### IRNode
```python
@dataclass
class IRNode:
    type: str                          # "button", "flex", "section", "video_bg", etc.
    props: dict[str, Any]              # resolved props + class_name + inline_style
    children: list[IRNode]
    events: dict[str, str]             # event_name → handler_id
    reactive_bindings: list[str]
    reactive_props: dict[str, list[str]]
    style_variant: str | None
    node_id: str
```

Key props stored by `build_ir_node`:
- `props["class_name"]` — space-joined string from `component._classes` (`.className()`)
- `props["inline_style"]` — raw CSS string from `component._inline_style` (`.inlineStyle()`)

### IRTree
```python
@dataclass
class IRTree:
    app_meta: dict[str, Any]   # name, version, description, favicon,
                               # extra_css, head_scripts
    pages: list[IRPage]
    theme: str | dict[str, str]
    reactive_vars: dict[str, Any]
    event_handlers: dict[str, Callable]
    persistent_vars: list[str]
```

---

## Component System

### BaseComponent (components/base.py)

Key internals:
- `_CONTEXT_STACK` — global stack. `with Flex():` pushes Flex; children auto-register.
- `component_type: str` — must be set on every subclass. Used by IR dispatcher.
- `props: dict` — all component-specific data.
- `_classes: list[str]` — from `.className()`, stored as `props["class_name"]`
- `_inline_style: str` — from `.inlineStyle()`, stored as `props["inline_style"]`

### Chainable API
```python
Button("Save")
    .style("primary")           # sets _style_variant
    .size("lg")                 # sets _size
    .className("my-class")      # appends to _classes
    .inlineStyle("z-index:10;") # sets _inline_style (v1.2)
    .disabled(False)
    .onClick(handler)
```

### Adding a New Component — Checklist
1. Create file in `src/pyui/components/<category>/`
2. Inherit from `BaseComponent`, set `component_type = "my_type"`
3. Export from category `__init__.py`
4. Export from `src/pyui/__init__.py` (import + `__all__`)
5. Add `"my_type": _render_my_type` to dispatch dict in `generator.py`
6. Add `_render_my_type(node: IRNode) -> str` in `generator.py`
   - Do NOT manually read `class_name` — the post-processor injects it automatically
   - Do NOT manually read `inline_style` unless you need to merge it into a style attr
7. Add widget builder in `renderers/desktop/tkinter_renderer.py`
8. Add renderer in `renderers/cli/generator.py`

### class_name Post-Processor (IMPORTANT)
After every `_render_*` function returns HTML, `_render_node` runs:
```python
custom_class = node.props.get("class_name", "").strip()
if custom_class and ' class="' in html:
    html = html.replace(' class="', f' class="{custom_class} ', 1)
```
This means: **never manually include `class_name` in your renderer output** — it will be doubled.

---

## New Components (v1.2)

### BlurHeading
```python
BlurHeading("The Website Your Brand Deserves", level=1, delay_ms=100)
    .className("text-white max-w-3xl mx-auto")
```
- Splits text into words, wraps each in `<span style="animation-delay:Nms">`
- Always applies `word-reveal font-heading` classes (Instrument Serif italic)
- Fluid font-size via `clamp()` per heading level (h1=clamp(3rem,8vw,6rem), etc.)
- `class_name` injected by post-processor — do not include manually

### Link
```python
Link("Get Started", href="#").style("glass").icon("arrow-up-right")
Link("Privacy", href="/privacy").style("footer")
```
Style variants: `glass`, `primary`, `ghost`, `nav`, `footer`

### Section
```python
with Section(min_height=560, bg="#000").className("h-screen"):
    VideoBg(src="...", hls=True)
    Flex(...).inlineStyle("position:absolute;inset:0;z-index:10;")
```
Renders as `<section style="position:relative;overflow:hidden;...">`.

### VideoBg
```python
VideoBg(src=MUX_URL, hls=True, desaturate=True, fade_height=160)
```
- `hls=True` → injects hls.js init script inline
- `desaturate=True` → `filter:saturate(0)`
- `fade_height` → top+bottom gradient fades in px (0 to disable)
- Requires hls.js loaded — add to `App.head_scripts`

### FloatingNav
```python
FloatingNav(
    logo_src="/images/logo.png",
    logo_alt="Studio",
    links=["Home", "Services", "Work"],  # or [("Home", "/"), ...]
    cta_text="Get Started",
    cta_href="#",
)
```
Renders as `position:fixed` nav with liquid-glass pill.

---

## App Class — Full Attributes

```python
class MyApp(App):
    name: str = "PyUI App"
    version: str = "1.0.0"
    description: str = ""
    icon: str | None = None
    favicon: str | None = None
    theme: str | dict[str, str] = "light"   # or ReactiveVar
    fonts: list[str] = ["Inter"]
    extra_css: str = ""                      # injected into <style> block
    head_scripts: list[str] = []             # CDN <script> tags in <head>
    meta: dict[str, str] = {}
    plugins: list[Any] = []
    # Pages declared as class attributes — AppMeta discovers them
    home = HomePage()
```

---

## State & Reactivity

```python
count = reactive(0)           # ReactiveVar[int]
name  = reactive("", persist=True)  # syncs to localStorage

count.get()                   # read
count.set(5)                  # write + notify subscribers
count.subscribe(fn)           # returns unsubscribe callable
```

Reactive Text:
```python
Text(lambda: f"Count: {count.get()}")  # re-renders on count change
```

Reactive theme (for theme switching):
```python
_theme = reactive("light")
class MyApp(App):
    theme = _theme
    current_theme = _theme
```

---

## Theme System

6 built-in themes: `light`, `dark`, `ocean`, `sunset`, `forest`, `rose`

Theme switching flow:
1. User calls `pyuiSetTheme('dark')` (JS function in every page)
2. Browser POSTs to `/pyui-api/theme/dark`
3. Server calls `app_class.theme.set('dark')` on the ReactiveVar
4. Server returns new CSS vars
5. Browser reloads → `build_ir_tree` reads new theme → page renders with dark tokens

`tokens_to_css_vars()` generates both CSS variables AND `!important` overrides for Tailwind classes (bg-white, text-gray-900, etc.) so theme colors actually apply visually.

---

## Web Renderer — Key Details

### Template Sentinels
The page template uses sentinels instead of `.format()` placeholders for content that contains `{`/`}`:
- `__PYUI_DARK_SCRIPT__` → replaced with `dark_mode_script() + theme_swap_script()`
- `"__PYUI_ALPINE_DATA__"` → replaced with actual JSON (single-quoted)

This avoids Python's `.format()` interpreting JS object literals as format placeholders.

### CSP Headers
```
media-src 'self' blob: https:    ← allows CloudFront MP4, Mux HLS blobs
connect-src 'self' ws: wss: https:  ← allows Mux HLS stream requests
img-src 'self' data: blob: https:   ← allows external images
```

### head_scripts
`App.head_scripts = ["https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"]`
→ injected as `<script src="..."></script>` tags in `<head>` before closing `</head>`.

---

## CLI Commands

| Command | Status | Notes |
|---|---|---|
| `zolt new <name>` | ✅ | `--template blank\|dashboard\|landing\|admin\|auth\|agency` |
| `zolt templates` | ✅ | Interactive table + prompt, scaffolds chosen template |
| `zolt run [app.py]` | ✅ | `--target web\|desktop\|cli`, `--port`, `--host`, `--no-browser` |
| `zolt build [app.py]` | ✅ | `--target web\|desktop\|cli\|all`, `--out` |
| `zolt storybook` | ✅ | Port 9000, hot reload enabled |
| `zolt doctor` | ✅ | Python, deps, ports, PyPI version |
| `zolt lint [app.py]` | ✅ | Missing alt, empty pages, duplicate routes |
| `zolt search <query>` | ✅ | Searches PyPI for zolt-* packages |
| `zolt publish` | ✅ | Validates pyui.json, runs build + twine upload |
| `zolt info` | ✅ | Version info panel |

---

## Agency Template — Scaffold Behaviour

`create_project(name, template="agency")`:
1. If `examples/agency/` exists (dev/editable install) → copies files directly, updates `name` in `app.py`
2. If not (installed package) → writes inline file constants from `_SECTION_*` strings in `scaffold.py`

Output structure:
```
<name>/
├── app.py, styles.py, requirements.txt, README.md
└── sections/
    ├── __init__.py, navbar.py, hero.py, start.py
    ├── features_chess.py, features_grid.py
    ├── stats.py, testimonials.py, cta_footer.py
```

---

## Testing

```bash
pytest                          # all 243 tests
pytest tests/test_compiler/
pytest tests/test_renderers/
pytest tests/test_theme/
pytest tests/integration/
```

- `conftest.py` resets global store between every test
- `asyncio_mode = "auto"` — async tests work without decorators
- E2E tests require Playwright, marked `@pytest.mark.e2e`

---

## Code Style

```bash
ruff check src/ tests/ examples/agency/   # lint
ruff format src/ tests/ examples/agency/  # format
mypy src/pyui/ --ignore-missing-imports   # type check
```

- Line length: 100
- Ruff rules: E, F, I, UP, B, SIM (E501 ignored)
- Per-file ignores: SIM117 for `storybook.py` and `tests/landing.py`
  (nested `with` blocks are intentional PyUI composition pattern)
- MyPy: strict, ignore_missing_imports = true

---

## Known Constraints

- Import name is `pyui` (not `zolt`) — `from pyui import App` — intentional
- `AppMeta` runs at class definition time — pages must be in the class body
- `REACTIVE_VAR_REGISTRY` is module-level — not thread-safe for multi-user servers
- Hot reload re-imports the module on every file change
- `RawHTML` / `Text.inject_html()` bypass XSS protection — only use with trusted content
- Tailwind loaded from CDN — not suitable for production without `zolt build`
- `zolt build` produces static HTML — no server required for deployed apps

---

## v1.5 Roadmap

See `docs/Zolt_v1_5_PRD_TRD_Final.md` for the full plan.

Key changes in v1.5:
- **ZoltCSS** — replaces Tailwind entirely. Zero CDN. Zero class names visible to developer.
- **zolt-bundler** — GSAP, Three.js, Alpine.js as local assets. No npm.
- **Animation Engine** — GSAP-powered, declared in Python.
- **3D Engine** — Three.js scenes from Python.
- **Zolt UI** — 80+ prebuilt components on ZoltCSS.
- **Figma import** — `zolt import figma <url>`
- **Qt5 + Qt6** desktop upgrade
- **AI skill files** — 100% API coverage for Claude Code, Cursor, etc.
