"""
Project scaffolder — implements ``pyui new <name>``.

Creates a minimal working project directory with app.py, requirements.txt,
and README.md. The ``--template`` flag selects a richer starting point.
"""

from __future__ import annotations

from pathlib import Path

# ── Templates ─────────────────────────────────────────────────────────────────

_BLANK_APP = '''\
"""
{name} — built with PyUI.

Run with: pyui run
"""

from pyui import App, Button, Flex, Heading, Page, Text


class HomePage(Page):
    title = "{name}"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", align="center", justify="center", gap=6):
            Heading("{name}", level=1)
            Text("Welcome to your new PyUI app.").style("muted")
            Button("Get Started").style("primary").size("lg")


class {class_name}(App):
    name = "{name}"
    home = HomePage()
'''

_DASHBOARD_APP = '''\
"""
{name} — dashboard template built with PyUI.

Run with: pyui run
"""

from pyui import App, Badge, Flex, Grid, Heading, Nav, Page, Stat, Table, Text


class DashboardPage(Page):
    title = "Dashboard"
    route = "/"
    layout = "default"

    def compose(self) -> None:
        Nav(items=[("Dashboard", "/"), ("Reports", "/reports"), ("Settings", "/settings")])

        with Flex(direction="col", gap=8):
            with Flex(align="center", justify="between"):
                Heading("Dashboard", level=1)
                Badge("Live", variant="success")

            with Grid(cols=4, gap=6):
                Stat("Total Users",   "24,521", trend="+12%",  trend_up=True)
                Stat("Revenue",       "$84,200", trend="+6%",  trend_up=True)
                Stat("Active Sessions", "1,429", trend="+3%",  trend_up=True)
                Stat("Churn Rate",    "2.4%",   trend="-0.8%", trend_up=False)

            Heading("Recent Activity", level=2)
            Table(
                headers=["User", "Action", "Time", "Status"],
                rows=[
                    ["Alice Smith",  "Login",    "2 min ago",  "Success"],
                    ["Bob Jones",    "Export",   "5 min ago",  "Success"],
                    ["Carol White",  "Upload",   "12 min ago", "Pending"],
                    ["Dan Brown",    "Delete",   "1 hr ago",   "Failed"],
                ],
            ).striped()


class ReportsPage(Page):
    title = "Reports"
    route = "/reports"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Reports", level=1)
            Text("Report content goes here.").style("muted")


class SettingsPage(Page):
    title = "Settings"
    route = "/settings"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Settings", level=1)
            Text("Settings content goes here.").style("muted")


class {class_name}(App):
    name = "{name}"
    home = DashboardPage()
    reports = ReportsPage()
    settings = SettingsPage()
'''

_REQUIREMENTS = """\
pyui-framework>=0.1.0
"""

_README = """\
# {name}

Built with [PyUI](https://github.com/12errh/pyui).

## Getting started

```bash
pip install pyui-framework
pyui run
```

## Commands

```bash
pyui run              # Start dev server
pyui run --target desktop  # Open as desktop app
pyui run --target cli      # Render in terminal
pyui build            # Build for production
```
"""

_TEMPLATES: dict[str, str] = {
    "blank": _BLANK_APP,
    "dashboard": _DASHBOARD_APP,
    # landing / admin / auth use blank as base for now
    "landing": _BLANK_APP,
    "admin": _DASHBOARD_APP,
    "auth": _BLANK_APP,
}


def _to_class_name(name: str) -> str:
    """Convert a project name like 'my-app' to a class name like 'MyApp'."""
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_")) + "App"


def create_project(name: str, template: str = "blank", target: str = "web") -> Path:
    """
    Scaffold a new PyUI project in a directory called *name*.

    Parameters
    ----------
    name : str
        Project name (also used as the directory name).
    template : str
        One of ``"blank"``, ``"dashboard"``, ``"landing"``, ``"admin"``, ``"auth"``.
    target : str
        Default render target (informational only — written to README).

    Returns
    -------
    Path
        The created project directory.

    Raises
    ------
    FileExistsError
        If the directory already exists.
    """
    project_dir = Path(name)
    if project_dir.exists():
        raise FileExistsError(
            f"Directory '{name}' already exists. "
            "Choose a different name or remove the existing directory."
        )

    project_dir.mkdir(parents=True)

    class_name = _to_class_name(name)
    app_template = _TEMPLATES.get(template, _BLANK_APP)

    (project_dir / "app.py").write_text(
        app_template.format(name=name, class_name=class_name),
        encoding="utf-8",
    )
    (project_dir / "requirements.txt").write_text(_REQUIREMENTS, encoding="utf-8")
    (project_dir / "README.md").write_text(
        _README.format(name=name, target=target),
        encoding="utf-8",
    )

    return project_dir
