"""
Project scaffolder — implements ``zolt new <name>``.

Creates a minimal working project directory with app.py, requirements.txt,
and README.md. The ``--template`` flag selects a richer starting point.
"""

from __future__ import annotations

from pathlib import Path

# ── Templates ─────────────────────────────────────────────────────────────────

_BLANK_APP = '''\
"""
{name} — built with Zolt.

Run with: zolt run
"""

from pyui import App, Button, Flex, Heading, Page, Text


class HomePage(Page):
    title = "{name}"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", align="center", justify="center", gap=6):
            Heading("{name}", level=1)
            Text("Welcome to your new Zolt app.").style("muted")
            Button("Get Started").style("primary").size("lg")


class {class_name}(App):
    name = "{name}"
    home = HomePage()
'''

_DASHBOARD_APP = '''\
"""
{name} — dashboard template built with Zolt.

Run with: zolt run
"""

from pyui import App, Badge, Flex, Grid, Heading, Nav, Page, Stat, Table, Text


class DashboardPage(Page):
    title = "Dashboard"
    route = "/"
    layout = "default"

    def compose(self) -> None:
        Nav(items=[("Dashboard", "/"), ("Reports", "/reports"), ("Settings", "/settings")])

        with Flex(direction="col", gap=8):
            with Flex(align="center", justify="between"):
                Heading("Dashboard", level=1)
                Badge("Live", variant="success")

            with Grid(cols=4, gap=6):
                Stat("Total Users",   "24,521", trend="+12%",  trend_up=True)
                Stat("Revenue",       "$84,200", trend="+6%",  trend_up=True)
                Stat("Active Sessions", "1,429", trend="+3%",  trend_up=True)
                Stat("Churn Rate",    "2.4%",   trend="-0.8%", trend_up=False)

            Heading("Recent Activity", level=2)
            Table(
                headers=["User", "Action", "Time", "Status"],
                rows=[
                    ["Alice Smith",  "Login",    "2 min ago",  "Success"],
                    ["Bob Jones",    "Export",   "5 min ago",  "Success"],
                    ["Carol White",  "Upload",   "12 min ago", "Pending"],
                    ["Dan Brown",    "Delete",   "1 hr ago",   "Failed"],
                ],
            ).striped()


class ReportsPage(Page):
    title = "Reports"
    route = "/reports"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Reports", level=1)
            Text("Report content goes here.").style("muted")


class SettingsPage(Page):
    title = "Settings"
    route = "/settings"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Settings", level=1)
            Text("Settings content goes here.").style("muted")


class {class_name}(App):
    name = "{name}"
    home = DashboardPage()
    reports = ReportsPage()
    settings = SettingsPage()
'''

_AGENCY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&display=swap');
.font-heading {{ font-family: 'Instrument Serif', serif; font-style: italic; }}
.font-body    {{ font-family: 'Barlow', sans-serif; }}
.liquid-glass {{
  background: rgba(255,255,255,0.01); backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px); border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative; overflow: hidden;
}}
.liquid-glass::before {{
  content: ''; position: absolute; inset: 0; border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,rgba(255,255,255,0.45) 0%,rgba(255,255,255,0.15) 20%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%,rgba(255,255,255,0.15) 80%,rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}}
.liquid-glass-strong {{
  background: rgba(255,255,255,0.01); backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px); border: none;
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);
  position: relative; overflow: hidden;
}}
.liquid-glass-strong::before {{
  content: ''; position: absolute; inset: 0; border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,rgba(255,255,255,0.5) 0%,rgba(255,255,255,0.2) 20%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%,rgba(255,255,255,0.2) 80%,rgba(255,255,255,0.5) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}}
@keyframes wordReveal {{
  0%   {{ filter: blur(10px); opacity: 0; transform: translateY(50px); }}
  50%  {{ filter: blur(5px);  opacity: 0.5; transform: translateY(-5px); }}
  100% {{ filter: blur(0px);  opacity: 1; transform: translateY(0); }}
}}
.word-reveal span {{ display: inline-block; animation: wordReveal 0.7s cubic-bezier(0.16,1,0.3,1) both; }}
@keyframes blurIn {{ from {{ filter: blur(10px); opacity: 0; transform: translateY(20px); }} to {{ filter: blur(0px); opacity: 1; transform: translateY(0); }} }}
.blur-in {{ animation: blurIn 0.6s cubic-bezier(0.16,1,0.3,1) both; }}
.blur-in-delay-1 {{ animation-delay: 0.8s; }}
.blur-in-delay-2 {{ animation-delay: 1.1s; }}
.desaturate {{ filter: saturate(0); }}
"""

_AGENCY_APP = '''\
"""
__NAME__ — AI agency landing page built with Zolt.

Run with: zolt run
"""

from __future__ import annotations

from pyui import App, Flex, Grid, Icon, Image, Page, RawHTML, Text

AGENCY_CSS = """__AGENCY_CSS__"""

HERO_VIDEO = "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4"
MUX_START  = "https://stream.mux.com/9JXDljEVWYwWu01PUkAemafDugK89o01BR6zqJ3aS9u00A.m3u8"
MUX_STATS  = "https://stream.mux.com/NcU3HlHeF7CUL86azTTzpy3Tlb00d6iF3BmCdFslMJYM.m3u8"
MUX_CTA    = "https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8"
GIF_1      = "https://motionsites.ai/assets/hero-finlytic-preview-CV9g0FHP.gif"
GIF_2      = "https://motionsites.ai/assets/hero-wealth-preview-B70idl_u.gif"


class LandingPage(Page):
    title = "__NAME__"
    route = "/"
    layout = "full-width"

    def compose(self) -> None:
        RawHTML('<script src="https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"></script>')

        with Flex(direction="col").className("bg-black min-h-screen"):
            self._navbar()
            self._hero()
            with Flex(direction="col").className("bg-black"):
                self._features_chess()
                self._features_grid()
                self._start()
                self._stats()
                self._testimonials()
                self._cta_footer()

    def _navbar(self) -> None:
        RawHTML("""
<nav style="position:fixed;top:1rem;left:0;right:0;z-index:50;padding:0 2rem;
            display:flex;align-items:center;justify-content:space-between;">
  <img src="/images/logo-icon.png" alt="__NAME__" style="width:2.5rem;height:2.5rem;" />
  <div class="liquid-glass" style="border-radius:9999px;padding:0.25rem 0.375rem;
       display:flex;align-items:center;gap:0.125rem;">
    <a href="#" style="padding:0.5rem 0.75rem;font-size:0.875rem;font-weight:500;
       color:rgba(255,255,255,0.9);font-family:'Barlow',sans-serif;text-decoration:none;">Home</a>
    <a href="#" style="padding:0.5rem 0.75rem;font-size:0.875rem;font-weight:500;
       color:rgba(255,255,255,0.9);font-family:'Barlow',sans-serif;text-decoration:none;">Services</a>
    <a href="#" style="padding:0.5rem 0.75rem;font-size:0.875rem;font-weight:500;
       color:rgba(255,255,255,0.9);font-family:'Barlow',sans-serif;text-decoration:none;">Work</a>
    <a href="#" style="padding:0.5rem 0.75rem;font-size:0.875rem;font-weight:500;
       color:rgba(255,255,255,0.9);font-family:'Barlow',sans-serif;text-decoration:none;">Process</a>
    <a href="#" class="liquid-glass-strong" style="display:inline-flex;align-items:center;
       gap:0.25rem;padding:0.375rem 0.875rem;border-radius:9999px;background:white;
       color:black;font-size:0.875rem;font-weight:500;font-family:'Barlow',sans-serif;
       text-decoration:none;margin-left:0.25rem;">Get Started &#8599;</a>
  </div>
</nav>""")

    def _hero(self) -> None:
        RawHTML(f"""
<section style="position:relative;width:100%;height:100vh;min-height:700px;
                overflow:hidden;background:#000;">
  <video autoplay loop muted playsinline poster="/images/hero_bg.jpeg"
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.85;">
    <source src="{{HERO_VIDEO}}" type="video/mp4" />
  </video>
  <div style="position:absolute;inset:0;background:rgba(0,0,0,0.25);z-index:1;"></div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:300px;
              background:linear-gradient(to top,#000,transparent);z-index:2;pointer-events:none;"></div>
  <div style="position:relative;z-index:3;width:100%;height:100%;display:flex;
              flex-direction:column;align-items:center;justify-content:flex-start;
              padding-top:clamp(5rem,12vh,9rem);text-align:center;padding:clamp(5rem,12vh,9rem) 1.5rem 0;">
    <div class="liquid-glass" style="border-radius:9999px;padding:0.25rem 0.375rem;
         display:inline-flex;align-items:center;gap:0.5rem;margin-bottom:1.75rem;">
      <span style="background:white;color:black;border-radius:9999px;padding:0.25rem 0.75rem;
                   font-size:0.7rem;font-weight:600;font-family:'Barlow',sans-serif;">New</span>
      <span style="color:white;font-size:0.8rem;font-family:'Barlow',sans-serif;
                   padding-right:0.75rem;">Introducing AI-powered web design.</span>
    </div>
    <h1 class="word-reveal" style="font-family:'Instrument Serif',serif;font-style:italic;
        color:white;line-height:0.88;letter-spacing:-0.03em;
        font-size:clamp(3.5rem,9vw,6.5rem);max-width:700px;margin:0 0 1.5rem 0;">
      <span style="animation-delay:0.05s">The</span>&nbsp;
      <span style="animation-delay:0.15s">Website</span>&nbsp;
      <span style="animation-delay:0.25s">Your</span><br>
      <span style="animation-delay:0.35s">Brand</span>&nbsp;
      <span style="animation-delay:0.45s">Deserves</span>
    </h1>
    <p class="blur-in blur-in-delay-1" style="color:rgba(255,255,255,0.85);
       font-family:'Barlow',sans-serif;font-weight:300;font-size:clamp(0.85rem,1.5vw,1rem);
       line-height:1.5;max-width:420px;margin:0 0 2rem 0;">
      Stunning design. Blazing performance. Built by AI, refined by experts.
    </p>
    <div class="blur-in blur-in-delay-2" style="display:flex;align-items:center;
         gap:1rem;flex-wrap:wrap;justify-content:center;margin-bottom:auto;">
      <a href="#" class="liquid-glass-strong" style="display:inline-flex;align-items:center;
         gap:0.4rem;border-radius:9999px;padding:0.625rem 1.25rem;color:white;
         font-family:'Barlow',sans-serif;font-size:0.875rem;font-weight:500;text-decoration:none;">
         Get Started &#8599;</a>
      <a href="#" style="display:inline-flex;align-items:center;gap:0.4rem;color:white;
         font-family:'Barlow',sans-serif;font-size:0.875rem;text-decoration:none;">
         &#9654; Watch the Film</a>
    </div>
    <div style="margin-top:auto;padding:3rem 0 2.5rem;display:flex;flex-direction:column;
                align-items:center;gap:1.25rem;">
      <div class="liquid-glass" style="border-radius:9999px;padding:0.375rem 1rem;display:inline-block;">
        <span style="color:rgba(255,255,255,0.7);font-size:0.75rem;font-family:'Barlow',sans-serif;">
          Trusted by the teams behind</span>
      </div>
      <div style="display:flex;align-items:center;gap:clamp(2rem,5vw,4rem);flex-wrap:wrap;justify-content:center;">
        <span style="font-family:'Instrument Serif',serif;font-style:italic;font-size:clamp(1.25rem,2.5vw,1.75rem);color:white;">Stripe</span>
        <span style="font-family:'Instrument Serif',serif;font-style:italic;font-size:clamp(1.25rem,2.5vw,1.75rem);color:white;">Vercel</span>
        <span style="font-family:'Instrument Serif',serif;font-style:italic;font-size:clamp(1.25rem,2.5vw,1.75rem);color:white;">Linear</span>
        <span style="font-family:'Instrument Serif',serif;font-style:italic;font-size:clamp(1.25rem,2.5vw,1.75rem);color:white;">Notion</span>
        <span style="font-family:'Instrument Serif',serif;font-style:italic;font-size:clamp(1.25rem,2.5vw,1.75rem);color:white;">Figma</span>
      </div>
    </div>
  </div>
</section>""")

    def _features_chess(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-16"):
                Text("Capabilities").className("liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block")
                Text("Pro features. Zero complexity.").className("font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl")
            for reverse, title, body, cta, gif, alt in [
                (False, "Designed to convert. Built to perform.",
                 "Every pixel is intentional. Our AI studies what works across thousands of top sites.",
                 "Learn more", GIF_1, "Design preview"),
                (True, "It gets smarter. Automatically.",
                 "Your site evolves on its own. AI monitors every click, scroll, and conversion.",
                 "See how it works", GIF_2, "AI preview"),
            ]:
                d = "row-reverse" if reverse else "row"
                with Flex(direction="row", align="center", gap=16).className(f"flex-col md:flex-{{d}} mb-24 gap-8 md:gap-16"):
                    with Flex(direction="col", align="start", gap=6).className("flex-1"):
                        Text(title).className("font-heading text-white tracking-tight leading-tight text-3xl md:text-4xl")
                        Text(body).className("text-white/60 font-body font-light text-sm md:text-base leading-relaxed").paragraph()
                        with Flex(direction="row", align="center", gap=2).className("liquid-glass-strong rounded-full px-5 py-2.5 cursor-pointer inline-flex"):
                            Text(cta).className("text-white text-sm font-body font-medium")
                            Text("↗").className("text-white text-sm")
                    with Flex().className("flex-1 liquid-glass rounded-2xl overflow-hidden"):
                        Image(src=gif, alt=alt).className("w-full h-auto")

    def _features_grid(self) -> None:
        cards = [
            ("zap",         "Days, Not Months",      "Concept to launch at a pace that redefines fast."),
            ("palette",     "Obsessively Crafted",   "Every detail considered. Every element refined."),
            ("bar-chart-3", "Built to Convert",      "Layouts informed by data. Results you can measure."),
            ("shield",      "Secure by Default",     "Enterprise-grade protection comes standard."),
        ]
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("Why Us").className("liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block")
                Text("The difference is everything.").className("font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl")
            with Grid(cols=4, gap=6).className("grid-cols-1 md:grid-cols-2 lg:grid-cols-4"):
                for icon, title, body in cards:
                    with Flex(direction="col", align="start", gap=4).className("liquid-glass rounded-2xl p-6"):
                        with Flex(align="center", justify="center").className("liquid-glass-strong rounded-full w-10 h-10"):
                            Icon(icon).className("text-white w-5 h-5")
                        Text(title).className("text-white font-body font-medium text-base")
                        Text(body).className("text-white/60 font-body font-light text-sm leading-relaxed").paragraph()

    def _start(self) -> None:
        RawHTML(f"""
<section style="position:relative;width:100%;min-height:560px;overflow:hidden;background:#000;">
  <video id="start-video" autoplay loop muted playsinline
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"></video>
  <script>(function(){{var v=document.getElementById('start-video');if(window.Hls&&Hls.isSupported()){{var h=new Hls();h.loadSource('{{MUX_START}}');h.attachMedia(v);}}else if(v.canPlayType('application/vnd.apple.mpegurl')){{v.src='{{MUX_START}}';}}}})()</script>
  <div style="position:absolute;top:0;left:0;right:0;height:160px;background:linear-gradient(to bottom,#000,transparent);z-index:1;pointer-events:none;"></div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:160px;background:linear-gradient(to top,#000,transparent);z-index:1;pointer-events:none;"></div>
  <div style="position:relative;z-index:2;width:100%;min-height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:6rem 2rem;">
    <div class="liquid-glass" style="border-radius:9999px;padding:0.25rem 0.875rem;display:inline-block;margin-bottom:1.5rem;">
      <span style="color:white;font-size:0.75rem;font-weight:500;font-family:'Barlow',sans-serif;">How It Works</span>
    </div>
    <h2 style="font-family:'Instrument Serif',serif;font-style:italic;color:white;font-size:clamp(2.5rem,6vw,4.5rem);line-height:0.9;letter-spacing:-0.02em;margin:0 0 1.25rem 0;max-width:600px;">You dream it. We ship it.</h2>
    <p style="color:rgba(255,255,255,0.6);font-family:'Barlow',sans-serif;font-weight:300;font-size:1rem;line-height:1.6;max-width:420px;margin:0 0 2rem 0;">Share your vision. Our AI handles the rest — wireframes, design, code, launch.</p>
    <a href="#" class="liquid-glass-strong" style="display:inline-flex;align-items:center;gap:0.4rem;border-radius:9999px;padding:0.75rem 1.5rem;color:white;font-family:'Barlow',sans-serif;font-size:0.875rem;font-weight:500;text-decoration:none;">Get Started &#8599;</a>
  </div>
</section>""")

    def _stats(self) -> None:
        with Flex(direction="col").className("video-section").height(500):
            RawHTML(f"""
<video id="stats-video" autoplay loop muted playsinline class="desaturate"
  style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"></video>
<script>(function(){{var v=document.getElementById('stats-video');if(window.Hls&&Hls.isSupported()){{var h=new Hls();h.loadSource('{{MUX_STATS}}');h.attachMedia(v);}}else if(v.canPlayType('application/vnd.apple.mpegurl')){{v.src='{{MUX_STATS}}';}}}})()</script>""")
            Flex().className("video-fade-top")
            Flex().className("video-fade-bottom")
            with Flex(direction="col", align="center", justify="center").className("relative z-10 w-full h-full min-h-[500px] py-24 px-8"):
                with Flex(direction="col").className("liquid-glass rounded-3xl p-12 w-full max-w-5xl mx-auto"):
                    with Grid(cols=4, gap=8).className("grid-cols-2 md:grid-cols-4 text-center"):
                        for val, lbl in [("200+","Sites launched"),("98%","Client satisfaction"),("3.2x","More conversions"),("5 days","Average delivery")]:
                            with Flex(direction="col", align="center", gap=2):
                                Text(val).className("font-heading text-white text-4xl md:text-5xl lg:text-6xl leading-none")
                                Text(lbl).className("text-white/60 font-body font-light text-sm")

    def _testimonials(self) -> None:
        quotes = [
            ("A complete rebuild in five days. The result outperformed everything we'd spent months building before.", "Sarah Chen", "CEO, Luminary"),
            ("Conversions up 4x. That's not a typo. The design just works differently when it's built on real data.", "Marcus Webb", "Head of Growth, Arcline"),
            ("They didn't just design our site. They defined our brand. World-class doesn't begin to cover it.", "Elena Voss", "Brand Director, Helix"),
        ]
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("What They Say").className("liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block")
                Text("Don't take our word for it.").className("font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl")
            with Grid(cols=3, gap=6).className("grid-cols-1 md:grid-cols-3"):
                for quote, name, role in quotes:
                    with Flex(direction="col", align="start", gap=6).className("liquid-glass rounded-2xl p-8"):
                        Text(f'"{quote}"').className("text-white/80 font-body font-light text-sm italic leading-relaxed flex-1").paragraph()
                        with Flex(direction="col", gap=1):
                            Text(name).className("text-white font-body font-medium text-sm")
                            Text(role).className("text-white/50 font-body font-light text-xs")

    def _cta_footer(self) -> None:
        RawHTML(f"""
<section style="position:relative;width:100%;min-height:700px;overflow:hidden;background:#000;">
  <video id="cta-video" autoplay loop muted playsinline
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"></video>
  <script>(function(){{var v=document.getElementById('cta-video');if(window.Hls&&Hls.isSupported()){{var h=new Hls();h.loadSource('{{MUX_CTA}}');h.attachMedia(v);}}else if(v.canPlayType('application/vnd.apple.mpegurl')){{v.src='{{MUX_CTA}}';}}}})()</script>
  <div style="position:absolute;top:0;left:0;right:0;height:160px;background:linear-gradient(to bottom,#000,transparent);z-index:1;pointer-events:none;"></div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:160px;background:linear-gradient(to top,#000,transparent);z-index:1;pointer-events:none;"></div>
  <div style="position:relative;z-index:2;width:100%;min-height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:6rem 2rem 2rem;">
    <h2 style="font-family:'Instrument Serif',serif;font-style:italic;color:white;font-size:clamp(2.75rem,7vw,5.5rem);line-height:0.88;letter-spacing:-0.02em;margin:0 0 1.5rem 0;max-width:700px;">Your next website starts here.</h2>
    <p style="color:rgba(255,255,255,0.6);font-family:'Barlow',sans-serif;font-weight:300;font-size:1rem;line-height:1.6;max-width:400px;margin:0 0 2.5rem 0;">Book a free strategy call. No commitment, no pressure. Just possibilities.</p>
    <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;justify-content:center;">
      <a href="#" class="liquid-glass-strong" style="display:inline-flex;align-items:center;border-radius:9999px;padding:0.75rem 1.5rem;color:white;font-family:'Barlow',sans-serif;font-size:0.875rem;font-weight:500;text-decoration:none;">Book a Call</a>
      <a href="#" style="display:inline-flex;align-items:center;border-radius:9999px;padding:0.75rem 1.5rem;background:white;color:black;font-family:'Barlow',sans-serif;font-size:0.875rem;font-weight:500;text-decoration:none;">View Pricing</a>
    </div>
  </div>
  <div style="position:relative;z-index:2;width:100%;padding:2rem 3rem;border-top:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
    <span style="color:rgba(255,255,255,0.4);font-size:0.75rem;font-family:'Barlow',sans-serif;">&copy; 2026 __NAME__. All rights reserved.</span>
    <div style="display:flex;align-items:center;gap:1.5rem;">
      <a href="#" style="color:rgba(255,255,255,0.4);font-size:0.75rem;font-family:'Barlow',sans-serif;text-decoration:none;">Privacy</a>
      <a href="#" style="color:rgba(255,255,255,0.4);font-size:0.75rem;font-family:'Barlow',sans-serif;text-decoration:none;">Terms</a>
      <a href="#" style="color:rgba(255,255,255,0.4);font-size:0.75rem;font-family:'Barlow',sans-serif;text-decoration:none;">Contact</a>
    </div>
  </div>
</section>""")


class __CLASS__(App):
    name = "__NAME__"
    description = "AI-powered web design agency."
    theme = {
        "color.background": "#000000",
        "color.text":       "#ffffff",
        "color.primary":    "#ffffff",
        "color.surface":    "#0a0a0a",
        "color.border":     "rgba(255,255,255,0.2)",
    }
    extra_css = AGENCY_CSS
    head_scripts = ["https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"]
    home = LandingPage()
'''

# ── Inline section files for agency template (fallback when examples/ absent) ─

_SECTION_NAVBAR = '''\
"""Navbar — pure Zolt FloatingNav."""

from pyui import FloatingNav


class Navbar:
    def compose(self) -> None:
        FloatingNav(
            logo_src="/images/logo-icon.png",
            logo_alt="Studio",
            links=["Home", "Services", "Work", "Process"],
            cta_text="Get Started",
            cta_href="#",
        )
'''

_SECTION_HERO = '''\
"""Hero — pure Zolt, no RawHTML."""

from pyui import BlurHeading, Flex, Link, Section, Text, VideoBg

HERO_VIDEO = (
    "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/"
    "hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4"
)
PARTNERS = ["Stripe", "Vercel", "Linear", "Notion", "Figma"]


class HeroSection:
    def compose(self) -> None:
        with Section(min_height=700, bg="#000").className("h-screen"):
            VideoBg(src=HERO_VIDEO, hls=False, fade_height=300, poster="/images/hero_bg.jpeg")
            Flex().className("absolute inset-0 bg-black/30")
            with (
                Flex(direction="col", align="center", justify="start", gap=0)
                .className("absolute inset-0 text-center px-6")
                .inlineStyle("padding-top:clamp(6rem,14vh,10rem);z-index:10;")
            ):
                with Flex(direction="row", align="center", gap=2).className(
                    "liquid-glass rounded-full px-1 py-1 inline-flex mb-7"
                ):
                    Text("New").className(
                        "bg-white text-black rounded-full px-3 py-1 text-xs font-semibold font-body"
                    )
                    Text("Introducing AI-powered web design.").className(
                        "text-white text-sm font-body font-medium pr-3"
                    ).inlineStyle("text-shadow:0 1px 4px rgba(0,0,0,0.6);")
                BlurHeading(
                    "The Website Your Brand Deserves", level=1, delay_ms=100
                ).className("text-white max-w-3xl mx-auto mb-6")
                Text(
                    "Stunning design. Blazing performance. Built by AI, refined by experts."
                ).className(
                    "blur-in blur-in-delay-1 font-body font-light text-base leading-relaxed max-w-md mx-auto mb-8"
                ).inlineStyle(
                    "color:rgba(255,255,255,0.9);text-shadow:0 1px 6px rgba(0,0,0,0.7);"
                ).paragraph()
                with Flex(direction="row", align="center", justify="center", gap=4).className(
                    "blur-in blur-in-delay-2"
                ):
                    Link("Get Started", href="#").style("glass").icon("arrow-up-right")
                    Link("Watch the Film", href="#").style("nav").icon("play", position="left")
            with (
                Flex(direction="col", align="center", gap=5)
                .className("absolute bottom-0 left-0 right-0 text-center pb-10")
                .inlineStyle("z-index:10;")
            ):
                Text("Trusted by the teams behind").className(
                    "liquid-glass rounded-full px-3.5 py-1 text-xs font-medium font-body inline-block"
                ).inlineStyle("color:rgba(255,255,255,0.7);")
                with Flex(direction="row", align="center", justify="center", gap=0, wrap=True).className(
                    "gap-x-12 md:gap-x-16"
                ):
                    for partner in PARTNERS:
                        Text(partner).className("font-heading text-white text-2xl md:text-3xl")
'''

_SECTION_START = '''\
"""StartSection — HLS video via VideoBg."""

from pyui import BlurHeading, Flex, Link, Section, Text, VideoBg

MUX_START = "https://stream.mux.com/9JXDljEVWYwWu01PUkAemafDugK89o01BR6zqJ3aS9u00A.m3u8"


class StartSection:
    def compose(self) -> None:
        with Section(min_height=560, bg="#000"):
            VideoBg(src=MUX_START, hls=True, fade_height=160)
            with Flex(direction="col", align="center", justify="center", gap=6).className(
                "relative z-10 w-full text-center min-h-[560px] py-24 px-8"
            ):
                Text("How It Works").className(
                    "liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block"
                )
                BlurHeading("You dream it. We ship it.", level=2, delay_ms=120).className(
                    "text-white max-w-xl mx-auto"
                )
                Text(
                    "Share your vision. Our AI handles the rest — wireframes, design, code, launch. All in days, not quarters."
                ).className(
                    "text-white/60 font-body font-light text-sm md:text-base max-w-md mx-auto"
                ).paragraph()
                Link("Get Started", href="#").style("glass").icon("arrow-up-right")
'''

_SECTION_FEATURES_CHESS = '''\
"""FeaturesChess — alternating text/gif rows."""

from pyui import Flex, Image, Text

GIF_1 = "https://motionsites.ai/assets/hero-finlytic-preview-CV9g0FHP.gif"
GIF_2 = "https://motionsites.ai/assets/hero-wealth-preview-B70idl_u.gif"

ROWS = [
    {
        "reverse": False,
        "title": "Designed to convert. Built to perform.",
        "body": "Every pixel is intentional. Our AI studies what works across thousands of top sites — then builds yours to outperform them all.",
        "cta": "Learn more",
        "gif": GIF_1,
        "gif_alt": "Conversion-focused design preview",
    },
    {
        "reverse": True,
        "title": "It gets smarter. Automatically.",
        "body": "Your site evolves on its own. AI monitors every click, scroll, and conversion — then optimizes in real time. No manual updates. Ever.",
        "cta": "See how it works",
        "gif": GIF_2,
        "gif_alt": "AI optimization preview",
    },
]


class FeaturesChess:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-16"):
                Text("Capabilities").className(
                    "liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block"
                )
                Text("Pro features. Zero complexity.").className(
                    "font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl"
                )
            for row in ROWS:
                d = "row-reverse" if row["reverse"] else "row"
                with Flex(direction="row", align="center", gap=16).className(
                    f"flex-col md:flex-{d} mb-24 gap-8 md:gap-16"
                ):
                    with Flex(direction="col", align="start", gap=6).className("flex-1"):
                        Text(row["title"]).className(
                            "font-heading text-white tracking-tight leading-tight text-3xl md:text-4xl"
                        )
                        Text(row["body"]).className(
                            "text-white/60 font-body font-light text-sm md:text-base leading-relaxed"
                        ).paragraph()
                        with Flex(direction="row", align="center", gap=2).className(
                            "liquid-glass-strong rounded-full px-5 py-2.5 cursor-pointer inline-flex"
                        ):
                            Text(row["cta"]).className("text-white text-sm font-body font-medium")
                            Text("↗").className("text-white text-sm")
                    with Flex().className("flex-1 liquid-glass rounded-2xl overflow-hidden"):
                        Image(src=row["gif"], alt=row["gif_alt"]).className("w-full h-auto")
'''

_SECTION_FEATURES_GRID = '''\
"""FeaturesGrid — 4-column Why Us cards."""

from pyui import Flex, Grid, Icon, Text

CARDS = [
    {"icon": "zap",         "title": "Days, Not Months",      "body": "Concept to launch at a pace that redefines fast. Because waiting isn\'t a strategy."},
    {"icon": "palette",     "title": "Obsessively Crafted",   "body": "Every detail considered. Every element refined. Design so precise, it feels inevitable."},
    {"icon": "bar-chart-3", "title": "Built to Convert",      "body": "Layouts informed by data. Decisions backed by performance. Results you can measure."},
    {"icon": "shield",      "title": "Secure by Default",     "body": "Enterprise-grade protection comes standard. SSL, DDoS mitigation, compliance. All included."},
]


class FeaturesGrid:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("Why Us").className(
                    "liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block"
                )
                Text("The difference is everything.").className(
                    "font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl"
                )
            with Grid(cols=4, gap=6).className("grid-cols-1 md:grid-cols-2 lg:grid-cols-4"):
                for card in CARDS:
                    with Flex(direction="col", align="start", gap=4).className("liquid-glass rounded-2xl p-6"):
                        with Flex(align="center", justify="center").className("liquid-glass-strong rounded-full w-10 h-10"):
                            Icon(card["icon"]).className("text-white w-5 h-5")
                        Text(card["title"]).className("text-white font-body font-medium text-base")
                        Text(card["body"]).className("text-white/60 font-body font-light text-sm leading-relaxed").paragraph()
'''

_SECTION_STATS = '''\
"""Stats — desaturated HLS video."""

from pyui import Flex, Grid, Section, Text, VideoBg

MUX_STATS = "https://stream.mux.com/NcU3HlHeF7CUL86azTTzpy3Tlb00d6iF3BmCdFslMJYM.m3u8"
STATS = [("200+", "Sites launched"), ("98%", "Client satisfaction"), ("3.2x", "More conversions"), ("5 days", "Average delivery")]


class StatsSection:
    def compose(self) -> None:
        with Section(min_height=500, bg="#000"):
            VideoBg(src=MUX_STATS, hls=True, desaturate=True, fade_height=160)
            with Flex(direction="col", align="center", justify="center").className(
                "relative z-10 w-full min-h-[500px] py-24 px-8"
            ):
                with Flex(direction="col").className("liquid-glass rounded-3xl p-12 md:p-16 w-full max-w-5xl mx-auto"):
                    with Grid(cols=4, gap=8).className("grid-cols-2 md:grid-cols-4 text-center"):
                        for value, label in STATS:
                            with Flex(direction="col", align="center", gap=2):
                                Text(value).className("font-heading text-white text-4xl md:text-5xl lg:text-6xl leading-none")
                                Text(label).className("text-white/60 font-body font-light text-sm")
'''

_SECTION_TESTIMONIALS = '''\
"""Testimonials — 3-column quote cards."""

from pyui import Flex, Grid, Text

QUOTES = [
    {"quote": "A complete rebuild in five days. The result outperformed everything we\'d spent months building before.", "name": "Sarah Chen", "role": "CEO, Luminary"},
    {"quote": "Conversions up 4x. That\'s not a typo. The design just works differently when it\'s built on real data.", "name": "Marcus Webb", "role": "Head of Growth, Arcline"},
    {"quote": "They didn\'t just design our site. They defined our brand. World-class doesn\'t begin to cover it.", "name": "Elena Voss", "role": "Brand Director, Helix"},
]


class Testimonials:
    def compose(self) -> None:
        with Flex(direction="col", gap=0).className("agency-section bg-black"):
            with Flex(direction="col", align="center", gap=4).className("text-center mb-12"):
                Text("What They Say").className(
                    "liquid-glass rounded-full px-3.5 py-1 text-xs font-medium text-white font-body inline-block"
                )
                Text("Don\'t take our word for it.").className(
                    "font-heading text-white tracking-tight leading-none text-4xl md:text-5xl lg:text-6xl"
                )
            with Grid(cols=3, gap=6).className("grid-cols-1 md:grid-cols-3"):
                for q in QUOTES:
                    with Flex(direction="col", align="start", gap=6).className("liquid-glass rounded-2xl p-8"):
                        Text(f\'"{q["quote"]}"\').className(
                            "text-white/80 font-body font-light text-sm italic leading-relaxed flex-1"
                        ).paragraph()
                        with Flex(direction="col", gap=1):
                            Text(q["name"]).className("text-white font-body font-medium text-sm")
                            Text(q["role"]).className("text-white/50 font-body font-light text-xs")
'''

_SECTION_CTA_FOOTER = '''\
"""CTA + Footer — HLS video."""

from pyui import Flex, Link, Section, Text, VideoBg

MUX_CTA = "https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8"


class CtaFooter:
    def compose(self) -> None:
        with Section(min_height=700, bg="#000"):
            VideoBg(src=MUX_CTA, hls=True, fade_height=160)
            with Flex(direction="col", align="center", justify="center", gap=8).className(
                "relative z-10 w-full min-h-[600px] text-center py-24 px-8"
            ):
                Text("Your next website starts here.").className(
                    "font-heading text-white leading-none text-5xl md:text-6xl lg:text-7xl max-w-3xl mx-auto"
                )
                Text(
                    "Book a free strategy call. See what AI-powered design can do. No commitment, no pressure. Just possibilities."
                ).className(
                    "text-white/60 font-body font-light text-sm md:text-base max-w-md mx-auto"
                ).paragraph()
                with Flex(direction="row", align="center", justify="center", gap=4):
                    Link("Book a Call", href="#").style("glass")
                    Link("View Pricing", href="#").style("primary")
            with Flex(direction="row", align="center", justify="between").className(
                "relative z-10 w-full px-8 py-8 border-t border-white/10"
            ):
                Text("© 2026 Studio. All rights reserved.").className("text-white/40 text-xs font-body")
                with Flex(direction="row", align="center", gap=6):
                    for label in ["Privacy", "Terms", "Contact"]:
                        Link(label, href="#").style("footer")
'''

_REQUIREMENTS = """\
zolt>=1.0.0
"""

_README = """\
# {name}

Built with [PyUI](https://github.com/12errh/pyui).

## Getting started

```bash
pip install zolt
zolt run
```

## Commands

```bash
zolt run              # Start dev server
zolt run --target desktop  # Open as desktop app
zolt run --target cli      # Render in terminal
zolt build            # Build for production
```
"""

_TEMPLATES: dict[str, str] = {
    "blank": _BLANK_APP,
    "dashboard": _DASHBOARD_APP,
    "landing": _BLANK_APP,
    "admin": _DASHBOARD_APP,
    "auth": _BLANK_APP,
    "agency": _AGENCY_APP,
}


def _to_class_name(name: str) -> str:
    """Convert a project name like 'my-app' to a class name like 'MyApp'."""
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_")) + "App"


def create_project(name: str, template: str = "blank", target: str = "web") -> Path:
    """
    Scaffold a new PyUI project in a directory called *name*.

    Parameters
    ----------
    name : str
        Project name (also used as the directory name).
    template : str
        One of ``"blank"``, ``"dashboard"``, ``"landing"``, ``"admin"``, ``"auth"``.
    target : str
        Default render target (informational only — written to README).

    Returns
    -------
    Path
        The created project directory.

    Raises
    ------
    FileExistsError
        If the directory already exists.
    """
    project_dir = Path(name)
    if project_dir.exists():
        raise FileExistsError(
            f"Directory '{name}' already exists. "
            "Choose a different name or remove the existing directory."
        )

    project_dir.mkdir(parents=True)

    if template == "agency":
        _scaffold_agency(project_dir, name)
    else:
        class_name = _to_class_name(name)
        app_template = _TEMPLATES.get(template, _BLANK_APP)
        formatted = app_template.format(name=name, class_name=class_name)
        (project_dir / "app.py").write_text(formatted, encoding="utf-8")

    (project_dir / "requirements.txt").write_text(_REQUIREMENTS, encoding="utf-8")
    (project_dir / "README.md").write_text(
        _README.format(name=name, target=target),
        encoding="utf-8",
    )

    return project_dir


def _scaffold_agency(project_dir: Path, name: str) -> None:
    """
    Copy the exact multi-file agency landing page structure into *project_dir*.

    Produces:
        app.py
        styles.py
        sections/__init__.py
        sections/navbar.py
        sections/hero.py
        sections/start.py
        sections/features_chess.py
        sections/features_grid.py
        sections/stats.py
        sections/testimonials.py
        sections/cta_footer.py
    """

    # Try to copy from the installed examples/agency directory first,
    # then fall back to writing the files inline.
    src_dir = Path(__file__).parent.parent.parent / "examples" / "agency"

    if src_dir.exists():
        # Copy the whole directory tree, excluding __pycache__
        for src_file in src_dir.rglob("*.py"):
            if "__pycache__" in src_file.parts:
                continue
            rel = src_file.relative_to(src_dir)
            dest = project_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            content = src_file.read_text(encoding="utf-8")
            # Update the app name in app.py
            if rel == Path("app.py"):
                content = content.replace(
                    'name = "Studio — AI Web Design"',
                    f'name = "{name}"',
                ).replace(
                    'title = "Studio — AI-Powered Web Design"',
                    f'title = "{name}"',
                )
            dest.write_text(content, encoding="utf-8")
    else:
        # Fallback: write files inline (for installed package without examples/)
        _write_agency_inline(project_dir, name)


def _write_agency_inline(project_dir: Path, name: str) -> None:
    """Write agency files inline when examples/ directory is not available."""
    sections_dir = project_dir / "sections"
    sections_dir.mkdir(exist_ok=True)

    # ── app.py ────────────────────────────────────────────────────────────────
    (project_dir / "app.py").write_text(
        f'''"""
{name} — AI Agency Landing Page built with Zolt.

Run with:
    zolt run
"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from pyui import App, Flex, Page  # noqa: E402

from sections.cta_footer import CtaFooter  # noqa: E402
from sections.features_chess import FeaturesChess  # noqa: E402
from sections.features_grid import FeaturesGrid  # noqa: E402
from sections.hero import HeroSection  # noqa: E402
from sections.navbar import Navbar  # noqa: E402
from sections.start import StartSection  # noqa: E402
from sections.stats import StatsSection  # noqa: E402
from sections.testimonials import Testimonials  # noqa: E402
from styles import AGENCY_CSS  # noqa: E402

_HLS_CDN = "https://cdn.jsdelivr.net/npm/hls.js@1.6.15/dist/hls.min.js"


class LandingPage(Page):
    title = "{name}"
    route = "/"
    layout = "full-width"

    def compose(self) -> None:
        with Flex(direction="col").className("bg-black min-h-screen"):
            Navbar().compose()
            HeroSection().compose()
            with Flex(direction="col").className("bg-black"):
                FeaturesChess().compose()
                FeaturesGrid().compose()
                StartSection().compose()
                StatsSection().compose()
                Testimonials().compose()
                CtaFooter().compose()


class {_to_class_name(name)}(App):
    name = "{name}"
    description = "AI-powered web design agency."
    theme = {{
        "color.background": "#000000",
        "color.text":       "#ffffff",
        "color.primary":    "#ffffff",
        "color.surface":    "#0a0a0a",
        "color.border":     "rgba(255,255,255,0.2)",
    }}
    extra_css = AGENCY_CSS
    head_scripts = [_HLS_CDN]
    home = LandingPage()
''',
        encoding="utf-8",
    )

    # ── styles.py — copy AGENCY_CSS constant ──────────────────────────────────
    (project_dir / "styles.py").write_text(
        f'"""Custom CSS for the agency landing page."""\n\nAGENCY_CSS = {_AGENCY_CSS!r}\n',
        encoding="utf-8",
    )

    # ── sections/__init__.py ──────────────────────────────────────────────────
    (sections_dir / "__init__.py").write_text("# sections\n", encoding="utf-8")

    # ── Individual section files — copied verbatim from the source ────────────
    _SECTION_FILES = {
        "navbar.py": _SECTION_NAVBAR,
        "hero.py": _SECTION_HERO,
        "start.py": _SECTION_START,
        "features_chess.py": _SECTION_FEATURES_CHESS,
        "features_grid.py": _SECTION_FEATURES_GRID,
        "stats.py": _SECTION_STATS,
        "testimonials.py": _SECTION_TESTIMONIALS,
        "cta_footer.py": _SECTION_CTA_FOOTER,
    }
    for filename, content in _SECTION_FILES.items():
        (sections_dir / filename).write_text(content, encoding="utf-8")
