from collections.abc import Callable
from typing import Any

from pyui.components.base import BaseComponent
from pyui.state.reactive import ReactiveVar


class List(BaseComponent):
    """
    A reactive list component that renders a list of children based on a
    reactive items variable.
    """

    component_type = "list"

    def __init__(
        self,
        items: list[Any] | ReactiveVar[list[Any]],
        render: Callable[[Any], BaseComponent] | None = None,
    ) -> None:
        super().__init__()
        self.props["items"] = items
        self.props["render_fn"] = render

    def _build_children(self) -> None:
        """Populate self.children by calling render_fn for each item."""
        items = self.props.get("items", [])
        render_fn = self.props.get("render_fn")

        if isinstance(items, ReactiveVar):
            items = items.get()

        self.children.clear()
        if render_fn and items:
            for item in items:
                child = render_fn(item)
                if child:
                    self.add(child)

    def items(self, value: list[Any] | ReactiveVar[list[Any]]) -> "List":
        self.props["items"] = value
        return self

    def render_item(self, fn: Callable[[Any], BaseComponent]) -> "List":
        self.props["render_fn"] = fn
        return self
