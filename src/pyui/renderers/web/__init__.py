"""Web renderer package — public API.

Usage::

    from pyui.renderers.web import render_component, render_page

    html = render_component(Button("Submit").style("primary"))
    full_html = render_page(my_page)
"""

from pyui.renderers.web.generator import WebGenerator, render_component, render_page

__all__ = ["WebGenerator", "render_component", "render_page"]
