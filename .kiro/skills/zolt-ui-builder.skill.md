---
name: zolt-ui-builder
description: Expert guide for building beautiful UIs with the Zolt framework
inclusion: manual
---

# Zolt UI Builder — Expert Skill

You are an expert Zolt UI developer. When asked to build a UI, you produce clean, production-quality Python code using the Zolt framework. Follow every rule in this document precisely.

---

## Framework Fundamentals

**Install:** `pip install zolt`  
**Run:** `zolt run app.py`  
**Import name is `pyui`, NOT `zolt`:**

```python
from pyui import App, Page, Flex, Grid, Heading, Text, Button, reactive
```

**Version:** 1.1.0

---

## App & Page Structure

### The Golden Rule — Page Registration

Pages MUST be declared as class attributes inside the App class body. `AppMeta` runs at class definition time.

```python
# ✅ CORRECT
class MyApp(App):
    home = HomePage()
    about = AboutPage()

# ❌ WRONG — causes 404, AppMeta already ran
class MyApp(App):
    pass
MyApp.home = HomePage()
```

### App Class

```python
class MyApp(App):
    name = "My App"           # browser title / window title
    version = "1.0.0"
    description = "Short description for meta tags"
    theme = "light"           # "light" | "dark" | "ocean" | "sunset" | "forest" | "rose"
    fonts = ["Inter"]         # Google Font families
    plugins = []              # PyUIPlugin instances

    # Reactive vars registered here for IR compilation
    count = _count            # reference module-level reactive vars

    # Pages — must be class attributes
    home = HomePage()
    about = AboutPage()
```

### Page Class — Two Styles

**Style 1: Declarative `compose()` method (preferred)**

```python
class HomePage(Page):
    title = "Home"
    route = "/"
    layout = "default"   # "default" | "full-width" | "sidebar" | "auth"

    def compose(self) -> None:
        with Flex(direction="col", gap=8):
            Heading("Hello", level=1)
            Text("Welcome").style("muted")
```

**Style 2: Imperative `.add()` (for simple pages)**

```python
home = Page(title="Home", route="/")
home.add(
    Heading("Hello"),
    Text("Welcome"),
)
```

### Page Layouts

| Layout | Description |
|--------|-------------|
| `"default"` | `container mx-auto px-6 py-10 max-w-7xl` |
| `"full-width"` | `w-full` — edge to edge |
| `"sidebar"` | `flex gap-8 px-6 py-10 max-w-7xl mx-auto` |
| `"auth"` | Centered vertically and horizontally, gray background |

---

## Reactive State

### Pattern — Always Module-Level

```python
# 1. Define at module level
_count = reactive(0)
_name = reactive("")
_items = reactive([])
_token = reactive("", persist=True)  # persists to localStorage

# 2. Reference in App class for IR registration
class MyApp(App):
    count = _count
    name = _name
```

### ReactiveVar API

```python
count = reactive(0)
count.get()                          # read value
count.set(5)                         # write value (notifies subscribers)
unsub = count.subscribe(lambda v: print(v))
unsub()                              # unsubscribe
```

### Computed Values (derived, read-only)

```python
from pyui import computed

count = reactive(3)
doubled = computed(lambda: count.get() * 2)
# doubled auto-updates when count changes
doubled.get()   # → 6
```

### Global Store (cross-page state)

```python
from pyui import store

username = store.define("username", "Guest")
store.get("username").set("Alice")
store.snapshot()   # → {"username": "Alice"}
```

### Reactive in Components

```python
# Reactive text — lambda re-evaluates on state change
Text(lambda: f"Count: {_count.get()}")

# Reactive badge
Badge(lambda: str(_count.get()), variant="primary")

# Reactive visibility
Button("Delete").hidden(lambda: not _is_admin.get())

# Reactive disabled
Button("Submit").disabled(lambda: _loading.get())

# Reactive value binding
Input(value=_name, placeholder="Your name")
```

---

## Component API — Universal Methods

Every component supports these chainable methods:

```python
component
  .style("primary")          # style variant
  .size("lg")                # size preset
  .margin(16)                # CSS margin shorthand
  .padding(8, 16)            # CSS padding shorthand
  .width("100%")             # width
  .height(400)               # height
  .className("custom-class") # raw Tailwind classes (escape hatch)
  .hidden(condition)         # hide when truthy (bool or ReactiveVar)
  .disabled(condition)       # disable when truthy
  .id("my-element")          # override auto-generated ID
  .onClick(handler)          # click event
  .onChange(handler)         # change event
  .onHover(handler)          # hover event
  .onMount(handler)          # lifecycle: mounted
  .onUnmount(handler)        # lifecycle: removed
  .add(*children)            # append children
```

---

## Layout Components

### Flex

```python
Flex(
    direction="row",    # "row" | "col" | "row-reverse" | "col-reverse"
    align="center",     # "start" | "center" | "end" | "baseline" | "stretch"
    justify="start",    # "start" | "center" | "end" | "between" | "around" | "evenly"
    gap=4,              # gap on 4px/8px scale
    wrap=False,
)

# Common patterns
with Flex(direction="col", gap=6):
    ...

with Flex(align="center", justify="between"):
    Heading("Title")
    Button("Action").style("primary")
```

### Grid

```python
Grid(
    cols=3,             # 1–12 or responsive string "1 sm:2 lg:3"
    gap=4,              # gap scale
    rows=None,          # explicit row count (optional)
)
.align("stretch")       # "start" | "center" | "end" | "stretch"
.justify("start")       # "start" | "center" | "end" | "between"

# Common patterns
with Grid(cols=3, gap=6):
    for item in items:
        Card(...)
```

### Container

```python
Container(
    size="xl",          # "sm" | "md" | "lg" | "xl" | "2xl" | "6xl" | "full"
    centered=True,
)
```

### Stack

```python
Stack(
    direction="vertical",   # "vertical" | "horizontal"
    spacing=4,
)
```

### Sidebar

```python
Sidebar(side="left", width=280)
  .sidebar(Nav(...))
  .content(MainContent())
```

### Split

```python
Split(direction="horizontal", ratio=0.3)
  .first(LeftPanel())
  .second(RightPanel())
```

### Divider

```python
Divider()                          # horizontal hairline
Divider(direction="vertical")      # vertical
Divider(label="OR")                # with centered label
```

### Spacer

```python
Spacer()          # flex-grow (fills remaining space)
Spacer(size=8)    # fixed 32px space
```

### List (reactive)

```python
List(items=_items, render=lambda item: Text(item))
```

---

## Display Components

### Text

```python
Text("Static content")
Text(lambda: f"Dynamic: {_count.get()}")   # reactive

# Style variants
Text("Muted").style("muted")       # gray-500
Text("Code").style("code")         # monospace, inset
Text("Lead").style("lead")         # larger, lighter
Text("Small").style("small")       # xs, uppercase tracking
Text("Error").style("error")       # red
Text("Success").style("success")   # emerald
Text("Caption").style("caption")   # xs, uppercase, widest tracking

# Element type
Text("Paragraph").paragraph()      # renders as <p>
Text("Label").label()              # renders as <label>
Text("Truncated...").truncate()    # ellipsis overflow
```

### Heading

```python
Heading("Title", level=1)          # h1–h6
Heading("Section", level=2)

# Style variants
Heading("Gradient", level=1).style("gradient")   # violet→indigo gradient
Heading("Muted", level=3).style("muted")         # gray-400, normal weight
Heading("Hero", level=1).style("display")        # 6xl, extrabold
Heading("Code", level=2).style("mono")           # monospace

# With subtitle
Heading("Title", level=1, subtitle="Subtitle text")
```

### Badge

```python
Badge("New", variant="primary")    # violet
Badge("Active", variant="success") # emerald
Badge("Error", variant="danger")   # red
Badge("Warn", variant="warning")   # amber
Badge("Info", variant="info")      # sky
Badge("Dark", variant="dark")      # gray-900
Badge("Tag", variant="secondary")  # gray-50

# Reactive badge
Badge(lambda: str(_count.get()), variant="primary")
```

### Tag

```python
Tag("Python", variant="primary")
Tag("Tutorial", variant="secondary")
```

### Avatar

```python
Avatar(src="https://...", name="Alice", size="md")
# Sizes: "xs" | "sm" | "md" | "lg" | "xl" | "2xl"
# Falls back to initials from name if src fails
```

### Icon

```python
Icon(name="zap", size=20, color="gray-500")
# Uses Lucide icons — any Lucide icon name works
# Common: "zap", "star", "check", "x", "plus", "arrow-right",
#         "user", "settings", "home", "search", "bell", "github"
```

### Image

```python
Image(src="https://...", alt="Description", width=400, height=300)
  .fit("cover")    # "cover" | "contain" | "fill" | "none" | "scale-down"
```

### Markdown

```python
Markdown("# Hello\n\nThis is **markdown** content.")
Markdown(lambda: _content.get())   # reactive
```

### RawHTML

```python
RawHTML("<strong>Raw HTML</strong>")
# ⚠️ Only use with trusted content — bypasses XSS protection
```

---

## Input Components

### Button

```python
Button("Save").style("primary").size("lg").onClick(handler)

# Style variants
Button("Primary").style("primary")     # black filled
Button("Secondary").style("secondary") # gray-100 filled
Button("Ghost").style("ghost")         # white with border
Button("Danger").style("danger")       # red
Button("Success").style("success")     # emerald
Button("Link").style("link")           # inline text link
Button("CTA").style("gradient")        # violet→indigo gradient

# Sizes: "xs" | "sm" | "md" | "lg" | "xl"

# Special states
Button("Loading").loading(True)
Button("Disabled").disabled(True)
Button("Submit").submit()              # type="submit" for forms

# With icons (Lucide icon names)
Button("Save").icon("save")
Button("Next").icon("arrow-right", position="right")
```

### Input

```python
Input(
    value=_name,              # str or ReactiveVar[str]
    placeholder="Enter text",
    type="text",              # "text" | "email" | "password" | "number" | "url"
    label="Full Name",
)
.onChange(lambda: None)       # called on every keystroke
```

### Textarea

```python
Textarea(
    value=_bio,
    placeholder="Tell us about yourself...",
    rows=4,
    label="Bio",
)
```

### Select

```python
Select(
    options=[
        ("value1", "Display Label 1"),
        ("value2", "Display Label 2"),
    ],
    value=_selected,          # ReactiveVar[str]
    label="Choose option",
)
.onChange(lambda: None)
```

### Checkbox

```python
Checkbox(checked=_agreed, label="I agree to the terms")
.onChange(lambda: None)
```

### Radio

```python
Radio(
    options=[("a", "Option A"), ("b", "Option B")],
    value=_choice,
    label="Select one",
)
```

### Toggle

```python
Toggle(checked=_enabled, label="Enable notifications")
.onChange(lambda: None)
```

### Slider

```python
Slider(
    value=_volume,
    min=0, max=100, step=1,
    label=lambda: f"Volume: {_volume.get()}%",
)
```

### DatePicker

```python
DatePicker(value=_date, label="Select date")
```

### FilePicker

```python
FilePicker(label="Upload file", multiple=False, accept=".pdf,.png")
```

### Form

```python
with Form(title="Contact Us").onSubmit(handle_submit):
    Input(value=_email, placeholder="Email", label="Email", type="email")
    Textarea(value=_message, placeholder="Message", label="Message")
    Button("Send").style("primary").submit()
```

---

## Feedback Components

### Alert

```python
Alert("Title", "Optional description", variant="info")
# Variants: "info" | "success" | "warning" | "danger"

Alert("Success!", "Your changes were saved.", variant="success")
Alert("Warning", "This action cannot be undone.", variant="warning")
Alert("Error", "Something went wrong.", variant="danger")

# Conditional alert
if _flash_msg.get():
    Alert(_flash_msg.get(), variant=_flash_type.get())
```

### Toast

```python
Toast("Saved!", variant="success", duration=3000)
Toast("Error occurred", variant="danger")
```

### Modal

```python
Modal(title="Confirm Delete", open=_modal_open.get())
  .add(Text("Are you sure?"))
  .footer(
      Button("Cancel").style("ghost").onClick(lambda: _modal_open.set(False)),
      Button("Delete").style("danger").onClick(handle_delete),
  )
```

### Drawer

```python
Drawer(title="Settings", open=_drawer_open.get(), side="right")
  .add(Text("Drawer content here"))
```

### Tooltip

```python
Tooltip("This is a helpful tip").add(
    Button("Hover me")
)
```

### Progress

```python
Progress(value=75, max=100)
Progress(value=_progress.get(), max=100)
Progress(value=60, circular=True)
```

### Spinner

```python
Spinner(size="md")
# Sizes: "xs" | "sm" | "md" | "lg" | "xl"
```

### Skeleton

```python
Skeleton()                      # text line placeholder
Skeleton(variant="rect")        # rectangle placeholder
Skeleton(variant="circle")      # circle placeholder
```

---

## Navigation Components

### Nav

```python
Nav(items=[
    ("Home", "/"),
    ("About", "/about"),
    ("Contact", "/contact"),
])
```

### Tabs

```python
Tabs(active_tab="overview")
  .add_tab("Overview",
      Heading("Overview", level=2),
      Text("Content here"),
  )
  .add_tab("Details",
      Text("Details content"),
  )
```

### Breadcrumb

```python
Breadcrumb(items=[
    ("Home", "/"),
    ("Products", "/products"),
    ("Item", None),   # None = current page (no link)
])
```

### Pagination

```python
Pagination(current=_page.get(), total=10)
  .onChange(lambda: None)
```

### Menu

```python
Menu(items=[
    ("Edit", handle_edit),
    ("Duplicate", handle_duplicate),
    ("Delete", handle_delete),
])
```

---

## Data Components

### Table

```python
Table(
    headers=["Name", "Email", "Role", "Status"],
    rows=[
        ["Alice", "alice@example.com", "Admin", "Active"],
        ["Bob",   "bob@example.com",   "User",  "Inactive"],
    ],
)
.striped()       # alternating row colors
.scrollable()    # horizontal scroll on overflow
```

### Stat (KPI Card)

```python
Stat("Total Users", "24,521", trend="+12%", trend_up=True)
Stat("Churn Rate",  "2.4%",   trend="-0.8%", trend_up=False)
Stat("Revenue",     lambda: f"${_revenue.get():,}")   # reactive value
```

### Chart

```python
Chart(
    type="line",    # "line" | "bar" | "pie"
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets=[{
        "label": "Revenue ($k)",
        "data": [42, 55, 61, 70, 78, 84],
        "borderColor": "#6C63FF",
        "backgroundColor": "rgba(108,99,255,0.1)",
    }],
)

# Bar chart
Chart(
    type="bar",
    labels=["Q1", "Q2", "Q3", "Q4"],
    datasets=[{
        "label": "Sales",
        "data": [120, 190, 150, 210],
        "backgroundColor": "#6C63FF",
    }],
)

# Pie chart
Chart(
    type="pie",
    labels=["Direct", "Organic", "Referral"],
    datasets=[{
        "data": [40, 35, 25],
        "backgroundColor": ["#6C63FF", "#10B981", "#F59E0B"],
    }],
)
```

---

## Media Components

### Video

```python
Video(
    src="https://example.com/video.mp4",
    poster="https://example.com/thumb.jpg",
    controls=True,
    autoplay=False,
    loop=False,
)
```

---

## Theme System

### Built-in Themes

| Theme | Primary | Background | Personality |
|-------|---------|------------|-------------|
| `"light"` | #6C63FF violet | #FFFFFF | Clean, modern default |
| `"dark"` | #7C73FF | #0F172A | Elegant dark mode |
| `"ocean"` | #0EA5E9 sky | #F0F9FF | Calm, professional |
| `"sunset"` | #F97316 orange | #FFF7ED | Warm, energetic |
| `"forest"` | #10B981 emerald | #F0FDF4 | Natural, calm |
| `"rose"` | #F43F5E | #FFF1F2 | Bold, expressive |

```python
class MyApp(App):
    theme = "dark"
```

### Custom Theme

Override only the tokens you want — everything else inherits from `light`:

```python
class MyApp(App):
    theme = {
        "color.primary":       "#FF6B6B",
        "color.primary.hover": "#E55555",
        "color.background":    "#FFF5F5",
        "color.surface":       "#FFE8E8",
        "font.family":         "Poppins, sans-serif",
        "radius.md":           "12px",
    }
```

### Full Token Reference

```
color.primary          color.primary.hover
color.secondary        color.secondary.hover
color.background       color.surface
color.text             color.text.muted
color.border
color.success          color.warning
color.danger           color.info

font.family
font.size.xs  .sm  .md  .lg  .xl  .2xl
font.weight.normal  .medium  .bold

space.1  .2  .3  .4  .6  .8  .12  .16

radius.sm  .md  .lg  .xl  .full

shadow.sm  .md  .lg

transition.fast  .normal  .slow
```

---

## Design Patterns & Best Practices

### Card Pattern

```python
with Flex(direction="col", gap=4).className(
    "bg-white border border-gray-100 rounded-2xl p-6 shadow-sm "
    "hover:shadow-md transition-shadow"
):
    Heading("Card Title", level=3)
    Text("Card description").style("muted").paragraph()
    Button("Action").style("primary")
```

### Hero Section

```python
with Flex(direction="col", align="center", gap=6).className(
    "py-24 text-center max-w-3xl mx-auto"
):
    Badge("New Release", variant="secondary")
    Heading("Build UIs in Pure Python", level=1).style("gradient")
    Text(
        "Write once, render anywhere — web, desktop, and terminal."
    ).style("lead").paragraph()
    with Flex(gap=3):
        Button("Get Started").style("gradient").size("lg")
        Button("View Docs").style("ghost").size("lg")
```

### Dashboard Layout

```python
class DashboardPage(Page):
    title = "Dashboard"
    route = "/"

    def compose(self) -> None:
        Nav(items=[("Dashboard", "/"), ("Reports", "/reports")])

        with Flex(direction="col", gap=8):
            with Flex(align="center", justify="between"):
                Heading("Analytics", level=1)
                Badge("Live", variant="success")

            with Grid(cols=4, gap=6):
                Stat("Users",   "24,521", trend="+12%", trend_up=True)
                Stat("Revenue", "$84,200", trend="+6%",  trend_up=True)
                Stat("Sessions","1,429",   trend="+3%",  trend_up=True)
                Stat("Churn",   "2.4%",    trend="-0.8%",trend_up=False)

            Chart(type="line", labels=[...], datasets=[...])

            Table(headers=[...], rows=[...]).striped()
```

### Form Pattern

```python
_email = reactive("")
_password = reactive("")

def _handle_login():
    # validate and submit
    pass

class LoginPage(Page):
    title = "Login"
    route = "/login"
    layout = "auth"

    def compose(self) -> None:
        with Flex(direction="col", gap=6).className(
            "w-full max-w-sm bg-white rounded-2xl p-8 "
            "shadow-[0_4px_24px_rgba(0,0,0,0.08)] border border-gray-100"
        ):
            Heading("Welcome back", level=2)
            Text("Sign in to your account").style("muted")

            with Form().onSubmit(_handle_login):
                Input(value=_email, placeholder="Email", label="Email", type="email")
                Input(value=_password, placeholder="Password", label="Password", type="password")
                Button("Sign in").style("primary").size("lg").submit()
                    .className("w-full")
```

### Reactive List Pattern

```python
_todos: list[dict] = []
_count = reactive(0)
_new_text = reactive("")

def _add_todo():
    text = _new_text.get().strip()
    if text:
        _todos.append({"text": text, "done": False})
        _count.set(len(_todos))
        _new_text.set("")

def _toggle(index: int):
    if 0 <= index < len(_todos):
        _todos[index]["done"] = not _todos[index]["done"]

class TodoPage(Page):
    title = "Todos"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", gap=6).className("max-w-lg mx-auto py-12"):
            with Flex(gap=3):
                Input(value=_new_text, placeholder="Add todo...").onChange(lambda: None)
                Button("Add").style("primary").onClick(_add_todo)

            with Flex(direction="col", gap=2):
                for i, todo in enumerate(_todos):
                    with Flex(align="center", justify="between").className(
                        "p-4 bg-white border border-gray-100 rounded-xl shadow-sm"
                    ):
                        Text(todo["text"]).className(
                            "line-through text-gray-400" if todo["done"] else ""
                        )
                        Button("✓").style("success").size("sm").onClick(
                            lambda idx=i: _toggle(idx)
                        )
```

### Multi-Page App Pattern

```python
_count = reactive(0)
_name = reactive("")

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self) -> None:
        Nav(items=[("Home", "/"), ("About", "/about")])
        with Flex(direction="col", gap=6):
            Heading("Home", level=1)

class AboutPage(Page):
    title = "About"
    route = "/about"

    def compose(self) -> None:
        Nav(items=[("Home", "/"), ("About", "/about")])
        with Flex(direction="col", gap=6):
            Heading("About", level=1)

class MyApp(App):
    name = "My App"
    theme = "light"

    count = _count
    name = _name

    home = HomePage()
    about = AboutPage()
```

---

## className — Tailwind Escape Hatch

Use `.className()` for layout, spacing, and visual tweaks not covered by the component API:

```python
# Centering and max-width
Flex(...).className("max-w-3xl mx-auto py-12 px-4")

# Card styling
Flex(...).className(
    "bg-white border border-gray-100 rounded-2xl p-6 "
    "shadow-sm hover:shadow-md transition-shadow cursor-pointer"
)

# Full width button
Button("Submit").style("primary").className("w-full")

# Custom text styling
Text("Label").className("font-semibold text-gray-900 text-sm uppercase tracking-wide")

# Responsive grid
Grid(cols=1).className("sm:grid-cols-2 lg:grid-cols-3")
```

---

## Error Codes

| Code | Error | Cause |
|------|-------|-------|
| `PYUI-002` | `AppNotFoundError` | No `App` subclass in file |
| `PYUI-003` | `ModuleImportError` | File can't be imported |
| `PYUI-004` | `MissingRouteError` | Page missing `route=` |
| `PYUI-201` | `UnknownThemeError` | Unknown theme name |
| `PYUI-301` | `PluginConflictError` | Duplicate component registration |

---

## CLI Reference

```bash
zolt new <name>                          # scaffold new project
zolt new <name> --template dashboard     # from template (blank|dashboard|landing|admin|auth)
zolt run [app.py]                        # dev server with hot reload (default: web)
zolt run app.py --target desktop         # run as desktop window
zolt run app.py --target cli             # run as terminal UI
zolt build [app.py]                      # production build
zolt build app.py --target all           # build all targets
zolt storybook                           # component gallery on port 9000
zolt doctor                              # environment health check
zolt lint [app.py]                       # validate component trees
zolt search <query>                      # search PyPI for zolt-* packages
zolt publish                             # publish component package
```

---

## Dev Server Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/{path}` | GET | Serve HTML page |
| `/pyui-api/event/{handler_id}` | POST | Invoke Python event handler |
| `/pyui-api/theme/{name}` | POST | Hot-swap theme |
| `/pyui-api/ws` | WS | Hot reload WebSocket |
| `/pyui-api/devtools/state` | GET | Reactive state snapshot |

---

## Known Constraints

- Import name is `pyui` (not `zolt`) — `from pyui import App` — intentional
- `AppMeta` runs at class definition time — pages must be in the class body
- `REACTIVE_VAR_REGISTRY` is module-level — not thread-safe for multi-user servers
- Hot reload re-imports the module on every file change
- `RawHTML` / `Text.inject_html()` bypass XSS protection — only use with trusted content
- Reactive state updates require the reactive var to be registered in the App class

---

## Complete Minimal Example

```python
from pyui import App, Button, Flex, Heading, Page, Text, reactive

_count = reactive(0)

def _increment():
    _count.set(_count.get() + 1)

def _decrement():
    if _count.get() > 0:
        _count.set(_count.get() - 1)

class HomePage(Page):
    title = "Counter"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", align="center", gap=6).className("py-24"):
            Heading("Counter", level=1)
            Text(lambda: f"Count: {_count.get()}").style("lead")
            with Flex(gap=3):
                Button("−").style("ghost").size("lg").onClick(_decrement)
                Button("+").style("primary").size("lg").onClick(_increment)

class CounterApp(App):
    name = "Counter"
    theme = "light"
    count = _count
    home = HomePage()
```

Run with: `zolt run app.py`
