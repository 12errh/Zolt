"""
PyUI Example — Admin Panel (CRUD)

Run with: pyui run examples/admin/app.py
"""

from pyui import (
    Alert, App, Badge, Button, Flex, Form,
    Grid, Heading, Input, Nav, Page, Stat, Table, Text, reactive,
)

# ── In-memory store ───────────────────────────────────────────────────────────

_USERS: list[dict] = [
    {"id": 1, "name": "Alice Smith",  "email": "alice@example.com",  "role": "Admin",  "status": "Active"},
    {"id": 2, "name": "Bob Jones",    "email": "bob@example.com",    "role": "Editor", "status": "Active"},
    {"id": 3, "name": "Carol White",  "email": "carol@example.com",  "role": "Viewer", "status": "Inactive"},
    {"id": 4, "name": "Dan Brown",    "email": "dan@example.com",    "role": "Editor", "status": "Active"},
    {"id": 5, "name": "Eve Davis",    "email": "eve@example.com",    "role": "Viewer", "status": "Active"},
]
_next_id = 6

# ── Shared state ──────────────────────────────────────────────────────────────

_user_count   = reactive(len(_USERS))
_active_count = reactive(sum(1 for u in _USERS if u["status"] == "Active"))
_flash_msg    = reactive("")
_flash_type   = reactive("info")
_new_name     = reactive("")
_new_email    = reactive("")
_new_role     = reactive("Viewer")


def _delete_user(user_id: int) -> None:
    global _USERS
    _USERS = [u for u in _USERS if u["id"] != user_id]
    _user_count.set(len(_USERS))
    _active_count.set(sum(1 for u in _USERS if u["status"] == "Active"))
    _flash_msg.set(f"User #{user_id} deleted.")
    _flash_type.set("warning")


def _add_user() -> None:
    global _USERS, _next_id
    name  = _new_name.get().strip()
    email = _new_email.get().strip()
    role  = _new_role.get().strip() or "Viewer"
    if not name or not email:
        _flash_msg.set("Name and email are required.")
        _flash_type.set("danger")
        return
    _USERS.append({"id": _next_id, "name": name, "email": email, "role": role, "status": "Active"})
    _next_id += 1
    _user_count.set(len(_USERS))
    _active_count.set(sum(1 for u in _USERS if u["status"] == "Active"))
    _flash_msg.set(f"User '{name}' created.")
    _flash_type.set("success")
    _new_name.set("")
    _new_email.set("")


# ── Pages ─────────────────────────────────────────────────────────────────────


class UsersPage(Page):
    title = "Users — Admin"
    route = "/"

    def compose(self) -> None:
        Nav(items=[("Users", "/"), ("New User", "/new-user"), ("Settings", "/settings")])

        with Flex(direction="col", gap=6).className("py-8"):
            with Flex(align="center", justify="between"):
                Heading("User Management", level=1)
                Badge(lambda: str(_user_count.get()), variant="primary")

            if _flash_msg.get():
                Alert(_flash_msg.get(), variant=_flash_type.get())

            with Grid(cols=3, gap=4):
                Stat("Total Users",  lambda: str(_user_count.get()))
                Stat("Active",       lambda: str(_active_count.get()))
                Stat("Inactive",     lambda: str(_user_count.get() - _active_count.get()))

            Table(
                headers=["ID", "Name", "Email", "Role", "Status"],
                rows=[
                    [str(u["id"]), u["name"], u["email"], u["role"], u["status"]]
                    for u in _USERS
                ],
            ).striped()


class NewUserPage(Page):
    title = "New User — Admin"
    route = "/new-user"

    def compose(self) -> None:
        Nav(items=[("Users", "/"), ("New User", "/new-user")])

        with Flex(direction="col", gap=6).className("max-w-lg py-8"):
            Heading("Create New User", level=1)

            if _flash_msg.get():
                Alert(_flash_msg.get(), variant=_flash_type.get())

            with Form(title="User Details").className(
                "bg-white border border-gray-100 rounded-2xl p-6 shadow-sm"
            ):
                Input(value=_new_name,  placeholder="Full name",            label="Name")
                Input(value=_new_email, placeholder="email@example.com",    label="Email", type="email")
                Input(value=_new_role,  placeholder="Admin / Editor / Viewer", label="Role")

                with Flex(gap=3):
                    Button("Create User").style("primary").onClick(_add_user)
                    Button("Cancel").style("ghost")


class SettingsPage(Page):
    title = "Settings — Admin"
    route = "/settings"

    def compose(self) -> None:
        Nav(items=[("Users", "/"), ("New User", "/new-user"), ("Settings", "/settings")])
        with Flex(direction="col", gap=6).className("py-8"):
            Heading("Settings", level=1)
            Text("Admin panel configuration.").style("muted")
            Alert("Settings are read-only in this demo.", variant="info")


# ── App ───────────────────────────────────────────────────────────────────────


class AdminApp(App):
    name = "Admin Panel"
    theme = "light"

    user_count   = _user_count
    active_count = _active_count
    flash_msg    = _flash_msg
    flash_type   = _flash_type

    home         = UsersPage()
    new_user     = NewUserPage()
    settings     = SettingsPage()
