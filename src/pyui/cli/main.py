"""
Zolt CLI entry point.

All subcommands live under the ``zolt`` group. Run ``zolt --help`` for usage.
"""

from __future__ import annotations

import click
from rich import box
from rich.console import Console
from rich.panel import Panel

import pyui
from pyui.utils.logging import configure_logging

console = Console()


# ── Main group ────────────────────────────────────────────────────────────────


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(pyui.__version__, "-V", "--version", prog_name="Zolt")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose (DEBUG) logging.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    \b
    Zolt -- Write Python. Render anywhere.
    Web | Desktop | CLI from a single Python codebase.
    """
    configure_logging("DEBUG" if verbose else "INFO")

    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                f"[bold cyan]Zolt[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
                "[dim]Run [bold]zolt --help[/bold] to see available commands.[/dim]",
                box=box.ASCII,
                border_style="cyan",
            )
        )


# ── new ───────────────────────────────────────────────────────────────────────


@main.command("new")
@click.argument("name")
@click.option(
    "--template",
    default="blank",
    type=click.Choice(["blank", "dashboard", "landing", "admin", "auth"]),
    show_default=True,
    help="Project template to scaffold from.",
)
@click.option(
    "--target",
    default="web",
    type=click.Choice(["web", "desktop", "cli", "all"]),
    show_default=True,
    help="Default render target.",
)
def cmd_new(name: str, template: str, target: str) -> None:
    """Scaffold a new Zolt project called NAME."""
    from pyui.scaffold import create_project

    try:
        project_path = create_project(name, template=template, target=target)
        console.print(
            f"[green]✓[/green] Created [cyan]{name}[/cyan] at [dim]{project_path}[/dim]\n\n"
            f"  [dim]cd {name}[/dim]\n"
            f"  [dim]zolt run[/dim]"
        )
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None


# ── run ───────────────────────────────────────────────────────────────────────


@main.command("run")
@click.option(
    "--target",
    "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli"]),
    show_default=True,
    help="Render target.",
)
@click.option("--port", "-p", default=8000, show_default=True, help="Dev server port.")
@click.option("--host", default="localhost", show_default=True, help="Dev server host.")
@click.option(
    "--no-browser", is_flag=True, default=False, help="Do not open browser automatically."
)
@click.argument("app_file", default="app.py", required=False)
def cmd_run(target: str, port: int, host: str, no_browser: bool, app_file: str) -> None:
    """Start the Zolt dev server (APP_FILE defaults to app.py)."""
    try:
        from pyui.compiler.discovery import discover_app

        AppClass = discover_app(app_file)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] App file not found: [cyan]{app_file}[/cyan]")
        raise SystemExit(1) from None
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None

    if target == "web":
        from pyui.server.dev_server import run_dev_server

        run_dev_server(
            AppClass,
            host=host,
            port=port,
            open_browser=not no_browser,
            watch_file=app_file,
        )

    elif target == "desktop":
        console.print(f"[bold cyan]Launching desktop window for[/bold cyan] [dim]{app_file}[/dim]")
        from pyui.renderers.desktop import run_desktop_app

        run_desktop_app(AppClass)

    elif target == "cli":
        from pyui.renderers.cli import run_cli_app

        run_cli_app(AppClass)

    else:
        console.print(f"[red]Error:[/red] Unknown target: [cyan]{target}[/cyan]")
        raise SystemExit(1) from None


# ── build ─────────────────────────────────────────────────────────────────────


@main.command("build")
@click.option(
    "--target",
    "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli", "all"]),
    show_default=True,
)
@click.option("--out", default="./dist", show_default=True, help="Output directory.")
@click.argument("app_file", default="app.py", required=False)
def cmd_build(target: str, out: str, app_file: str) -> None:
    """Build a production bundle from APP_FILE."""
    try:
        from pyui.compiler.discovery import discover_app

        AppClass = discover_app(app_file)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None

    from pyui.compiler import compile_app

    try:
        output_path, stats = compile_app(AppClass, target=target, output_dir=out)
        if target == "web":
            pages = stats.get("pages", "?")
            total_kb = stats.get("total_kb", "?")
            elapsed = stats.get("elapsed_ms", "?")
            console.print(
                f"[green]Built[/green] [cyan]{app_file}[/cyan] → [cyan]{output_path}[/cyan]  "
                f"[dim]{pages} page(s) · {total_kb} KB · {elapsed}ms[/dim]"
            )
        elif target == "all":
            console.print(
                f"[green]Built[/green] [cyan]{app_file}[/cyan] → [cyan]{output_path}[/cyan]\n"
                f"  [dim]{output_path}/web/[/dim]     HTML/CSS/JS\n"
                f"  [dim]{output_path}/desktop/[/dim]  python run.py\n"
                f"  [dim]{output_path}/cli/[/dim]      python run.py"
            )
        else:
            console.print(
                f"[green]Built[/green] [cyan]{app_file}[/cyan] → [cyan]{output_path}[/cyan]\n"
                f"  Run with: [dim]python {output_path}/run.py[/dim]"
            )
    except NotImplementedError as exc:
        console.print(f"[yellow]![/yellow]  {exc}")


# ── publish ───────────────────────────────────────────────────────────────────


@main.command("publish")
@click.option("--name", default=None, help="Override package name.")
@click.option("--build-only", is_flag=True, default=False, help="Build dist/ but do not upload.")
def cmd_publish(name: str | None, build_only: bool) -> None:
    """Package and publish a Zolt component to PyPI."""
    import json
    import subprocess
    import sys
    from pathlib import Path

    manifest_path = Path("pyui.json")
    if not manifest_path.exists():
        console.print(
            "[red]Error:[/red] No [cyan]pyui.json[/cyan] found in the current directory.\n\n"
            "Create one with the following structure:\n"
            '[dim]{\n'
            '  "name": "zolt-my-component",\n'
            '  "version": "1.0.0",\n'
            '  "pyui_version": ">=1.0.0",\n'
            '  "components": ["MyComponent"],\n'
            '  "targets": ["web"],\n'
            '  "author": "Your Name",\n'
            '  "license": "MIT"\n'
            '}[/dim]'
        )
        raise SystemExit(1) from None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        console.print(f"[red]Error:[/red] Invalid pyui.json: {exc}")
        raise SystemExit(1) from None

    required_fields = ["name", "version", "components"]
    missing = [f for f in required_fields if f not in manifest]
    if missing:
        console.print(f"[red]Error:[/red] pyui.json is missing required fields: {missing}")
        raise SystemExit(1) from None

    pkg_name = name or manifest["name"]
    pkg_version = manifest["version"]

    has_pyproject = Path("pyproject.toml").exists()
    has_setup = Path("setup.py").exists()
    if not has_pyproject and not has_setup:
        console.print(
            "[red]Error:[/red] No [cyan]pyproject.toml[/cyan] or [cyan]setup.py[/cyan] found."
        )
        raise SystemExit(1) from None

    console.print(f"[bold]Publishing[/bold] [cyan]{pkg_name}[/cyan] v[dim]{pkg_version}[/dim]\n")

    console.print("[dim]Building distribution...[/dim]")
    result = subprocess.run([sys.executable, "-m", "build"], capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        console.print(f"[red]Build failed:[/red]\n{result.stderr}")
        console.print("[dim]Tip: pip install build[/dim]")
        raise SystemExit(1) from None
    console.print("[green]✓[/green] Distribution built in [dim]dist/[/dim]")

    if build_only:
        console.print("\n[dim]--build-only: skipping upload.[/dim]")
        return

    console.print("[dim]Uploading to PyPI...[/dim]")
    result = subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"], text=True)  # noqa: S603
    if result.returncode != 0:
        console.print("[red]Upload failed.[/red] [dim]Tip: pip install twine[/dim]")
        raise SystemExit(1) from None

    console.print(
        f"\n[green]✓[/green] Published [cyan]{pkg_name}[/cyan] v{pkg_version} to PyPI.\n"
        f"  Install with: [dim]pip install {pkg_name}[/dim]"
    )


# ── search ────────────────────────────────────────────────────────────────────


@main.command("search")
@click.argument("query")
def cmd_search(query: str) -> None:
    """Search PyPI for Zolt component packages matching QUERY."""
    import json as _json
    import urllib.parse
    import urllib.request

    search_term = f"zolt-{query}" if not query.startswith("zolt") else query
    url = f"https://pypi.org/pypi/{urllib.parse.quote(search_term)}/json"

    console.print(f"[dim]Searching PyPI for[/dim] [cyan]{search_term}[/cyan]...\n")

    try:
        with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310
            data = _json.loads(resp.read())
        info = data["info"]
        console.print(f"[bold cyan]{info['name']}[/bold cyan] [dim]v{info['version']}[/dim]")
        console.print(f"  {info.get('summary', 'No description.')}")
        console.print(f"  [dim]Install:[/dim] pip install {info['name']}")
    except Exception:
        console.print(
            f"[yellow]![/yellow]  Package [cyan]{search_term}[/cyan] not found on PyPI.\n"
            f"  Browse community packages at [link=https://pypi.org/search/?q=zolt-]"
            f"https://pypi.org/search/?q=zolt-[/link]"
        )


# ── doctor ────────────────────────────────────────────────────────────────────


@main.command("doctor")
def cmd_doctor() -> None:
    """Check environment health (Python version, dependencies, ports)."""
    import importlib.metadata
    import json as _json
    import platform
    import socket
    import sys
    import urllib.request

    from rich.table import Table

    console.print("[bold]Zolt Doctor[/bold]\n")

    results: list[tuple[str, str, str]] = []

    py_ver = sys.version.split()[0]
    py_ok = sys.version_info >= (3, 10)
    results.append(("Python >= 3.10", py_ver, "✓" if py_ok else "✗ upgrade required"))

    try:
        with urllib.request.urlopen(  # noqa: S310
            "https://pypi.org/pypi/zolt/json", timeout=3
        ) as r:
            latest = _json.loads(r.read())["info"]["version"]
        up_to_date = latest == pyui.__version__
        results.append((
            "Zolt version",
            f"{pyui.__version__} (latest: {latest})",
            "✓" if up_to_date else f"↑ {latest} available",
        ))
    except Exception:
        results.append(("Zeno version", pyui.__version__, "✓ (PyPI check skipped)"))

    for dep in ["click", "jinja2", "aiohttp", "watchdog", "rich", "structlog"]:
        try:
            ver = importlib.metadata.version(dep)
            results.append((f"dep: {dep}", ver, "✓"))
        except importlib.metadata.PackageNotFoundError:
            results.append((f"dep: {dep}", "NOT FOUND", "✗ pip install zolt"))

    for port in [8000, 9000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            in_use = s.connect_ex(("localhost", port)) == 0
        results.append((
            f"Port {port}",
            "in use" if in_use else "available",
            "⚠ choose another port" if in_use else "✓",
        ))

    results.append(("Platform", f"{platform.system()} {platform.release()}", "✓"))

    table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 2))
    table.add_column("Check")
    table.add_column("Value")
    table.add_column("Status")

    for check, value, status in results:
        color = "green" if status.startswith("✓") else "red" if status.startswith("✗") else "yellow"
        table.add_row(check, value, f"[{color}]{status}[/{color}]")

    console.print(table)


# ── lint ──────────────────────────────────────────────────────────────────────


@main.command("lint")
@click.argument("app_file", default="app.py", required=False)
def cmd_lint(app_file: str) -> None:
    """Lint component definitions in APP_FILE."""
    from pyui.linter import lint_app

    try:
        from pyui.compiler.discovery import discover_app
        AppClass = discover_app(app_file)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from None

    warnings = lint_app(AppClass)
    if not warnings:
        console.print(f"[green]✓[/green] No issues found in [cyan]{app_file}[/cyan]")
    else:
        for w in warnings:
            icon = "[red]✗[/red]" if w["level"] == "error" else "[yellow]⚠[/yellow]"
            console.print(f"  {icon}  {w['message']}")
        console.print(f"\n[dim]{len(warnings)} issue(s) found.[/dim]")
        raise SystemExit(1) from None


# ── storybook ─────────────────────────────────────────────────────────────────


@main.command("storybook")
@click.option("--port", "-p", default=9000, show_default=True, help="Storybook port.")
@click.option("--no-browser", is_flag=True, default=False, help="Do not open browser automatically.")
def cmd_storybook(port: int, no_browser: bool) -> None:
    """Open the component storybook (gallery)."""
    from pyui.cli.storybook import run_storybook

    console.print("[bold cyan]Opening Zolt Storybook...[/bold cyan]")
    run_storybook(port=port, open_browser=not no_browser)


# ── info ──────────────────────────────────────────────────────────────────────


@main.command("info")
def cmd_info() -> None:
    """Show Zeno version and project info."""
    console.print(
        Panel.fit(
            f"[bold cyan]Zolt[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
            "[dim]Write Python. Render anywhere.[/dim]\n\n"
            f"[dim]Docs    :[/dim] https://zolt.dev\n"
            f"[dim]GitHub  :[/dim] https://github.com/12errh/zolt\n"
            f"[dim]License :[/dim] MIT",
            box=box.ASCII,
            border_style="cyan",
        )
    )
