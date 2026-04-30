# Changelog

All notable changes to PyUI are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [1.1.1] - 2026-04-30

### Fixed
- **Theme switching** — `pyuiSetTheme` was not defined in the browser due to
  JS brace escaping bug in the template engine. Scripts are now injected via
  sentinel replacement instead of `str.format()`, so `{`/`}` in JS are never
  mangled.
- **Alpine data** — `x-data` was rendering as the literal string `{alpine_data}`
  instead of the actual JSON. Fixed with the same sentinel approach.
- **Theme colors not applying** — components use hardcoded Tailwind classes that
  ignore CSS variables. `tokens_to_css_vars()` now emits `!important` CSS
  overrides for all key Tailwind classes so every theme visually applies.
- **Body background** — removed hardcoded `bg-white text-gray-900` from `<body>`,
  now uses `var(--pyui-color-background)` and `var(--pyui-color-text)`.
- **Hot reload off in storybook** — `run_storybook()` now passes `watch_file`
  so the `FileWatcher` is active during `zolt storybook`.
- **CSP blocking images** — `img-src` now allows `https:` for external images.

### Changed
- Ruff: auto-fixed 66 lint issues across `src/` and `tests/`.
- Ruff format: reformatted 17 files.
- Mypy: resolved all type errors in `dev_server.py` and `storybook.py`.

---

## [1.1.0] - 2026-04-26

### Changed
- Package renamed from `zeno-py` → `zolt` (PyPI name conflict resolved)
- CLI command renamed from `zeno` → `zolt`
- All branding updated: Zeno → Zolt throughout codebase
- GitHub repo renamed to `12errh/zolt`
- Docs URL updated to `https://zolt.dev`
- Version bump 1.0.0 → 1.1.0 to reflect the rename

### Fixed
- PyPI upload blocked by name similarity to existing `zeno` package

---

## [1.0.0] - 2026-04-26

### 🎉 First stable release

PyUI is now production-ready. All eight development phases are complete.

### Added — Phase 4: Desktop & CLI Renderers
- **tkinter renderer** — `pyui run --target desktop` opens a native window
  - 31 component builders with lazy tkinter imports (no display required at import time)
  - Reactive state subscriptions via `ReactiveVar.subscribe()`
  - Scrollable canvas, multi-page Notebook, sv-ttk theme support
  - `raw_html` rendered as plain-text (HTML stripped)
- **Rich TUI renderer** — `pyui run --target cli` renders in the terminal
  - 35+ component renderers mapping to Rich Panel, Table, Columns, Rule, etc.
  - Interactive button prompts with state re-render after handler execution
  - ASCII bar charts for Chart component
- **`pyui build --target desktop/cli`** — writes `run.py` launcher + `README.txt`
- **`pyui build --target all`** — builds all three targets into `dist/web/`, `dist/desktop/`, `dist/cli/`

### Added — Phase 5: Theme Engine & Plugin System
- **Theme engine** (`src/pyui/theme/engine.py`)
  - `build_theme(name|dict)` — merges overrides onto `DEFAULT_TOKENS`, raises `ThemeError` for unknown names
  - `tokens_to_css_vars()` — renders `--pyui-*` CSS variables in a `:root` block
  - `tokens_to_figma()` — exports W3C design tokens JSON for Figma / Tokens Studio
  - `dark_mode_script()` — injects `prefers-color-scheme` auto-detection into every page
  - `theme_swap_script()` — provides `pyuiSetTheme()` JS for runtime switching
  - `POST /pyui-api/theme/{name}` endpoint for live hot-swap
- **Plugin system** (`src/pyui/plugins/`)
  - `PyUIPlugin` base class with 5 lifecycle hooks: `on_load`, `on_compile_start`, `on_compile_end`, `on_build`, `on_dev_start`
  - Component registry: `register_component` / `get_component` / `list_components`
  - `load_plugins()` called automatically by `compile_app()` before IR building
  - `PyUIPlugin` + `register_component` exported from `pyui` root
- **`pyui search <query>`** — searches PyPI for `pyui-*` packages
- **`pyui publish`** — validates `pyui.json`, runs `python -m build`, uploads via `twine`
  - `--build-only` flag to build without uploading

### Added — Phase 6: Developer Tooling & Hot Reload
- **Hot reload** — file save → browser update
  - `FileWatcher` (watchdog-based, debounced) monitors `.py` files
  - `_reimport_app()` re-executes the user's file from disk on every change
  - WebSocket broadcaster sends `{"type": "reload"}` to all connected browsers
  - Compiler errors broadcast as `{"type": "error"}` — shown as styled overlay in browser
- **Error overlay** — dismissable error panel in browser on compile failure
- **Dev tools panel** — `⚙ PyUI` button in every page (bottom-right)
  - State tab: live reactive vars, auto-updates via Alpine.effect
  - Pages tab: all routes with active page highlighted
  - Events tab: log of every `__pyuiEvent` call
- **`pyui doctor`** — full environment check: Python version, all 6 deps, port availability, PyPI version
- **`pyui lint`** — validates component trees: missing `alt`, empty pages, duplicate routes, unknown variants
- **`pyui new`** — fully implemented scaffold
  - `blank` template: App + Page + Button
  - `dashboard` template: Nav + Stats + Table + 3 pages

### Added — Phase 7: Production Hardening
- **Structured error codes** — every exception carries a `PYUI-NNN` code
  - `PYUI-001` CompilerError, `PYUI-002` AppNotFoundError, `PYUI-003` ModuleImportError
  - `PYUI-004` MissingRouteError, `PYUI-005` DuplicateRouteError, `PYUI-006` IRBuildError
  - `PYUI-100` ComponentError, `PYUI-101` InvalidPropError, `PYUI-102` UnknownComponentError
  - `PYUI-200` ThemeError, `PYUI-201` UnknownThemeError, `PYUI-202` InvalidTokenError
  - `PYUI-300` PluginError, `PYUI-301` PluginConflictError
  - `PYUI-400` CLIError, `PYUI-401` BuildError
  - All error messages include suggested fixes
- **Security hardening** — dev server security middleware
  - Content-Security-Policy header on all responses
  - `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`
  - CORS scoped to localhost API routes only
- **Graceful component degradation** — broken component renders an error card, not a Python crash
- **Build stats** — `pyui build --target web` reports page count, total KB, and elapsed ms
- **5 example apps** in `examples/`
  - `dashboard/` — analytics dashboard with stats, chart, table
  - `todo/` — reactive todo list
  - `blog/` — content site with routing
  - `ml-demo/` — ML inference UI with mock model
  - `admin/` — CRUD admin panel with 3 pages
- **Integration tests** — 13 end-to-end pipeline tests

---

## [0.1.0] - 2026-04-12

### Added — Phase 0: Project Setup
- `pyproject.toml` with hatchling build system
- `App` and `Page` base classes with `AppMeta` metaclass
- `BaseComponent` with full chainable API
- Exception hierarchy: `PyUIError`, `CompilerError`, `ComponentError`, `ThemeError`, `PluginError`
- Structured logging via `structlog`
- GitHub Actions CI, pre-commit hooks (ruff, mypy)

### Added — Phase 1: Core Compiler (Web)
- IR pipeline: `build_ir_node` → `build_ir_page` → `build_ir_tree`
- `WebGenerator` — IRTree → HTML/Tailwind/Alpine.js
- `PyUIDevServer` — aiohttp dev server with event POST handler
- First 5 components: `Page`, `Button`, `Text`, `Heading`, `Grid`

### Added — Phase 2: Full Component Library
- **42+ components** across 7 categories
  - Layout: `Flex`, `Stack`, `Container`, `Divider`, `Spacer`, `Sidebar`, `Split`, `List`
  - Display: `Badge`, `Tag`, `Avatar`, `Icon`, `Image`, `Markdown`, `Video`, `RawHTML`
  - Input: `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Toggle`, `Slider`, `DatePicker`, `FilePicker`, `Form`
  - Feedback: `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`, `Spinner`, `Skeleton`
  - Navigation: `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu`
  - Data: `Table`, `Stat`, `Chart` (line, bar, pie via Chart.js)
- `pyui storybook` — component gallery
- `compose()` method on Pages + context manager composition

### Added — Phase 3: State & Reactivity
- `ReactiveVar[T]` — observable value with subscribers
- `ComputedVar[T]` — read-only derived reactive value with auto dependency tracking
- `Store` — global singleton for named reactive state
- `persist=True` — syncs ReactiveVar to `localStorage`
- `x-model` two-way binding for all input components
- `List` component for reactive list rendering
- Alpine.js store integration for browser-side reactivity

---

## [0.0.1] - 2026-04-10

### Added
- Phase 0 skeleton: package structure, CI, pre-commit
