from pyui import (
    Alert,
    App,
    Avatar,
    Badge,
    Breadcrumb,
    Button,
    Chart,
    Checkbox,
    Container,
    DatePicker,
    Divider,
    Drawer,
    FilePicker,
    Flex,
    Form,
    Grid,
    Heading,
    Icon,
    Input,
    Markdown,
    Menu,
    Modal,
    Nav,
    Pagination,
    Page,
    Progress,
    Select,
    Skeleton,
    Slider,
    Spacer,
    Spinner,
    Stack,
    Stat,
    Table,
    Tag,
    Text,
    Toggle,
    Tooltip,
)


class StorybookPage(Page):
    title = "PyUI Storybook — Component Gallery"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="row", align="start", gap=0).className(
            "min-h-screen bg-gray-50"
        ):
            self._sidebar()
            self._main()

    # =========================================================
    # SIDEBAR
    # =========================================================
    def _sidebar(self) -> None:
        with Flex(direction="col", align="start", gap=0).className(
            "w-64 flex-shrink-0 bg-white border-r border-gray-100 "
            "min-h-screen sticky top-0 overflow-y-auto"
        ):
            # Logo bar
            with Flex(align="center", gap=3).className(
                "px-5 py-5 border-b border-gray-100"
            ):
                with Flex(align="center", justify="center").className(
                    "w-8 h-8 bg-gray-950 rounded-lg flex-shrink-0"
                ):
                    Icon("code-2", size=14).className("text-white")
                with Flex(direction="col", gap=0):
                    Text("PyUI").className(
                        "text-sm font-bold text-gray-950 tracking-tight leading-none"
                    )
                    Text("Storybook").className(
                        "text-[10px] text-gray-400 uppercase tracking-widest"
                    )

            self._nav_group("Foundation")
            self._nav_link("zap",          "Typography",     "#typography")
            self._nav_link("tag",          "Badges + Tags",  "#badges")
            self._nav_link("user-circle",  "Avatars + Icons","#avatars")

            self._nav_group("Inputs")
            self._nav_link("mouse-pointer-click", "Buttons",     "#buttons")
            self._nav_link("text-cursor-input",   "Text Inputs", "#inputs")
            self._nav_link("sliders",             "Controls",    "#controls")
            self._nav_link("file-text",           "Forms",       "#forms")

            self._nav_group("Feedback")
            self._nav_link("alert-circle", "Alerts",        "#alerts")
            self._nav_link("layers",       "Modal + Drawer","#overlays")
            self._nav_link("loader",       "Loading States","#loading")

            self._nav_group("Navigation")
            self._nav_link("navigation",   "Nav + Tabs",  "#nav")
            self._nav_link("arrow-left-right", "Pagination", "#pagination")
            self._nav_link("list",         "Menu",        "#menu")

            self._nav_group("Data")
            self._nav_link("bar-chart-2",  "Stats",  "#stats")
            self._nav_link("table",        "Tables", "#tables")
            self._nav_link("activity",     "Charts", "#charts")

    def _nav_group(self, label: str) -> None:
        Text(label).className(
            "block px-5 pt-5 pb-1 text-[10px] font-semibold "
            "uppercase tracking-widest text-gray-400"
        )

    def _nav_link(self, icon: str, label: str, href: str) -> None:
        with Flex(align="center", gap=2).className(
            "px-5 py-2 text-sm font-medium text-gray-500 "
            "hover:text-gray-900 hover:bg-gray-50 cursor-pointer "
            "transition-colors duration-100"
        ):
            Icon(icon, size=14)
            Text(label).className("text-[13px]")

    # =========================================================
    # MAIN AREA
    # =========================================================
    def _main(self) -> None:
        with Flex(direction="col", gap=0).className(
            "flex-1 min-w-0 px-10 py-10 pb-24"
        ):
            # Page header
            with Flex(direction="col", gap=2).className("mb-12"):
                with Flex(align="center", gap=2).className("mb-1"):
                    Badge("v0.1.0", variant="dark")
                    Badge("42+ Components", variant="secondary")
                Heading("Component Gallery", level=1)
                Text(
                    "Every PyUI component, live and interactive. "
                    "Built entirely with pure Python."
                ).style("lead").paragraph()

            self._section_typography()
            self._section_badges()
            self._section_avatars()
            self._section_buttons()
            self._section_inputs()
            self._section_controls()
            self._section_forms()
            self._section_alerts()
            self._section_overlays()
            self._section_loading()
            self._section_nav()
            self._section_pagination()
            self._section_menu()
            self._section_stats()
            self._section_tables()
            self._section_charts()

    # =========================================================
    # SHARED HELPERS
    # =========================================================
    def _section_header(self, title: str, desc: str, anchor: str = "") -> None:
        with Flex(direction="col", gap=1).className("mb-6 mt-14 first:mt-0"):
            Heading(title, level=2)
            Text(desc).style("muted").paragraph()
            Divider()

    def _card(self, label: str, hint: str = "") -> Flex:
        """Outer preview card — use as context manager."""
        card = Flex(direction="col", gap=0).className(
            "bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-md "
            "transition-shadow duration-200"
        )
        with card:
            with Flex(align="center", justify="between").className(
                "px-5 py-3 border-b border-gray-100"
            ):
                Text(label).className(
                    "text-xs font-semibold text-gray-700 tracking-tight"
                )
                if hint:
                    Badge(hint, variant="secondary")
        return card

    def _preview(self, dark: bool = False, col: bool = False) -> Flex:
        bg = "bg-gray-950" if dark else "bg-[#f8f9fa]"
        direction = "col" if col else "row"
        return Flex(
            direction=direction, align="center", justify="center",
            gap=3, wrap=True
        ).className(f"{bg} px-8 py-10 min-h-[120px]")

    # =========================================================
    # SECTION: TYPOGRAPHY
    # =========================================================
    def _section_typography(self) -> None:
        self._section_header(
            "Typography",
            "Headings, text variants, and the full typographic scale.",
            "typography",
        )
        with Grid(cols=2, gap=5):
            # Headings card
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Headings").className("text-xs font-semibold text-gray-700")
                    Badge("h1 – h4", variant="secondary")
                with Flex(direction="col", gap=3).className("px-6 py-6"):
                    Heading("Display Heading", level=1)
                    Heading("Section Heading", level=2)
                    Heading("Card Title", level=3)
                    Heading("Subsection", level=4)

            # Text variants card
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Text Variants").className("text-xs font-semibold text-gray-700")
                    Badge("6 variants", variant="secondary")
                with Flex(direction="col", gap=3).className("px-6 py-6"):
                    Text("Default — primary body text").paragraph()
                    Text("Lead — intro paragraph, slightly larger").style("lead").paragraph()
                    Text("Muted — secondary, supporting copy").style("muted").paragraph()
                    Text("Small — captions and metadata").style("small").paragraph()
                    Text("Success — positive confirmation").style("success").paragraph()
                    Text("Error — validation and warnings").style("error").paragraph()

        # Gradient heading full-width
        with Flex(direction="col", gap=0).className(
            "mt-5 bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        ):
            with Flex(align="center", justify="between").className(
                "px-5 py-3 border-b border-gray-100"
            ):
                Text("Heading Variants").className("text-xs font-semibold text-gray-700")
            with Flex(direction="col", gap=4).className("px-6 py-6"):
                Heading("Gradient Heading", level=2).style("gradient")
                Heading("Display Heading", level=2).style("display")
                Heading("Muted Heading", level=2).style("muted")
                Heading("Mono Heading", level=2).style("mono")

    # =========================================================
    # SECTION: BADGES + TAGS
    # =========================================================
    def _section_badges(self) -> None:
        self._section_header(
            "Badges + Tags",
            "Status indicators, labels, and categorization chips.",
            "badges",
        )
        with Grid(cols=2, gap=5):
            # Badges
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Badge").className("text-xs font-semibold text-gray-700")
                    Badge("7 variants", variant="secondary")
                with Flex(align="center", gap=2, wrap=True).className("px-6 py-6"):
                    Badge("Primary",   variant="primary")
                    Badge("Secondary", variant="secondary")
                    Badge("Success",   variant="success")
                    Badge("Danger",    variant="danger")
                    Badge("Warning",   variant="warning")
                    Badge("Info",      variant="info")
                    Badge("Dark",      variant="dark")

            # Tags
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Tag").className("text-xs font-semibold text-gray-700")
                    Badge("4 variants", variant="secondary")
                with Flex(align="center", gap=2, wrap=True).className("px-6 py-6"):
                    Tag("Design",    variant="primary")
                    Tag("Frontend",  variant="secondary")
                    Tag("Shipped",   variant="success")
                    Tag("Blocked",   variant="danger")
                    Tag("Closable",  variant="secondary").closable()

    # =========================================================
    # SECTION: AVATARS + ICONS
    # =========================================================
    def _section_avatars(self) -> None:
        self._section_header(
            "Avatars + Icons",
            "User representations and the full Lucide icon set.",
            "avatars",
        )
        with Grid(cols=2, gap=5):
            # Avatars
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Avatar").className("text-xs font-semibold text-gray-700")
                    Badge("6 sizes", variant="secondary")
                with Flex(align="center", gap=4).className("px-6 py-6"):
                    Avatar(name="Alice Smith",  size="xs")
                    Avatar(name="Bob Jones",    size="sm")
                    Avatar(name="Carol White",  size="md")
                    Avatar(name="Dan Brown",    size="lg")
                    Avatar(
                        src="https://i.pravatar.cc/150?img=3",
                        name="Eve",
                        size="xl",
                    )

            # Icons
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Icon").className("text-xs font-semibold text-gray-700")
                    Badge("Lucide", variant="secondary")
                with Flex(align="center", gap=5, wrap=True).className("px-6 py-6"):
                    Icon("zap",          size=20)
                    Icon("layers",       size=20)
                    Icon("cpu",          size=20)
                    Icon("globe",        size=20)
                    Icon("shield-check", size=20)
                    Icon("rocket",       size=20)
                    Icon("sparkles",     size=20)
                    Icon("terminal",     size=20)
                    Icon("git-branch",   size=20)
                    Icon("package",      size=20)

    # =========================================================
    # SECTION: BUTTONS
    # =========================================================
    def _section_buttons(self) -> None:
        self._section_header(
            "Buttons",
            "Every variant, size, and state — the primary action primitive.",
            "buttons",
        )
        with Grid(cols=1, gap=5):
            # Variants
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Variants").className("text-xs font-semibold text-gray-700")
                    Badge("7 variants", variant="secondary")
                with Flex(align="center", gap=3, wrap=True).className("px-6 py-6"):
                    Button("Primary").style("primary")
                    Button("Secondary").style("secondary")
                    Button("Ghost").style("ghost")
                    Button("Danger").style("danger")
                    Button("Success").style("success")
                    Button("Gradient").style("gradient")
                    Button("Link").style("link")

            # Sizes
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Sizes").className("text-xs font-semibold text-gray-700")
                    Badge("xs → xl", variant="secondary")
                with Flex(align="center", gap=3, wrap=True).className("px-6 py-6"):
                    Button("XSmall").style("primary").size("xs")
                    Button("Small").style("primary").size("sm")
                    Button("Medium").style("primary").size("md")
                    Button("Large").style("primary").size("lg")
                    Button("XLarge").style("primary").size("xl")

            # States
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("States").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", gap=3, wrap=True).className("px-6 py-6"):
                    Button("Default").style("primary")
                    Button("Loading").style("primary").loading(True)
                    Button("Disabled").style("primary").disabled(True)
                    Button("With Icon").style("ghost").icon("zap")
                    Button("Icon Right").style("secondary").icon("arrow-right", "right")

    # =========================================================
    # SECTION: TEXT INPUTS
    # =========================================================
    def _section_inputs(self) -> None:
        self._section_header(
            "Text Inputs",
            "Input, Textarea, Select, and DatePicker — all form field primitives.",
            "inputs",
        )
        with Grid(cols=2, gap=5):
            # Input variants
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Input").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=4).className("px-6 py-6"):
                    Input(placeholder="Default input", label="Username")
                    Input(type="email",    placeholder="you@example.com", label="Email")
                    Input(type="password", placeholder="Password",        label="Password")
                    Input(placeholder="Search...", label="Search")

            # Textarea + Select
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Textarea + Select").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=4).className("px-6 py-6"):
                    from pyui.components.input.textarea import Textarea
                    Textarea(placeholder="Write something...", label="Bio", rows=3)
                    Select(
                        options=[
                            ("us", "United States"),
                            ("uk", "United Kingdom"),
                            ("de", "Germany"),
                            ("jp", "Japan"),
                        ],
                        label="Country",
                    )
                    DatePicker(label="Date of Birth")
                    FilePicker(label="Upload Resume")

    # =========================================================
    # SECTION: CONTROLS
    # =========================================================
    def _section_controls(self) -> None:
        self._section_header(
            "Controls",
            "Checkbox, Toggle, Radio, and Slider — binary and range inputs.",
            "controls",
        )
        with Grid(cols=2, gap=5):
            # Checkbox + Toggle
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Checkbox + Toggle").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=5).className("px-6 py-6"):
                    with Flex(direction="col", gap=3):
                        Checkbox(label="Accept terms and conditions")
                        Checkbox(label="Subscribe to newsletter", checked=True)
                        Checkbox(label="Disabled option").disabled(True)
                    Divider()
                    with Flex(direction="col", gap=3):
                        Toggle(label="Enable notifications")
                        Toggle(label="Dark mode", checked=True)
                        Toggle(label="Auto-save", checked=True)

            # Slider
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Slider").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=6).className("px-6 py-6"):
                    Slider(label="Volume", value=60)
                    Slider(label="Brightness", value=80)
                    Slider(label="Opacity", value=40)
                    Slider(label="Scale", value=20)

    # =========================================================
    # SECTION: FORMS
    # =========================================================
    def _section_forms(self) -> None:
        self._section_header(
            "Forms",
            "The Form component — a structured container for all input fields.",
            "forms",
        )
        with Grid(cols=2, gap=5):
            # Sign-up form
            with Form(title="Create Account"):
                Input(placeholder="John Doe",        label="Full Name")
                Input(type="email", placeholder="you@example.com", label="Email")
                Input(type="password", placeholder="Min 8 characters", label="Password")
                Select(
                    options=[("dev", "Developer"), ("design", "Designer"), ("pm", "Product Manager")],
                    label="Role",
                )
                Checkbox(label="I agree to the Terms of Service")
                Button("Create Account").style("primary")

            # Contact form
            with Form(title="Contact Us"):
                Input(placeholder="Your name",    label="Name")
                Input(type="email", placeholder="your@email.com", label="Email")
                Select(
                    options=[("bug", "Bug Report"), ("feature", "Feature Request"), ("other", "Other")],
                    label="Subject",
                )
                from pyui.components.input.textarea import Textarea
                Textarea(placeholder="Describe your issue...", label="Message", rows=4)
                Toggle(label="Send me a copy")
                Button("Send Message").style("primary")

    # =========================================================
    # SECTION: ALERTS
    # =========================================================
    def _section_alerts(self) -> None:
        self._section_header(
            "Alerts",
            "Inline status messages with left-accent border design.",
            "alerts",
        )
        with Flex(direction="col", gap=4):
            Alert(
                "Information",
                "This is an informational message. Use it for neutral updates.",
                variant="info",
            )
            Alert(
                "Success",
                "Your changes have been saved successfully.",
                variant="success",
            )
            Alert(
                "Warning",
                "Your trial expires in 3 days. Upgrade to keep access.",
                variant="warning",
            )
            Alert(
                "Error",
                "Failed to connect to the server. Please try again.",
                variant="danger",
            )

    # =========================================================
    # SECTION: OVERLAYS (Modal + Drawer + Tooltip + Toast)
    # =========================================================
    def _section_overlays(self) -> None:
        self._section_header(
            "Modal + Drawer + Tooltip",
            "Overlay components for focused interactions.",
            "overlays",
        )
        with Grid(cols=2, gap=5):
            # Modal preview
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Modal").className("text-xs font-semibold text-gray-700")
                    Badge("Alpine.js", variant="secondary")
                with Flex(direction="col", gap=4).className("px-6 py-6"):
                    Text(
                        "Modals use Alpine.js for open/close state. "
                        "Click the button to trigger."
                    ).style("muted").paragraph()
                    with Modal(title="Confirm Action", open=False):
                        Text("Are you sure you want to delete this item? "
                             "This action cannot be undone.").paragraph()
                    Button("Open Modal").style("primary")

            # Drawer preview
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Drawer").className("text-xs font-semibold text-gray-700")
                    Badge("side=right", variant="secondary")
                with Flex(direction="col", gap=4).className("px-6 py-6"):
                    Text(
                        "Drawers slide in from the side. "
                        "Useful for settings panels and detail views."
                    ).style("muted").paragraph()
                    with Drawer(title="Settings", open=False, side="right"):
                        Text("Drawer content goes here.").paragraph()
                    Button("Open Drawer").style("ghost")

        # Tooltip
        with Flex(direction="col", gap=0).className(
            "mt-5 bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        ):
            with Flex(align="center", justify="between").className(
                "px-5 py-3 border-b border-gray-100"
            ):
                Text("Tooltip").className("text-xs font-semibold text-gray-700")
                Badge("hover", variant="secondary")
            with Flex(align="center", gap=6).className("px-6 py-6"):
                with Tooltip("This is a helpful tooltip"):
                    Button("Hover me").style("ghost")
                with Tooltip("Saved to clipboard!"):
                    Button("Copy code").style("secondary").icon("copy")
                with Tooltip("Opens in new tab"):
                    Button("Documentation").style("link").icon("external-link", "right")

    # =========================================================
    # SECTION: LOADING STATES
    # =========================================================
    def _section_loading(self) -> None:
        self._section_header(
            "Loading States",
            "Spinner, Progress bar, and Skeleton for async content.",
            "loading",
        )
        with Grid(cols=3, gap=5):
            # Spinner
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Spinner").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", justify="center", gap=6).className("px-6 py-8"):
                    Spinner(size="xs")
                    Spinner(size="sm")
                    Spinner(size="md")
                    Spinner(size="lg")
                    Spinner(size="xl")

            # Progress
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Progress").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=5).className("px-6 py-6"):
                    with Flex(direction="col", gap=1):
                        with Flex(align="center", justify="between"):
                            Text("Uploading...").style("small")
                            Text("25%").style("small")
                        Progress(value=25)
                    with Flex(direction="col", gap=1):
                        with Flex(align="center", justify="between"):
                            Text("Processing").style("small")
                            Text("60%").style("small")
                        Progress(value=60)
                    with Flex(direction="col", gap=1):
                        with Flex(align="center", justify="between"):
                            Text("Complete").style("small")
                            Text("100%").style("small")
                        Progress(value=100)

            # Skeleton
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Skeleton").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=4).className("px-6 py-6"):
                    # Fake user card skeleton
                    with Flex(align="center", gap=3):
                        Skeleton(variant="circle").className("w-10 h-10 flex-shrink-0")
                        with Flex(direction="col", gap=2).className("flex-1"):
                            Skeleton().className("h-3 w-3/4")
                            Skeleton().className("h-3 w-1/2")
                    Skeleton(variant="rect").className("h-24 w-full")
                    with Flex(direction="col", gap=2):
                        Skeleton().className("h-3 w-full")
                        Skeleton().className("h-3 w-5/6")
                        Skeleton().className("h-3 w-4/6")

    # =========================================================
    # SECTION: NAV + TABS + BREADCRUMB
    # =========================================================
    def _section_nav(self) -> None:
        self._section_header(
            "Nav + Tabs + Breadcrumb",
            "Navigation primitives for routing and content switching.",
            "nav",
        )
        with Flex(direction="col", gap=5):
            # Nav
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Nav").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", justify="between").className("px-6 py-5"):
                    Nav(items=[
                        ("Home",     "/"),
                        ("Products", "/products"),
                        ("Pricing",  "/pricing"),
                        ("Docs",     "/docs"),
                        ("Blog",     "/blog"),
                    ])
                    Button("Sign In").style("ghost").size("sm")

            # Tabs
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Tabs").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=0).className("px-6 py-5"):
                    from pyui.components.navigation.tabs import Tabs
                    Tabs(active_tab="Overview").add_tab(
                        "Overview",
                        Text("Overview content — summary and key metrics.").paragraph(),
                    ).add_tab(
                        "Analytics",
                        Text("Analytics content — charts and data.").paragraph(),
                    ).add_tab(
                        "Settings",
                        Text("Settings content — configuration options.").paragraph(),
                    )

            # Breadcrumb
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Breadcrumb").className("text-xs font-semibold text-gray-700")
                with Flex(direction="col", gap=3).className("px-6 py-5"):
                    Breadcrumb(items=[
                        ("Home", "/"),
                        ("Components", "/components"),
                        ("Navigation", "/components/navigation"),
                    ])
                    Breadcrumb(items=[
                        ("Dashboard", "/"),
                        ("Projects", "/projects"),
                        ("PyUI", "/projects/pyui"),
                        ("Settings", "/projects/pyui/settings"),
                    ])

    # =========================================================
    # SECTION: PAGINATION
    # =========================================================
    def _section_pagination(self) -> None:
        self._section_header(
            "Pagination",
            "Page controls for navigating large datasets.",
            "pagination",
        )
        with Flex(direction="col", gap=0).className(
            "bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        ):
            with Flex(align="center", justify="between").className(
                "px-5 py-3 border-b border-gray-100"
            ):
                Text("Pagination").className("text-xs font-semibold text-gray-700")
            with Flex(direction="col", gap=6).className("px-6 py-6"):
                Pagination(current=1, total=10)
                Pagination(current=5, total=10)
                Pagination(current=10, total=10)

    # =========================================================
    # SECTION: MENU
    # =========================================================
    def _section_menu(self) -> None:
        self._section_header(
            "Menu",
            "Contextual dropdown menus for actions and navigation.",
            "menu",
        )
        with Grid(cols=3, gap=5):
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Actions Menu").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", justify="center").className("px-6 py-6"):
                    Menu(items=[
                        ("Edit",      "/edit"),
                        ("Duplicate", "/duplicate"),
                        ("Archive",   "/archive"),
                        ("Delete",    "/delete"),
                    ])

            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("User Menu").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", justify="center").className("px-6 py-6"):
                    Menu(items=[
                        ("Profile",      "/profile"),
                        ("Settings",     "/settings"),
                        ("Billing",      "/billing"),
                        ("Sign Out",     "/logout"),
                    ])

            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("View Menu").className("text-xs font-semibold text-gray-700")
                with Flex(align="center", justify="center").className("px-6 py-6"):
                    Menu(items=[
                        ("List View",  "/list"),
                        ("Grid View",  "/grid"),
                        ("Board View", "/board"),
                        ("Calendar",   "/calendar"),
                    ])

    # =========================================================
    # SECTION: STATS
    # =========================================================
    def _section_stats(self) -> None:
        self._section_header(
            "Stats",
            "Key metric cards with trend indicators.",
            "stats",
        )
        with Grid(cols=4, gap=4):
            Stat("Total Users",    "24,521",  trend="+18.2%", trend_up=True)
            Stat("Monthly Revenue","$84.2k",  trend="+6.1%",  trend_up=True)
            Stat("Churn Rate",     "2.4%",    trend="-0.8%",  trend_up=False)
            Stat("Uptime",         "99.98%",  trend="+0.01%", trend_up=True)

        with Grid(cols=3, gap=4).className("mt-4"):
            Stat("Active Sessions", "1,204",  trend="+42",    trend_up=True)
            Stat("Avg. Response",   "142ms",  trend="-18ms",  trend_up=True)
            Stat("Error Rate",      "0.03%",  trend="-0.01%", trend_up=True)

    # =========================================================
    # SECTION: TABLES
    # =========================================================
    def _section_tables(self) -> None:
        self._section_header(
            "Tables",
            "Structured data grids with striped rows and hover states.",
            "tables",
        )
        with Flex(direction="col", gap=5):
            # Default table
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Default Table").className("text-xs font-semibold text-gray-700")
                    Badge("5 rows", variant="secondary")
                with Flex(direction="col", gap=0).className("overflow-x-auto"):
                    Table(
                        headers=["Name", "Role", "Team", "Status", "Joined"],
                        rows=[
                            ["Alice Chen",    "Engineer",   "Platform",  "Active",    "Jan 2023"],
                            ["Bob Martinez",  "Designer",   "Product",   "Active",    "Mar 2023"],
                            ["Carol White",   "PM",         "Growth",    "Away",      "Jun 2022"],
                            ["Dan Kim",       "Engineer",   "Frontend",  "Active",    "Sep 2023"],
                            ["Eve Johnson",   "Analyst",    "Data",      "Inactive",  "Nov 2022"],
                        ],
                    )

            # Striped table
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Striped Table").className("text-xs font-semibold text-gray-700")
                    Badge("striped=True", variant="secondary")
                with Flex(direction="col", gap=0).className("overflow-x-auto"):
                    Table(
                        headers=["Package", "Version", "License", "Downloads"],
                        rows=[
                            ["pyui-framework", "0.1.0",  "MIT",     "12.4k"],
                            ["click",          "8.1.7",  "BSD",     "890M"],
                            ["aiohttp",        "3.9.1",  "Apache",  "45M"],
                            ["rich",           "13.7.0", "MIT",     "120M"],
                            ["watchdog",       "3.0.0",  "Apache",  "28M"],
                        ],
                    ).striped()

    # =========================================================
    # SECTION: CHARTS
    # =========================================================
    def _section_charts(self) -> None:
        self._section_header(
            "Charts",
            "Line, Bar, and Pie charts powered by Chart.js.",
            "charts",
        )
        with Grid(cols=2, gap=5):
            # Line chart
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Line Chart").className("text-xs font-semibold text-gray-700")
                    Badge("type=line", variant="secondary")
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="line",
                        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                        datasets=[
                            {
                                "label": "Revenue",
                                "data": [4200, 5800, 4900, 7200, 6100, 8400],
                                "borderColor": "#111827",
                                "backgroundColor": "rgba(17,24,39,0.06)",
                                "tension": 0.4,
                                "fill": True,
                            }
                        ],
                    )

            # Bar chart
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Bar Chart").className("text-xs font-semibold text-gray-700")
                    Badge("type=bar", variant="secondary")
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="bar",
                        labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                        datasets=[
                            {
                                "label": "Signups",
                                "data": [120, 190, 150, 210, 180, 90, 60],
                                "backgroundColor": "#111827",
                                "borderRadius": 6,
                            }
                        ],
                    )

        with Grid(cols=3, gap=5).className("mt-5"):
            # Pie chart
            with Flex(direction="col", gap=0).className(
                "bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Pie Chart").className("text-xs font-semibold text-gray-700")
                    Badge("type=pie", variant="secondary")
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="pie",
                        labels=["Web", "Desktop", "CLI"],
                        datasets=[
                            {
                                "data": [65, 25, 10],
                                "backgroundColor": ["#111827", "#6b7280", "#d1d5db"],
                            }
                        ],
                    )

            # Multi-line chart
            with Flex(direction="col", gap=0).className(
                "col-span-2 bg-white border border-gray-100 rounded-2xl overflow-hidden "
                "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
            ):
                with Flex(align="center", justify="between").className(
                    "px-5 py-3 border-b border-gray-100"
                ):
                    Text("Multi-Series Line").className("text-xs font-semibold text-gray-700")
                    Badge("2 datasets", variant="secondary")
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="line",
                        labels=["Q1", "Q2", "Q3", "Q4"],
                        datasets=[
                            {
                                "label": "2023",
                                "data": [18000, 22000, 19500, 28000],
                                "borderColor": "#111827",
                                "tension": 0.4,
                            },
                            {
                                "label": "2024",
                                "data": [21000, 26000, 24000, 34000],
                                "borderColor": "#6b7280",
                                "borderDash": [5, 5],
                                "tension": 0.4,
                            },
                        ],
                    )

        # Markdown showcase at the bottom
        with Flex(direction="col", gap=0).className(
            "mt-5 bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        ):
            with Flex(align="center", justify="between").className(
                "px-5 py-3 border-b border-gray-100"
            ):
                Text("Markdown").className("text-xs font-semibold text-gray-700")
                Badge("marked.js", variant="secondary")
            with Flex(direction="col", gap=0).className("px-6 py-6"):
                Markdown("""## PyUI Component System

PyUI ships with **42+ production-ready components** organized into six categories:

- **Layout** — `Flex`, `Grid`, `Stack`, `Container`, `Sidebar`, `Split`
- **Display** — `Heading`, `Text`, `Badge`, `Tag`, `Avatar`, `Icon`, `Image`
- **Input** — `Button`, `Input`, `Select`, `Checkbox`, `Toggle`, `Slider`
- **Feedback** — `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`
- **Navigation** — `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu`
- **Data** — `Table`, `Stat`, `Chart`

```python
from pyui import App, Page, Button, Text, reactive

class MyApp(App):
    count = reactive(0)

class Home(Page):
    route = "/"
    def compose(self):
        Text(lambda: f"Count: {MyApp.count.get()}")
        Button("Increment").style("primary").onClick(
            lambda: MyApp.count.set(MyApp.count.get() + 1)
        )
```

> Every component is a Python class. No HTML. No templates. No JavaScript.
""")


class StorybookApp(App):
    name = "PyUI Storybook"
    index = StorybookPage()


def run_storybook(port: int = 8000, open_browser: bool = True) -> None:
    from pyui.server.dev_server import run_dev_server

    run_dev_server(StorybookApp, port=port, open_browser=open_browser)
