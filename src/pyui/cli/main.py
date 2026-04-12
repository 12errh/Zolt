"""
PyUI CLI entry point.

All subcommands live under the ``pyui`` group. Run ``pyui --help`` for usage.
"""

from __future__ import annotations

import click
from rich.console import Console
from rich.panel import Panel
from rich import box

import pyui
from pyui.utils.logging import configure_logging

console = Console()


# ── Main group ────────────────────────────────────────────────────────────────

@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(pyui.__version__, "-V", "--version", prog_name="PyUI")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose (DEBUG) logging.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    \b
    PyUI — Write Python. Render anywhere.
    Web | Desktop | CLI from a single Python codebase.
    """
    configure_logging("DEBUG" if verbose else "INFO")

    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                f"[bold cyan]PyUI[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
                "[dim]Run [bold]pyui --help[/bold] to see available commands.[/dim]",
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
    """Scaffold a new PyUI project called NAME."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui new[/bold] is not yet implemented "
        f"(Phase 0 stub). Project name: [cyan]{name}[/cyan], "
        f"template: [cyan]{template}[/cyan], target: [cyan]{target}[/cyan]."
    )


# ── run ───────────────────────────────────────────────────────────────────────

@main.command("run")
@click.option(
    "--target", "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli"]),
    show_default=True,
    help="Render target.",
)
@click.option("--port", "-p", default=8000, show_default=True, help="Dev server port.")
@click.option("--host", default="localhost", show_default=True, help="Dev server host.")
@click.argument("app_file", default="app.py", required=False)
def cmd_run(target: str, port: int, host: str, app_file: str) -> None:
    """Start the PyUI dev server (APP_FILE defaults to app.py)."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui run[/bold] is not yet implemented "
        f"(Phase 1). "
        f"Would run [cyan]{app_file}[/cyan] -> [cyan]{target}[/cyan] "
        f"on [cyan]{host}:{port}[/cyan]."
    )


# ── build ─────────────────────────────────────────────────────────────────────

@main.command("build")
@click.option(
    "--target", "-t",
    default="web",
    type=click.Choice(["web", "desktop", "cli", "all"]),
    show_default=True,
)
@click.option("--out", default="./dist", show_default=True, help="Output directory.")
@click.argument("app_file", default="app.py", required=False)
def cmd_build(target: str, out: str, app_file: str) -> None:
    """Build a production bundle from APP_FILE."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui build[/bold] is not yet implemented (Phase 1). "
        f"Would build [cyan]{app_file}[/cyan] -> [cyan]{target}[/cyan] -> [cyan]{out}[/cyan]."
    )


# ── publish ───────────────────────────────────────────────────────────────────

@main.command("publish")
@click.option("--name", default=None, help="Override package name.")
def cmd_publish(name: str | None) -> None:
    """Publish a component package to the PyUI marketplace."""
    console.print(
        "[yellow]![/yellow]  [bold]pyui publish[/bold] is not yet implemented (Phase 5)."
    )


# ── doctor ────────────────────────────────────────────────────────────────────

@main.command("doctor")
def cmd_doctor() -> None:
    """Check environment health (Python version, dependencies, ports)."""
    import sys
    import platform

    console.print("[bold]PyUI Doctor[/bold]\n")
    console.print(f"  Python   : [cyan]{sys.version.split()[0]}[/cyan]")
    console.print(f"  Platform : [cyan]{platform.system()} {platform.release()}[/cyan]")
    console.print(f"  PyUI     : [cyan]{pyui.__version__}[/cyan]")

    py_ok = sys.version_info >= (3, 10)
    status = "[green]OK[/green]" if py_ok else "[red]FAIL -- upgrade to Python 3.10+[/red]"
    console.print(f"  Python >= 3.10 : {status}")
    console.print(
        "\n[dim]Full dependency checks will be added in Phase 6.[/dim]"
    )


# ── lint ──────────────────────────────────────────────────────────────────────

@main.command("lint")
@click.argument("app_file", default="app.py", required=False)
def cmd_lint(app_file: str) -> None:
    """Lint component definitions in APP_FILE."""
    console.print(
        f"[yellow]![/yellow]  [bold]pyui lint[/bold] is not yet implemented (Phase 6). "
        f"Would lint [cyan]{app_file}[/cyan]."
    )


# ── info ──────────────────────────────────────────────────────────────────────

@main.command("info")
def cmd_info() -> None:
    """Show PyUI version and project info."""
    console.print(
        Panel.fit(
            f"[bold cyan]PyUI Framework[/bold cyan] [dim]v{pyui.__version__}[/dim]\n"
            "[dim]Write Python. Render anywhere.[/dim]\n\n"
            f"[dim]Docs    :[/dim] https://pyui.dev\n"
            f"[dim]GitHub  :[/dim] https://github.com/pyui-framework/pyui\n"
            f"[dim]License :[/dim] MIT",
            box=box.ASCII,
            border_style="cyan",
        )
    )
