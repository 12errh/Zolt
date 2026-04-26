"""
PyUI Example — Blog / Content Site

Run with: pyui run examples/blog/app.py
"""

from pyui import App, Badge, Button, Container, Flex, Grid, Heading, Nav, Page, Text

_POSTS = [
    {
        "slug": "getting-started",
        "title": "Getting Started with PyUI",
        "date": "April 2026",
        "tag": "Tutorial",
        "excerpt": "Learn how to build your first PyUI app in under 10 minutes.",
        "content": """
PyUI lets you build production-grade UIs in pure Python.

## Installation

```bash
pip install pyui-framework
pyui new my-app
pyui run
```

## Your first component

```python
from pyui import App, Page, Heading, Text

class MyApp(App):
    home = Page(title="Home", route="/")
    home.add(
        Heading("Hello, World!"),
        Text("Built with PyUI."),
    )
```

That's it. Save the file and your browser updates instantly.
        """,
    },
    {
        "slug": "reactive-state",
        "title": "Reactive State in PyUI",
        "date": "April 2026",
        "tag": "Deep Dive",
        "excerpt": "How PyUI's reactive system works under the hood.",
        "content": """
PyUI's state system is built around `ReactiveVar` — an observable value
that notifies subscribers when it changes.

## Basic usage

```python
from pyui import reactive

count = reactive(0)
count.set(1)   # notifies all subscribers
count.get()    # → 1
```

## In a component

```python
class Counter(App):
    count = reactive(0)
    home = Page(route="/")
    home.add(
        Text(lambda: f"Count: {Counter.count.get()}"),
        Button("Increment").onClick(
            lambda: Counter.count.set(Counter.count.get() + 1)
        ),
    )
```
        """,
    },
    {
        "slug": "themes",
        "title": "Theming Your PyUI App",
        "date": "April 2026",
        "tag": "Design",
        "excerpt": "Switch between 6 built-in themes or create your own.",
        "content": """
PyUI ships with 6 built-in themes: light, dark, ocean, sunset, forest, rose.

## Switching themes

```python
class MyApp(App):
    theme = "dark"   # or "ocean", "sunset", "forest", "rose"
```

## Custom theme

```python
class MyApp(App):
    theme = {
        "color.primary": "#FF6B6B",
        "color.background": "#FFF5F5",
    }
```

Any token not overridden inherits from the default light theme.
        """,
    },
]


class HomePage(Page):
    title = "PyUI Blog"
    route = "/"

    def compose(self) -> None:
        Nav(items=[("Blog", "/"), ("About", "/about")])
        with Container(size="xl"):
            with Flex(direction="col", gap=4).className("py-12 text-center"):
                Heading("PyUI Blog", level=1)
                Text("Tutorials, deep dives, and updates from the PyUI team.").style("muted")

            with Grid(cols=3, gap=6):
                for post in _POSTS:
                    with Flex(direction="col", gap=3).className(
                        "bg-white border border-gray-100 rounded-2xl p-6 "
                        "shadow-sm hover:shadow-md transition-shadow"
                    ):
                        Badge(post["tag"], variant="secondary")
                        Heading(post["title"], level=3)
                        Text(post["excerpt"]).style("muted").paragraph()
                        with Flex(align="center", justify="between"):
                            Text(post["date"]).style("muted")
                            Button("Read more →").style("link")


class AboutPage(Page):
    title = "About — PyUI Blog"
    route = "/about"

    def compose(self) -> None:
        Nav(items=[("Blog", "/"), ("About", "/about")])
        with Container(size="md"):
            with Flex(direction="col", gap=6).className("py-12"):
                Heading("About PyUI", level=1)
                Text(
                    "PyUI is an open-source Python framework for building "
                    "production-grade UIs without HTML, CSS, or JavaScript."
                ).paragraph()
                Text(
                    "Write once, render anywhere — web, desktop, and terminal "
                    "from a single Python codebase."
                ).paragraph()
                Button("View on GitHub").style("primary").icon("github")


class BlogApp(App):
    name = "PyUI Blog"
    description = "A PyUI blog example."
    theme = "light"

    home = HomePage()
    about = AboutPage()
