"""
PyUI Example — Todo App

Run with: pyui run examples/todo/app.py
"""

from pyui import App, Badge, Button, Flex, Heading, Input, Page, Text, reactive

# ── Shared state (module-level so handlers can mutate it) ─────────────────────

_todos: list[dict] = []
_count = reactive(0)
_new_text = reactive("")


def _add_todo() -> None:
    text = _new_text.get().strip()
    if text:
        _todos.append({"text": text, "done": False})
        _count.set(len(_todos))
        _new_text.set("")


def _toggle(index: int) -> None:
    if 0 <= index < len(_todos):
        _todos[index]["done"] = not _todos[index]["done"]


# ── Pages ─────────────────────────────────────────────────────────────────────


class HomePage(Page):
    title = "Todo"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", gap=6).className("max-w-lg mx-auto py-12 px-4"):
            with Flex(align="center", justify="between"):
                Heading("My Todos", level=1)
                Badge(lambda: str(_count.get()), variant="primary")

            with Flex(gap=3):
                Input(
                    value=_new_text,
                    placeholder="What needs to be done?",
                ).onChange(lambda: None)
                Button("Add").style("primary").onClick(_add_todo)

            with Flex(direction="col", gap=2):
                for i, todo in enumerate(_todos):
                    with Flex(
                        align="center", justify="between", gap=4
                    ).className(
                        "p-4 bg-white border border-gray-100 rounded-xl "
                        "shadow-sm hover:shadow-md transition-shadow"
                    ):
                        Text(todo["text"]).className(
                            "line-through text-gray-400" if todo["done"] else "text-gray-900"
                        )
                        Button("✓" if not todo["done"] else "↩").style(
                            "success" if not todo["done"] else "ghost"
                        ).size("sm").onClick(lambda idx=i: _toggle(idx))

            if not _todos:
                Text("No todos yet. Add one above!").style("muted").paragraph()


# ── App ───────────────────────────────────────────────────────────────────────


class TodoApp(App):
    name = "Todo"
    theme = "light"

    count = _count
    new_text = _new_text

    home = HomePage()
