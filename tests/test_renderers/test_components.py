"""
Unit tests for the web renderer — component HTML output.

Each test instantiates a component, runs it through render_component(),
and asserts that the output contains the expected HTML attributes and content.
"""

from __future__ import annotations

from pyui.components.data.chart import Chart
from pyui.components.data.stat import Stat
from pyui.components.data.table import Table
from pyui.components.display.avatar import Avatar
from pyui.components.display.badge import Badge
from pyui.components.display.heading import Heading
from pyui.components.display.icon import Icon
from pyui.components.display.image import Image
from pyui.components.display.markdown import Markdown
from pyui.components.display.tag import Tag
from pyui.components.display.text import Text
from pyui.components.feedback.alert import Alert
from pyui.components.feedback.drawer import Drawer
from pyui.components.feedback.modal import Modal
from pyui.components.feedback.progress import Progress
from pyui.components.feedback.skeleton import Skeleton
from pyui.components.feedback.spinner import Spinner
from pyui.components.feedback.toast import Toast
from pyui.components.feedback.tooltip import Tooltip
from pyui.components.input.button import Button
from pyui.components.input.checkbox import Checkbox
from pyui.components.input.datepicker import DatePicker
from pyui.components.input.filepicker import FilePicker
from pyui.components.input.form import Form
from pyui.components.input.input import Input
from pyui.components.input.radio import Radio
from pyui.components.input.select import Select
from pyui.components.input.slider import Slider
from pyui.components.input.textarea import Textarea
from pyui.components.input.toggle import Toggle
from pyui.components.layout.container import Container
from pyui.components.layout.divider import Divider
from pyui.components.layout.flex import Flex
from pyui.components.layout.grid import Grid
from pyui.components.layout.spacer import Spacer
from pyui.components.layout.stack import Stack
from pyui.components.media.video import Video
from pyui.components.navigation.breadcrumb import Breadcrumb
from pyui.components.navigation.menu import Menu
from pyui.components.navigation.nav import Nav
from pyui.components.navigation.pagination import Pagination
from pyui.components.navigation.tabs import Tabs
from pyui.page import Page
from pyui.renderers.web.generator import render_component, render_page

# ── Display ───────────────────────────────────────────────────────────────────


class TestText:
    def test_renders_content(self):
        html = render_component(Text("Hello world"))
        assert "Hello world" in html

    def test_renders_as_paragraph(self):
        html = render_component(Text("Para").paragraph())
        assert "<p" in html

    def test_style_variant_applied(self):
        html = render_component(Text("Muted").style("muted"))
        assert "muted" in html or "gray" in html

    def test_escapes_html(self):
        html = render_component(Text("<script>alert(1)</script>"))
        assert "<script>" not in html
        assert "&lt;script&gt;" in html


class TestHeading:
    def test_renders_h1(self):
        html = render_component(Heading("Title", level=1))
        assert "<h1" in html
        assert "Title" in html

    def test_renders_h3(self):
        html = render_component(Heading("Sub", level=3))
        assert "<h3" in html

    def test_subtitle_rendered(self):
        html = render_component(Heading("Main", subtitle="Sub text"))
        assert "Sub text" in html

    def test_escapes_html(self):
        html = render_component(Heading("<b>bold</b>"))
        assert "<b>" not in html


class TestBadge:
    def test_renders_text(self):
        html = render_component(Badge("New"))
        assert "New" in html
        assert "<span" in html

    def test_variant_classes(self):
        html = render_component(Badge("OK", variant="success"))
        assert "OK" in html


class TestTag:
    def test_renders_text(self):
        html = render_component(Tag("Python"))
        assert "Python" in html

    def test_closable_has_button(self):
        html = render_component(Tag("Close me").closable())
        assert "<button" in html


class TestAvatar:
    def test_renders_initials(self):
        html = render_component(Avatar(name="Alice Smith"))
        assert "AS" in html

    def test_renders_image_src(self):
        html = render_component(Avatar(src="https://example.com/pic.jpg", name="Bob"))
        assert 'src="https://example.com/pic.jpg"' in html

    def test_fallback_icon_when_no_src_or_name(self):
        html = render_component(Avatar())
        assert "data-lucide" in html


class TestIcon:
    def test_renders_lucide_icon(self):
        html = render_component(Icon("zap"))
        assert 'data-lucide="zap"' in html

    def test_custom_size(self):
        html = render_component(Icon("star", size=32))
        assert "32px" in html


class TestImage:
    def test_renders_src_and_alt(self):
        html = render_component(Image(src="photo.jpg", alt="A photo"))
        assert 'src="photo.jpg"' in html
        assert 'alt="A photo"' in html

    def test_lazy_loading(self):
        html = render_component(Image(src="x.jpg", alt=""))
        assert 'loading="lazy"' in html

    def test_width_height_attributes(self):
        html = render_component(Image(src="x.jpg", alt="", width=800, height=600))
        assert 'width="800"' in html
        assert 'height="600"' in html

    def test_no_width_height_when_not_set(self):
        html = render_component(Image(src="x.jpg", alt=""))
        assert "width=" not in html
        assert "height=" not in html


class TestMarkdown:
    def test_renders_container(self):
        html = render_component(Markdown("# Hello"))
        assert "marked.parse" in html
        assert "# Hello" in html


# ── Input ─────────────────────────────────────────────────────────────────────


class TestButton:
    def test_renders_label(self):
        html = render_component(Button("Click me"))
        assert "Click me" in html
        assert "<button" in html

    def test_disabled_attribute(self):
        html = render_component(Button("Off").disabled(True))
        assert "disabled" in html

    def test_loading_spinner(self):
        html = render_component(Button("Wait").loading(True))
        assert "animate-spin" in html

    def test_type_attribute(self):
        html = render_component(Button("Submit", type="submit"))
        assert 'type="submit"' in html

    def test_escapes_label(self):
        html = render_component(Button("<b>bold</b>"))
        assert "<b>" not in html


class TestInput:
    def test_renders_input_element(self):
        html = render_component(Input(placeholder="Enter text"))
        assert "<input" in html
        assert 'placeholder="Enter text"' in html

    def test_label_rendered(self):
        html = render_component(Input(label="Username"))
        assert "Username" in html
        assert "<label" in html

    def test_type_email(self):
        html = render_component(Input(type="email"))
        assert 'type="email"' in html


class TestTextarea:
    def test_renders_textarea(self):
        html = render_component(Textarea(placeholder="Write here"))
        assert "<textarea" in html
        assert 'placeholder="Write here"' in html

    def test_rows_attribute(self):
        html = render_component(Textarea(rows=6))
        assert 'rows="6"' in html


class TestSelect:
    def test_renders_options(self):
        html = render_component(Select(options=[("a", "Option A"), ("b", "Option B")]))
        assert "<select" in html
        assert "Option A" in html
        assert "Option B" in html

    def test_selected_option(self):
        html = render_component(Select(options=[("a", "A"), ("b", "B")], value="b"))
        assert "selected" in html


class TestCheckbox:
    def test_renders_checkbox(self):
        html = render_component(Checkbox(label="Accept"))
        assert 'type="checkbox"' in html
        assert "Accept" in html

    def test_checked_attribute(self):
        html = render_component(Checkbox(checked=True))
        assert "checked" in html


class TestRadio:
    def test_renders_radio_inputs(self):
        html = render_component(Radio(options=[("a", "Option A"), ("b", "Option B")]))
        assert 'type="radio"' in html
        assert "Option A" in html

    def test_selected_value(self):
        html = render_component(Radio(options=[("a", "A"), ("b", "B")], value="a"))
        assert "checked" in html


class TestToggle:
    def test_renders_toggle_button(self):
        html = render_component(Toggle(label="Dark mode"))
        assert 'role="switch"' in html
        assert "Dark mode" in html

    def test_checked_state(self):
        html = render_component(Toggle(checked=True))
        assert 'aria-checked="true"' in html


class TestSlider:
    def test_renders_range_input(self):
        html = render_component(Slider(value=50))
        assert 'type="range"' in html
        assert 'value="50"' in html

    def test_min_max(self):
        html = render_component(Slider(min=10, max=90))
        assert 'min="10"' in html
        assert 'max="90"' in html


class TestDatePicker:
    def test_renders_date_input(self):
        html = render_component(DatePicker(label="Birthday"))
        assert 'type="date"' in html
        assert "Birthday" in html


class TestFilePicker:
    def test_renders_file_input(self):
        html = render_component(FilePicker(label="Upload"))
        assert 'type="file"' in html

    def test_multiple_attribute(self):
        html = render_component(FilePicker(multiple=True))
        assert "multiple" in html


class TestForm:
    def test_renders_form_element(self):
        html = render_component(Form(title="Sign Up"))
        assert "<form" in html
        assert "Sign Up" in html

    def test_prevents_default_submit(self):
        html = render_component(Form())
        assert "preventDefault" in html


# ── Layout ────────────────────────────────────────────────────────────────────


class TestFlex:
    def test_renders_div(self):
        html = render_component(Flex())
        assert "<div" in html

    def test_children_rendered(self):
        f = Flex()
        f.add(Text("child"))
        html = render_component(f)
        assert "child" in html


class TestGrid:
    def test_renders_grid(self):
        html = render_component(Grid(cols=3))
        assert "<div" in html
        assert "grid" in html

    def test_children_rendered(self):
        g = Grid(cols=2)
        g.add(Text("A"), Text("B"))
        html = render_component(g)
        assert "A" in html
        assert "B" in html


class TestStack:
    def test_renders_stack(self):
        html = render_component(Stack())
        assert "<div" in html


class TestContainer:
    def test_renders_container(self):
        html = render_component(Container())
        assert "<div" in html


class TestDivider:
    def test_renders_hr(self):
        html = render_component(Divider())
        assert "<hr" in html or "<div" in html

    def test_labeled_divider(self):
        html = render_component(Divider(label="OR"))
        assert "OR" in html

    def test_role_separator(self):
        html = render_component(Divider())
        assert 'role="separator"' in html


class TestSpacer:
    def test_renders_div(self):
        html = render_component(Spacer())
        assert "<div" in html


# ── Feedback ──────────────────────────────────────────────────────────────────


class TestAlert:
    def test_renders_title(self):
        html = render_component(Alert("Warning", "Be careful", variant="warning"))
        assert "Warning" in html
        assert "Be careful" in html

    def test_role_alert(self):
        html = render_component(Alert("Info", variant="info"))
        assert 'role="alert"' in html

    def test_icon_rendered(self):
        html = render_component(Alert("OK", variant="success"))
        assert "data-lucide" in html


class TestProgress:
    def test_renders_progress_bar(self):
        html = render_component(Progress(value=75))
        assert "75%" in html

    def test_zero_percent(self):
        html = render_component(Progress(value=0))
        assert "0%" in html

    def test_full_percent(self):
        html = render_component(Progress(value=100))
        assert "100%" in html


class TestSpinner:
    def test_renders_svg(self):
        html = render_component(Spinner())
        assert "<svg" in html
        assert "animate-spin" in html

    def test_size_variants(self):
        for size in ["xs", "sm", "md", "lg", "xl"]:
            html = render_component(Spinner(size=size))
            assert "<svg" in html


class TestSkeleton:
    def test_renders_div(self):
        html = render_component(Skeleton())
        assert "<div" in html

    def test_circle_variant(self):
        html = render_component(Skeleton(variant="circle"))
        assert "rounded-full" in html or "circle" in html

    def test_rect_variant(self):
        html = render_component(Skeleton(variant="rect"))
        assert "<div" in html


class TestToast:
    def test_renders_message(self):
        html = render_component(Toast("Saved!", variant="success"))
        assert "Saved!" in html

    def test_auto_dismiss_script(self):
        html = render_component(Toast("Done"))
        assert "setTimeout" in html


class TestModal:
    def test_renders_title(self):
        html = render_component(Modal(title="Confirm"))
        assert "Confirm" in html

    def test_alpine_open_state(self):
        html = render_component(Modal(open=False))
        assert "open: false" in html

    def test_children_rendered(self):
        m = Modal(title="Test")
        m.add(Text("Modal body"))
        html = render_component(m)
        assert "Modal body" in html


class TestDrawer:
    def test_renders_title(self):
        html = render_component(Drawer(title="Settings"))
        assert "Settings" in html

    def test_side_right_transition(self):
        html = render_component(Drawer(side="right"))
        assert "translate-x-full" in html

    def test_side_left_transition(self):
        html = render_component(Drawer(side="left"))
        assert "-translate-x-full" in html


class TestTooltip:
    def test_renders_text(self):
        html = render_component(Tooltip("Helpful hint"))
        assert "Helpful hint" in html

    def test_group_hover(self):
        html = render_component(Tooltip("tip"))
        assert "group" in html


# ── Navigation ────────────────────────────────────────────────────────────────


class TestNav:
    def test_renders_links(self):
        html = render_component(Nav(items=[("Home", "/"), ("About", "/about")]))
        assert "Home" in html
        assert "About" in html
        assert "<nav" in html

    def test_href_attributes(self):
        html = render_component(Nav(items=[("Docs", "/docs")]))
        assert 'href="/docs"' in html


class TestBreadcrumb:
    def test_renders_items(self):
        html = render_component(Breadcrumb(items=[("Home", "/"), ("Page", "/page")]))
        assert "Home" in html
        assert "Page" in html

    def test_last_item_not_linked(self):
        html = render_component(Breadcrumb(items=[("Home", "/"), ("Current", "/cur")]))
        # Last item should be a span, not an anchor
        assert "<span" in html

    def test_aria_label(self):
        html = render_component(Breadcrumb(items=[("Home", "/")]))
        assert 'aria-label="Breadcrumb"' in html


class TestPagination:
    def test_renders_page_numbers(self):
        html = render_component(Pagination(current=3, total=5))
        assert ">1<" in html
        assert ">5<" in html

    def test_prev_next_arrows(self):
        html = render_component(Pagination(current=2, total=4))
        assert "chevron-left" in html
        assert "chevron-right" in html


class TestMenu:
    def test_renders_items(self):
        html = render_component(Menu(items=[("Edit", "/edit"), ("Delete", "/del")]))
        assert "Edit" in html
        assert "Delete" in html

    def test_href_attributes(self):
        html = render_component(Menu(items=[("Profile", "/profile")]))
        assert 'href="/profile"' in html


class TestTabs:
    def test_renders_tab_labels(self):
        t = Tabs(active_tab="Tab A")
        t.add_tab("Tab A", Text("Content A"))
        t.add_tab("Tab B", Text("Content B"))
        html = render_component(t)
        assert "Tab A" in html
        assert "Tab B" in html

    def test_alpine_selected_state(self):
        t = Tabs(active_tab="First")
        t.add_tab("First", Text("Hello"))
        html = render_component(t)
        assert "selected" in html
        assert "First" in html


# ── Data ──────────────────────────────────────────────────────────────────────


class TestTable:
    def test_renders_headers(self):
        html = render_component(Table(headers=["Name", "Age"], rows=[]))
        assert "Name" in html
        assert "Age" in html
        assert "<table" in html

    def test_renders_rows(self):
        html = render_component(Table(headers=["Name"], rows=[["Alice"], ["Bob"]]))
        assert "Alice" in html
        assert "Bob" in html

    def test_escapes_cell_content(self):
        html = render_component(Table(headers=["X"], rows=[["<script>alert(1)</script>"]]))
        assert "<script>" not in html


class TestStat:
    def test_renders_label_and_value(self):
        html = render_component(Stat("Users", "1,234"))
        assert "Users" in html
        assert "1,234" in html

    def test_trend_up(self):
        html = render_component(Stat("Revenue", "$10k", trend="+5%", trend_up=True))
        assert "+5%" in html
        assert "emerald" in html

    def test_trend_down(self):
        html = render_component(Stat("Churn", "3%", trend="-1%", trend_up=False))
        assert "-1%" in html
        assert "red" in html


class TestChart:
    def test_renders_canvas(self):
        html = render_component(Chart(type="line", labels=["A", "B"], datasets=[{"data": [1, 2]}]))
        assert "<canvas" in html

    def test_chart_js_init(self):
        html = render_component(Chart(type="bar", labels=["X"], datasets=[{"data": [5]}]))
        assert "Chart" in html
        assert "chartConfig" in html


# ── Media ─────────────────────────────────────────────────────────────────────


class TestVideo:
    def test_renders_video_element(self):
        html = render_component(Video(src="movie.mp4"))
        assert "<video" in html
        assert "movie.mp4" in html

    def test_controls_attribute(self):
        html = render_component(Video(src="x.mp4", controls=True))
        assert "controls" in html

    def test_autoplay_muted(self):
        html = render_component(Video(src="x.mp4", autoplay=True))
        assert "autoplay" in html
        assert "muted" in html


# ── Page-level rendering ──────────────────────────────────────────────────────


class TestRenderPage:
    def test_renders_full_html_document(self):
        p = Page(title="Test Page", route="/")
        p.add(Heading("Hello", level=1))
        html = render_page(p)
        assert "<!DOCTYPE html>" in html
        assert "<title>Test Page</title>" in html
        assert "Hello" in html

    def test_includes_tailwind(self):
        p = Page(title="T", route="/")
        html = render_page(p)
        assert "tailwindcss" in html

    def test_includes_alpine(self):
        p = Page(title="T", route="/")
        html = render_page(p)
        assert "alpinejs" in html

    def test_theme_css_vars(self):
        p = Page(title="T", route="/")
        html = render_page(p, theme="dark")
        assert "--pyui-" in html

    def test_no_broken_cdn_script(self):
        """Ensure the removed tailwindcss-animate CDN script is gone."""
        p = Page(title="T", route="/")
        html = render_page(p)
        assert "tailwindcss-animate" not in html

    def test_multiple_components(self):
        p = Page(title="Multi", route="/")
        p.add(
            Heading("Title"),
            Text("Body text"),
            Button("Action").style("primary"),
        )
        html = render_page(p)
        assert "Title" in html
        assert "Body text" in html
        assert "Action" in html
