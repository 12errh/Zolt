from pyui.components.base import BaseComponent
from pyui.state.reactive import ReactiveVar


class Textarea(BaseComponent):
    """
    Multi-line text input.
    """

    component_type = "textarea"

    def __init__(
        self,
        value: str | ReactiveVar[str] = "",
        placeholder: str = "",
        rows: int = 4,
        label: str | None = None,
    ) -> None:
        super().__init__()
        self.props.update(
            {
                "value": value,
                "placeholder": placeholder,
                "rows": rows,
                "label": label,
            }
        )

    def rows(self, value: int) -> "Textarea":
        self.props["rows"] = value
        return self
