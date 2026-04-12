from pyui.components.base import BaseComponent
from pyui.state.reactive import ReactiveVar


class Checkbox(BaseComponent):
    """
    Standard checkbox input.
    """

    component_type = "checkbox"

    def __init__(self, checked: bool | ReactiveVar[bool] = False, label: str | None = None) -> None:
        super().__init__()
        self.props.update(
            {
                "checked": checked,
                "label": label,
            }
        )

    def checked(self, value: bool = True) -> "Checkbox":
        self.props["checked"] = value
        return self
