"""
PyUI Portfolio — "The Compiler" — Awwwards-Level Showcase

Design Concept: CINEMATIC DARK EDITORIAL
- The page IS a live PyUI compilation unfolding in real time
- Every section reveals like a compiler parsing and rendering output
- Luxury editorial meets raw terminal power
- Orbital cursor that responds to mouse movement
- Tokenized text animations — words arrive like compiler tokens
- A live "code → UI" split-screen demonstrating the framework
- Vertical rhythm based on an 8px grid, tight typographic control
- Color: deep obsidian background, phosphor green accents, chalk white

Fonts:
- Display: "PP Editorial New" feel via 'Playfair Display' (Google)
- Mono: 'JetBrains Mono' for all code/terminal elements
- Body: 'DM Sans' — clean, modern, reads at small sizes

Run with: python portfolio.py
Opens at: http://localhost:9010
"""

import base64
import os
from pyui import (
    App,
    Button,
    Container,
    Flex,
    Grid,
    Heading,
    Icon,
    Image,
    Input,
    Page,
    RawHTML,
    Stack,
    Text,
    reactive,
)


class PortfolioPage(Page):
    title = "PyUI — Write Python. Ship Everything."
    route = "/"
    layout = "full-width"

    def compose(self) -> None:

        # ── GLOBAL STYLES + FONTS + ANIMATIONS ─────────────────────────────
        Text("").className("").inject_html("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=JetBrains+Mono:wght@300;400;500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --obsidian:   #080808;
    --obsidian-2: #0f0f0f;
    --obsidian-3: #161616;
    --obsidian-4: #1e1e1e;
    --phosphor:   #00ff88;
    --phosphor-2: #00cc6a;
    --phosphor-dim:#00ff8822;
    --chalk:      #f0ede6;
    --chalk-2:    #c8c4bc;
    --chalk-3:    #7a776f;
    --orange:     #ff5c1a;
    --blue:       #3d7fff;
    --purple:     #9b6dff;
    --gold:       #d4a843;
    --border:     rgba(240,237,230,0.07);
    --border-bright: rgba(240,237,230,0.15);
    --font-display: 'Playfair Display', Georgia, serif;
    --font-mono:    'JetBrains Mono', 'Courier New', monospace;
    --font-body:    'DM Sans', system-ui, sans-serif;
    --ease-expo:    cubic-bezier(0.16, 1, 0.3, 1);
    --ease-back:    cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--obsidian);
    color: var(--chalk);
    font-family: var(--font-body);
    font-weight: 300;
    line-height: 1.6;
    overflow-x: hidden;
    cursor: none;
  }

  /* ── CUSTOM CURSOR ── */
  #cursor-ring {
    position: fixed; top: 0; left: 0; z-index: 9999;
    width: 40px; height: 40px; border-radius: 50%;
    border: 1px solid var(--phosphor);
    pointer-events: none;
    transform: translate(-50%, -50%);
    transition: width 0.3s var(--ease-expo), height 0.3s var(--ease-expo),
                border-color 0.3s ease, opacity 0.3s ease;
    mix-blend-mode: difference;
  }
  #cursor-dot {
    position: fixed; top: 0; left: 0; z-index: 10000;
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--phosphor);
    pointer-events: none;
    transform: translate(-50%, -50%);
  }
  body:has(a:hover) #cursor-ring,
  body:has(button:hover) #cursor-ring { width: 64px; height: 64px; border-color: var(--orange); }

  /* ── SCROLL ANIMATIONS ── */
  .reveal { opacity: 0; transform: translateY(48px); transition: opacity 0.9s var(--ease-expo), transform 0.9s var(--ease-expo); }
  .reveal.in-view { opacity: 1; transform: translateY(0); }
  .reveal-left { opacity: 0; transform: translateX(-48px); transition: opacity 0.9s var(--ease-expo), transform 0.9s var(--ease-expo); }
  .reveal-left.in-view { opacity: 1; transform: translateX(0); }
  .reveal-right { opacity: 0; transform: translateX(48px); transition: opacity 0.9s var(--ease-expo), transform 0.9s var(--ease-expo); }
  .reveal-right.in-view { opacity: 1; transform: translateX(0); }
  .reveal-scale { opacity: 0; transform: scale(0.92); transition: opacity 0.9s var(--ease-expo), transform 0.9s var(--ease-expo); }
  .reveal-scale.in-view { opacity: 1; transform: scale(1); }
  .d1 { transition-delay: 0.05s; } .d2 { transition-delay: 0.15s; }
  .d3 { transition-delay: 0.25s; } .d4 { transition-delay: 0.35s; }
  .d5 { transition-delay: 0.45s; } .d6 { transition-delay: 0.55s; }

  /* ── TYPOGRAPHY ── */
  .display { font-family: var(--font-display); }
  .mono    { font-family: var(--font-mono); }
  .label   { font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--chalk-3); }
  .phosphor-text { color: var(--phosphor); }
  .gold-text { color: var(--gold); }

  /* ── NOISE TEXTURE OVERLAY ── */
  .noise::after {
    content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 1;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    opacity: 0.4;
  }

  /* ── GRID LINES ── */
  .grid-bg {
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 80px 80px;
  }

  /* ── GLOW EFFECTS ── */
  .glow-phosphor { box-shadow: 0 0 40px var(--phosphor-dim), 0 0 80px var(--phosphor-dim); }
  .glow-text { text-shadow: 0 0 30px rgba(0,255,136,0.4); }

  /* ── SCANLINE ── */
  @keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
  }
  .scanline {
    position: fixed; top: 0; left: 0; width: 100%; height: 2px;
    background: linear-gradient(transparent, var(--phosphor), transparent);
    opacity: 0.03; z-index: 9998; pointer-events: none;
    animation: scanline 8s linear infinite;
  }

  /* ── HORIZONTAL MARQUEE ── */
  @keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
  .marquee-track { animation: marquee 28s linear infinite; display: flex; width: max-content; }
  .marquee-track:hover { animation-play-state: paused; }

  /* ── BLINKING CARET ── */
  @keyframes caret { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
  .caret::after { content: '_'; animation: caret 1s step-end infinite; color: var(--phosphor); }

  /* ── COUNTER ANIMATION ── */
  @keyframes count-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  .counter { animation: count-up 0.6s var(--ease-expo) both; }

  /* ── TYPEWRITER ── */
  @keyframes type-in {
    from { width: 0; }
    to { width: 100%; }
  }

  /* ── GRADIENT BORDER ── */
  .grad-border {
    background: linear-gradient(var(--obsidian-3), var(--obsidian-3)) padding-box,
                linear-gradient(135deg, var(--phosphor), var(--blue), var(--purple)) border-box;
    border: 1px solid transparent;
  }

  /* ── PILL TAG ── */
  .tag {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--font-mono); font-size: 10px; font-weight: 500;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 100px;
    border: 1px solid var(--border-bright);
    color: var(--chalk-2); background: rgba(255,255,255,0.03);
  }
  .tag.green { border-color: var(--phosphor); color: var(--phosphor); background: rgba(0,255,136,0.05); }
  .tag.orange { border-color: var(--orange); color: var(--orange); background: rgba(255,92,26,0.05); }

  /* ── BUTTONS ── */
  .btn-primary {
    display: inline-flex; align-items: center; gap: 10px;
    font-family: var(--font-mono); font-size: 11px; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    padding: 16px 32px;
    background: var(--phosphor); color: var(--obsidian);
    border: none; cursor: none;
    transition: all 0.3s var(--ease-expo);
    position: relative; overflow: hidden;
  }
  .btn-primary::before {
    content: ''; position: absolute; inset: 0;
    background: var(--chalk); transform: translateX(-101%);
    transition: transform 0.4s var(--ease-expo);
  }
  .btn-primary:hover::before { transform: translateX(0); }
  .btn-primary span { position: relative; z-index: 1; }

  .btn-ghost {
    display: inline-flex; align-items: center; gap: 10px;
    font-family: var(--font-mono); font-size: 11px; font-weight: 500;
    letter-spacing: 0.15em; text-transform: uppercase;
    padding: 15px 32px;
    background: transparent; color: var(--chalk);
    border: 1px solid var(--border-bright); cursor: none;
    transition: all 0.3s var(--ease-expo);
  }
  .btn-ghost:hover { border-color: var(--chalk); background: rgba(240,237,230,0.04); }

  /* ── SECTION DIVIDER ── */
  .section-num {
    font-family: var(--font-mono); font-size: 10px; color: var(--chalk-3);
    letter-spacing: 0.3em; text-transform: uppercase;
    display: flex; align-items: center; gap: 16px;
  }
  .section-num::after { content: ''; flex: 1; height: 1px; background: var(--border); }

  /* ── CODE WINDOW ── */
  .code-win { background: var(--obsidian-3); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  .code-win-bar { background: var(--obsidian-4); padding: 14px 20px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border); }
  .code-dot { width: 12px; height: 12px; border-radius: 50%; }
  .code-body { padding: 28px; font-family: var(--font-mono); font-size: 13px; line-height: 2; }
  .tok-kw  { color: #c792ea; }
  .tok-cls { color: #82aaff; }
  .tok-fn  { color: #82aaff; }
  .tok-str { color: #c3e88d; }
  .tok-cmt { color: #546e7a; font-style: italic; }
  .tok-num { color: var(--orange); }
  .tok-acc { color: var(--phosphor); }
  .tok-pct { color: var(--gold); }

  /* ── STAT CARD ── */
  .stat-card { border-top: 1px solid var(--border); padding: 40px 0; transition: all 0.4s var(--ease-expo); }
  .stat-card:hover { border-top-color: var(--phosphor); }
  .stat-card:hover .stat-num { color: var(--phosphor); }
  .stat-num { font-family: var(--font-display); font-size: clamp(48px, 6vw, 80px); font-weight: 900; color: var(--chalk); line-height: 1; transition: color 0.4s ease; }
  .stat-label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--chalk-3); margin-top: 12px; }
  .stat-delta { font-family: var(--font-mono); font-size: 11px; color: var(--phosphor); margin-top: 8px; }

  /* ── FEATURE CARD ── */
  .feat-card {
    border: 1px solid var(--border);
    padding: 40px; position: relative; overflow: hidden;
    transition: all 0.5s var(--ease-expo);
    background: transparent;
  }
  .feat-card::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(0,255,136,0.03), transparent 60%);
    opacity: 0; transition: opacity 0.5s ease;
  }
  .feat-card:hover { border-color: var(--border-bright); transform: translateY(-4px); }
  .feat-card:hover::before { opacity: 1; }
  .feat-icon {
    width: 48px; height: 48px; border-radius: 12px;
    background: var(--obsidian-4); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 18px; margin-bottom: 28px;
    transition: all 0.3s ease;
  }
  .feat-card:hover .feat-icon { border-color: var(--phosphor); background: rgba(0,255,136,0.08); }

  /* ── SYNTAX HIGHLIGHT IN LIVE DEMO ── */
  .live-output {
    background: var(--obsidian-2); border: 1px solid var(--border);
    border-radius: 12px; padding: 40px; height: 100%;
    display: flex; flex-direction: column; justify-content: center;
    gap: 16px;
  }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 3px; }
  ::-webkit-scrollbar-track { background: var(--obsidian); }
  ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }

  /* ── SELECTION ── */
  ::selection { background: var(--phosphor); color: var(--obsidian); }

  /* ── RESPONSIVE ── */
  @media (max-width: 768px) {
    body { cursor: auto; }
    #cursor-ring, #cursor-dot { display: none; }
  }

  /* ── FLOATING LABEL ── */
  @keyframes float { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
  .float { animation: float 6s ease-in-out infinite; }

  /* ── STAGGER CHILDREN ── */
  .stagger > * { opacity: 0; transform: translateY(24px); }
  .stagger.in-view > *:nth-child(1) { animation: reveal-child 0.7s 0.05s var(--ease-expo) forwards; }
  .stagger.in-view > *:nth-child(2) { animation: reveal-child 0.7s 0.15s var(--ease-expo) forwards; }
  .stagger.in-view > *:nth-child(3) { animation: reveal-child 0.7s 0.25s var(--ease-expo) forwards; }
  .stagger.in-view > *:nth-child(4) { animation: reveal-child 0.7s 0.35s var(--ease-expo) forwards; }
  .stagger.in-view > *:nth-child(5) { animation: reveal-child 0.7s 0.45s var(--ease-expo) forwards; }
  .stagger.in-view > *:nth-child(6) { animation: reveal-child 0.7s 0.55s var(--ease-expo) forwards; }
  @keyframes reveal-child { to { opacity: 1; transform: translateY(0); } }

  /* ── HERO CHAR ANIMATION ── */
  .hero-char {
    display: inline-block; opacity: 0; transform: translateY(60px) rotate(4deg);
    animation: char-in 0.8s var(--ease-expo) forwards;
  }
  @keyframes char-in { to { opacity: 1; transform: translateY(0) rotate(0deg); } }

  /* ── HORIZONTAL RULE GRADIENT ── */
  hr.fancy { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border-bright), transparent); }

</style>

<!-- Cursor elements -->
<div id="cursor-ring"></div>
<div id="cursor-dot"></div>
<div class="scanline"></div>
""")

        # ══════════════════════════════════════════════════════════════════
        # 1. NAVBAR
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<nav style="position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(8,8,8,0.85);backdrop-filter:blur(24px);border-bottom:1px solid var(--border);">
  <div style="max-width:1400px;margin:0 auto;padding:0 48px;height:72px;display:flex;align-items:center;justify-content:space-between;">

    <a href="#" style="text-decoration:none;display:flex;align-items:baseline;gap:8px;">
      <span style="font-family:var(--font-display);font-size:22px;font-weight:900;color:var(--chalk);letter-spacing:-0.03em;">Py</span>
      <span style="font-family:var(--font-mono);font-size:22px;font-weight:700;color:var(--phosphor);letter-spacing:-0.03em;">UI</span>
      <span style="font-family:var(--font-mono);font-size:9px;color:var(--chalk-3);letter-spacing:0.2em;margin-left:4px;padding:2px 8px;border:1px solid var(--border);text-transform:uppercase;">v0.3</span>
    </a>

    <div style="display:flex;align-items:center;gap:40px;">
      <div style="display:flex;gap:32px;" class="hidden-mobile">
        <a href="#syntax"   style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);text-decoration:none;transition:color 0.3s;">Syntax</a>
        <a href="#targets"  style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);text-decoration:none;transition:color 0.3s;">Targets</a>
        <a href="#features" style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);text-decoration:none;transition:color 0.3s;">Features</a>
        <a href="#compare"  style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);text-decoration:none;transition:color 0.3s;">Compare</a>
      </div>
      <div style="display:flex;gap:12px;">
        <a href="#" class="btn-ghost" style="padding:10px 24px;font-size:10px;"><span>Docs</span></a>
        <a href="#" class="btn-primary" style="padding:10px 24px;font-size:10px;"><span>pip install pyui</span></a>
      </div>
    </div>

  </div>
</nav>
""")

        # ══════════════════════════════════════════════════════════════════
        # 2. HERO — FULL VIEWPORT TYPOGRAPHIC STATEMENT
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section style="min-height:100vh;display:flex;flex-direction:column;justify-content:center;padding:120px 48px 80px;max-width:1400px;margin:0 auto;position:relative;">

  <!-- Background grid -->
  <div class="grid-bg" style="position:absolute;inset:0;opacity:0.5;pointer-events:none;"></div>

  <!-- Floating terminal snippet — top right -->
  <div class="float" style="position:absolute;top:140px;right:0;width:320px;opacity:0.6;animation-delay:1s;">
    <div class="code-win" style="transform:rotate(2deg);">
      <div class="code-win-bar">
        <div class="code-dot" style="background:#ff5f56;"></div>
        <div class="code-dot" style="background:#ffbd2e;"></div>
        <div class="code-dot" style="background:#27c93f;"></div>
        <span style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);margin-left:8px;">app.py</span>
      </div>
      <div class="code-body" style="font-size:11px;line-height:1.9;padding:20px 24px;">
        <div><span class="tok-kw">from</span> <span class="tok-acc">pyui</span> <span class="tok-kw">import</span> <span class="tok-cls">App</span>, <span class="tok-cls">Page</span>, <span class="tok-cls">Button</span></div>
        <div class="tok-cmt"># That's it. Seriously.</div>
        <div>&nbsp;</div>
        <div><span class="tok-kw">class</span> <span class="tok-cls">MyApp</span>(<span class="tok-cls">App</span>):</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">home</span> = <span class="tok-cls">Page</span>(<span class="tok-str">title=</span><span class="tok-str">"Home"</span>)</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">home</span>.<span class="tok-fn">add</span>(<span class="tok-cls">Button</span>(<span class="tok-str">"Launch"</span>))</div>
      </div>
    </div>
  </div>

  <!-- Main headline -->
  <div style="position:relative;z-index:1;max-width:1000px;">
    <div style="margin-bottom:32px;display:flex;align-items:center;gap:16px;">
      <span class="tag green">
        <span style="width:6px;height:6px;border-radius:50%;background:var(--phosphor);display:inline-block;"></span>
        Now in Public Beta
      </span>
      <span class="tag">Python 3.10+</span>
    </div>

    <h1 id="hero-headline" style="font-family:var(--font-display);font-weight:900;line-height:0.9;letter-spacing:-0.03em;margin-bottom:40px;">
      <div style="overflow:hidden;padding-bottom:8px;">
        <span style="display:block;font-size:clamp(72px,11vw,160px);color:var(--chalk);" id="hero-line-1">Write</span>
      </div>
      <div style="overflow:hidden;padding-bottom:8px;">
        <span style="display:block;font-size:clamp(72px,11vw,160px);color:var(--phosphor);font-style:italic;" id="hero-line-2">Python.</span>
      </div>
      <div style="overflow:hidden;padding-bottom:8px;">
        <span style="display:block;font-size:clamp(72px,11vw,160px);color:var(--chalk-3);" id="hero-line-3">Ship <em style="color:var(--chalk);font-style:normal;" id="target-cycle">Everything.</em></span>
      </div>
    </h1>

    <div style="display:flex;align-items:start;gap:80px;flex-wrap:wrap;">
      <p style="font-size:18px;line-height:1.7;color:var(--chalk-2);max-width:480px;font-weight:300;">
        The first Python framework that compiles to web, desktop, and terminal — from a single, beautiful API. No HTML. No JavaScript. No compromise.
      </p>
      <div style="display:flex;flex-direction:column;gap:16px;flex-shrink:0;">
        <div style="display:flex;gap:12px;">
          <a href="#syntax" class="btn-primary"><span>→ See the Syntax</span></a>
          <a href="#" class="btn-ghost">Watch 90s Demo</a>
        </div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);letter-spacing:0.1em;">
          <span style="color:var(--phosphor);">$</span> pip install pyui-framework
        </div>
      </div>
    </div>
  </div>

  <!-- Scroll indicator -->
  <div style="position:absolute;bottom:48px;left:48px;display:flex;align-items:center;gap:12px;opacity:0.4;">
    <div style="width:1px;height:40px;background:linear-gradient(to bottom,var(--chalk-3),transparent);"></div>
    <span style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.3em;text-transform:uppercase;color:var(--chalk-3);">Scroll to explore</span>
  </div>

  <!-- Live build indicator — bottom right -->
  <div style="position:absolute;bottom:48px;right:48px;display:flex;align-items:center;gap:10px;opacity:0.5;">
    <div style="width:8px;height:8px;border-radius:50%;background:var(--phosphor);animation:caret 1.5s step-end infinite;"></div>
    <span style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:var(--chalk-3);">Build successful</span>
  </div>

</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 3. MARQUEE TICKER
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<div style="border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:20px 0;overflow:hidden;background:var(--obsidian-2);">
  <div class="marquee-track" style="gap:0;">
    <span style="font-family:var(--font-mono);font-size:12px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);white-space:nowrap;padding-right:80px;">
      <span style="color:var(--phosphor);">◆</span>&nbsp; Web Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Desktop Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; CLI Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Reactive State &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Hot Reload &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Theme Engine &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Component Marketplace &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Type Safe &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Python 3.10+ &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp;
    </span>
    <span style="font-family:var(--font-mono);font-size:12px;letter-spacing:0.15em;text-transform:uppercase;color:var(--chalk-3);white-space:nowrap;padding-right:80px;" aria-hidden="true">
      <span style="color:var(--phosphor);">◆</span>&nbsp; Web Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Desktop Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; CLI Renderer &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Reactive State &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Hot Reload &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Theme Engine &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Component Marketplace &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Type Safe &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp; Python 3.10+ &nbsp;&nbsp;<span style="color:var(--border-bright);">—</span>&nbsp;&nbsp;
    </span>
  </div>
</div>
""")

        # ══════════════════════════════════════════════════════════════════
        # 4. SYNTAX SECTION — LIVE CODE DEMO
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section id="syntax" style="padding:160px 48px;max-width:1400px;margin:0 auto;">

  <div class="section-num reveal" style="margin-bottom:80px;">
    <span>01 — The Syntax</span>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">

    <!-- Left: Headline + description -->
    <div>
      <h2 class="reveal d1" style="font-family:var(--font-display);font-size:clamp(40px,5vw,72px);font-weight:900;line-height:1;letter-spacing:-0.03em;margin-bottom:32px;">
        Python that<br><em style="color:var(--phosphor);">looks like</em><br>the UI it builds.
      </h2>
      <p class="reveal d2" style="font-size:16px;line-height:1.8;color:var(--chalk-2);max-width:400px;margin-bottom:48px;">
        No templates. No JSX. No YAML. Every component is a Python class with a chainable method API — so your UI code reads exactly like the interface it describes.
      </p>

      <!-- Mini feature list -->
      <div class="stagger reveal d3" style="display:flex;flex-direction:column;gap:16px;">
        <div style="display:flex;align-items:center;gap:16px;">
          <span style="font-family:var(--font-mono);font-size:16px;color:var(--phosphor);">✓</span>
          <span style="font-size:14px;color:var(--chalk-2);">Chainable <code style="font-family:var(--font-mono);color:var(--phosphor);font-size:12px;">.style().size().onClick()</code> builder pattern</span>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
          <span style="font-family:var(--font-mono);font-size:16px;color:var(--phosphor);">✓</span>
          <span style="font-size:14px;color:var(--chalk-2);">Full Python type hints — IDE autocomplete everywhere</span>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
          <span style="font-family:var(--font-mono);font-size:16px;color:var(--phosphor);">✓</span>
          <span style="font-size:14px;color:var(--chalk-2);">Reactive state with a single <code style="font-family:var(--font-mono);color:var(--phosphor);font-size:12px;">@reactive</code> decorator</span>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
          <span style="font-family:var(--font-mono);font-size:16px;color:var(--phosphor);">✓</span>
          <span style="font-size:14px;color:var(--chalk-2);">Zero boilerplate — scaffold a full app in 8 lines</span>
        </div>
      </div>
    </div>

    <!-- Right: Split code demo with tabs -->
    <div class="reveal d2">
      <!-- Tab bar -->
      <div style="display:flex;border-bottom:1px solid var(--border);margin-bottom:0;gap:0;" id="code-tabs">
        <button onclick="switchTab('counter')" id="tab-counter"
          style="font-family:var(--font-mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;padding:14px 24px;border:none;background:transparent;color:var(--phosphor);border-bottom:2px solid var(--phosphor);cursor:none;transition:all 0.3s;">
          counter.py
        </button>
        <button onclick="switchTab('dashboard')" id="tab-dashboard"
          style="font-family:var(--font-mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;padding:14px 24px;border:none;background:transparent;color:var(--chalk-3);border-bottom:2px solid transparent;cursor:none;transition:all 0.3s;">
          dashboard.py
        </button>
        <button onclick="switchTab('theme')" id="tab-theme"
          style="font-family:var(--font-mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;padding:14px 24px;border:none;background:transparent;color:var(--chalk-3);border-bottom:2px solid transparent;cursor:none;transition:all 0.3s;">
          theme.py
        </button>
      </div>

      <!-- Code panels -->
      <div id="panel-counter" class="code-win" style="border-top:none;border-radius:0 0 12px 12px;">
        <div class="code-body">
          <div><span class="tok-kw">from</span> <span class="tok-acc">pyui</span> <span class="tok-kw">import</span> <span class="tok-cls">App</span>, <span class="tok-cls">Page</span>, <span class="tok-cls">Button</span>, <span class="tok-cls">Text</span>, <span class="tok-fn">reactive</span></div>
          <div>&nbsp;</div>
          <div><span class="tok-kw">class</span> <span class="tok-cls">Counter</span>(<span class="tok-cls">App</span>):</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cmt"># One line of state. That's all.</span></div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-acc">count</span> = <span class="tok-fn">reactive</span>(<span class="tok-num">0</span>)</div>
          <div>&nbsp;</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">home</span> = <span class="tok-cls">Page</span>(<span class="tok-str">title=</span><span class="tok-str">"Counter"</span>)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">home</span>.<span class="tok-fn">add</span>(</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Text</span>(<span class="tok-kw">lambda</span>: <span class="tok-str">f"Count: </span><span class="tok-pct">{Counter.count}</span><span class="tok-str">"</span>),</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Button</span>(<span class="tok-str">"+"</span>).<span class="tok-fn">style</span>(<span class="tok-str">"primary"</span>)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.<span class="tok-fn">onClick</span>(<span class="tok-kw">lambda</span>: <span class="tok-cls">Counter</span>.<span class="tok-acc">count</span>.<span class="tok-fn">set</span>(<span class="tok-cls">Counter</span>.<span class="tok-acc">count</span> + <span class="tok-num">1</span>))</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;)</div>
        </div>
      </div>

      <div id="panel-dashboard" class="code-win" style="display:none;border-top:none;border-radius:0 0 12px 12px;">
        <div class="code-body">
          <div><span class="tok-kw">from</span> <span class="tok-acc">pyui</span> <span class="tok-kw">import</span> <span class="tok-cls">App</span>, <span class="tok-cls">Page</span>, <span class="tok-cls">Grid</span>, <span class="tok-cls">Stat</span>, <span class="tok-cls">Chart</span>, <span class="tok-cls">Table</span></div>
          <div>&nbsp;</div>
          <div><span class="tok-kw">class</span> <span class="tok-cls">Dashboard</span>(<span class="tok-cls">App</span>):</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">main</span> = <span class="tok-cls">Page</span>(<span class="tok-str">layout=</span><span class="tok-str">"sidebar"</span>)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">main</span>.<span class="tok-fn">add</span>(</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Grid</span>(<span class="tok-fn">cols</span>=<span class="tok-num">4</span>).<span class="tok-fn">add</span>(</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Stat</span>(<span class="tok-str">label=</span><span class="tok-str">"Revenue"</span>, <span class="tok-str">value=</span><span class="tok-str">"$128k"</span>, <span class="tok-str">trend=</span><span class="tok-str">"up"</span>),</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Stat</span>(<span class="tok-str">label=</span><span class="tok-str">"Users"</span>,   <span class="tok-str">value=</span><span class="tok-str">"4,821"</span>, <span class="tok-str">trend=</span><span class="tok-str">"up"</span>),</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Stat</span>(<span class="tok-str">label=</span><span class="tok-str">"Churn"</span>,  <span class="tok-str">value=</span><span class="tok-str">"1.2%"</span>,  <span class="tok-str">trend=</span><span class="tok-str">"down"</span>)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;),</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cls">Chart</span>(<span class="tok-str">type=</span><span class="tok-str">"area"</span>, <span class="tok-str">data=</span>revenue_data)</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;)</div>
        </div>
      </div>

      <div id="panel-theme" class="code-win" style="display:none;border-top:none;border-radius:0 0 12px 12px;">
        <div class="code-body">
          <div><span class="tok-kw">from</span> <span class="tok-acc">pyui</span> <span class="tok-kw">import</span> <span class="tok-cls">App</span></div>
          <div>&nbsp;</div>
          <div><span class="tok-kw">class</span> <span class="tok-cls">MyApp</span>(<span class="tok-cls">App</span>):</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cmt"># Built-in themes</span></div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">theme</span> = <span class="tok-str">"dark"</span>  <span class="tok-cmt"># or "ocean", "forest", "sunset"</span></div>
          <div>&nbsp;</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-cmt"># Or go fully custom:</span></div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-fn">theme</span> = {</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-str">"color.primary"</span>:    <span class="tok-str">"#6C63FF"</span>,</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-str">"color.background"</span>: <span class="tok-str">"#0A0A0A"</span>,</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-str">"font.family"</span>:      <span class="tok-str">"Geist"</span>,</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tok-str">"radius.md"</span>:        <span class="tok-str">"12px"</span>,</div>
          <div>&nbsp;&nbsp;&nbsp;&nbsp;}</div>
        </div>
      </div>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 5. STATS ROW
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section style="border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:var(--obsidian-2);">
  <div style="max-width:1400px;margin:0 auto;padding:0 48px;display:grid;grid-template-columns:repeat(4,1fr);">

    <div class="stat-card reveal d1" style="border-right:1px solid var(--border);padding-right:48px;">
      <div class="stat-num" id="stat-1">0.002</div>
      <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-top:8px;">Compile latency (ms)</div>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--phosphor);margin-top:8px;">↗ vs React: 0 DOM diff overhead</div>
    </div>

    <div class="stat-card reveal d2" style="border-right:1px solid var(--border);padding:40px 48px;">
      <div class="stat-num" id="stat-2">3×</div>
      <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-top:8px;">Output targets</div>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--phosphor);margin-top:8px;">Web · Desktop · CLI</div>
    </div>

    <div class="stat-card reveal d3" style="border-right:1px solid var(--border);padding:40px 48px;">
      <div class="stat-num" id="stat-3">40+</div>
      <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-top:8px;">Built-in components</div>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--phosphor);margin-top:8px;">Production-ready on day one</div>
    </div>

    <div class="stat-card reveal d4" style="padding:40px 0 40px 48px;">
      <div class="stat-num" id="stat-4">8</div>
      <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-top:8px;">Lines to a full app</div>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--phosphor);margin-top:8px;">Hello world in 60 seconds</div>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 6. TARGETS SECTION — THE THREE RENDERERS
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section id="targets" style="padding:160px 48px;max-width:1400px;margin:0 auto;">

  <div class="section-num reveal" style="margin-bottom:80px;">
    <span>02 — One Codebase. Three Targets.</span>
  </div>

  <h2 class="reveal d1" style="font-family:var(--font-display);font-size:clamp(40px,5vw,72px);font-weight:900;line-height:1;letter-spacing:-0.03em;margin-bottom:80px;">
    The same 12 lines<br>render <em style="color:var(--phosphor);">everywhere.</em>
  </h2>

  <!-- Three renderer cards -->
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);">

    <!-- Web -->
    <div class="feat-card reveal d1" style="background:var(--obsidian);border:none;">
      <div class="feat-icon">🌐</div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <span style="font-family:var(--font-display);font-size:28px;font-weight:900;color:var(--chalk);">Web</span>
        <span class="tag green" style="font-size:9px;">Stable</span>
      </div>
      <p style="font-size:13px;line-height:1.8;color:var(--chalk-3);margin-bottom:28px;">
        Compiles to clean HTML + Tailwind CSS + Alpine.js. Lighthouse score > 90 out of the box. Static builds that deploy to Vercel, Netlify, or bare nginx in one command.
      </p>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);border-top:1px solid var(--border);padding-top:20px;display:flex;flex-direction:column;gap:8px;">
        <div><span style="color:var(--phosphor);">$</span> pyui run --web</div>
        <div><span style="color:var(--phosphor);">$</span> pyui build --web --out ./dist</div>
      </div>
    </div>

    <!-- Desktop -->
    <div class="feat-card reveal d2" style="background:var(--obsidian);border:none;">
      <div class="feat-icon">🖥</div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <span style="font-family:var(--font-display);font-size:28px;font-weight:900;color:var(--chalk);">Desktop</span>
        <span class="tag orange" style="font-size:9px;">Beta</span>
      </div>
      <p style="font-size:13px;line-height:1.8;color:var(--chalk-3);margin-bottom:28px;">
        Renders as a native window via tkinter (zero deps) or PyQt6 for richer widgets. Ships as a standalone .exe or .app via PyInstaller. Windows, macOS, Linux.
      </p>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);border-top:1px solid var(--border);padding-top:20px;display:flex;flex-direction:column;gap:8px;">
        <div><span style="color:var(--phosphor);">$</span> pyui run --desktop</div>
        <div><span style="color:var(--phosphor);">$</span> pyui build --desktop  <span style="color:var(--chalk-3);"># → .exe</span></div>
      </div>
    </div>

    <!-- CLI -->
    <div class="feat-card reveal d3" style="background:var(--obsidian);border:none;">
      <div class="feat-icon">⌨</div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <span style="font-family:var(--font-display);font-size:28px;font-weight:900;color:var(--chalk);">Terminal</span>
        <span class="tag" style="font-size:9px;">Alpha</span>
      </div>
      <p style="font-size:13px;line-height:1.8;color:var(--chalk-3);margin-bottom:28px;">
        Renders a full TUI using Rich + prompt_toolkit. Tables, charts, forms — all in the terminal. Perfect for internal tools and developer dashboards.
      </p>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);border-top:1px solid var(--border);padding-top:20px;display:flex;flex-direction:column;gap:8px;">
        <div><span style="color:var(--phosphor);">$</span> pyui run --cli</div>
        <div><span style="color:var(--phosphor);">$</span> pyui run --cli --no-color</div>
      </div>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 7. FEATURES GRID — 2×3 BENTO
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section id="features" style="padding:0 48px 160px;max-width:1400px;margin:0 auto;">

  <div class="section-num reveal" style="margin-bottom:80px;">
    <span>03 — What's Inside</span>
  </div>

  <!-- BENTO GRID -->
  <div style="display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:auto;gap:16px;">

    <!-- Big card: Reactive State -->
    <div class="reveal d1 grad-border" style="grid-column:span 7;padding:56px;background:var(--obsidian-3);border-radius:12px;position:relative;overflow:hidden;">
      <!-- BG glow -->
      <div style="position:absolute;top:-80px;right:-80px;width:300px;height:300px;background:radial-gradient(circle,rgba(0,255,136,0.06) 0%,transparent 70%);pointer-events:none;"></div>

      <span class="label" style="margin-bottom:20px;display:block;">Reactive State</span>
      <h3 style="font-family:var(--font-display);font-size:40px;font-weight:900;line-height:1;letter-spacing:-0.02em;margin-bottom:24px;">
        State that just<br><em style="color:var(--phosphor);">works.</em>
      </h3>
      <p style="font-size:14px;line-height:1.8;color:var(--chalk-3);max-width:360px;margin-bottom:36px;">
        Declare a reactive variable. Bind it to a component. Every update propagates automatically — no stores, no reducers, no boilerplate.
      </p>

      <!-- Live mini demo -->
      <div style="background:var(--obsidian);border:1px solid var(--border);border-radius:8px;padding:20px 24px;font-family:var(--font-mono);font-size:12px;line-height:2;">
        <span class="tok-acc">count</span> = <span class="tok-fn">reactive</span>(<span class="tok-num">0</span>)
        <br>
        <span class="tok-cls">Text</span>(<span class="tok-kw">lambda</span>: <span class="tok-str">f"</span><span class="tok-pct">{count}</span> <span class="tok-str">clicks"</span>)
        <span style="color:var(--chalk-3);font-size:10px;"> &lt;!-- auto-updates --&gt;</span>
      </div>
    </div>

    <!-- Small card: Hot Reload -->
    <div class="feat-card reveal d2" style="grid-column:span 5;border-radius:12px;">
      <div class="feat-icon">⚡</div>
      <span class="label" style="margin-bottom:12px;display:block;">Hot Reload</span>
      <h3 style="font-family:var(--font-display);font-size:28px;font-weight:900;line-height:1;letter-spacing:-0.02em;margin-bottom:16px;">
        &lt;200ms<br>save → refresh
      </h3>
      <p style="font-size:13px;line-height:1.7;color:var(--chalk-3);">
        watchdog monitors files. IR diffing sends only what changed. Browser patches the DOM without a full reload.
      </p>
    </div>

    <!-- Small card: Theme Engine -->
    <div class="feat-card reveal d3" style="grid-column:span 4;border-radius:12px;">
      <div class="feat-icon">🎨</div>
      <span class="label" style="margin-bottom:12px;display:block;">Theme Engine</span>
      <h3 style="font-family:var(--font-display);font-size:28px;font-weight:900;line-height:1;letter-spacing:-0.02em;margin-bottom:16px;">
        6 themes.<br>Infinitely custom.
      </h3>
      <p style="font-size:13px;line-height:1.7;color:var(--chalk-3);">
        Design tokens all the way down. Override any token — one line of Python, entire app re-themes.
      </p>
      <div style="display:flex;gap:8px;margin-top:20px;flex-wrap:wrap;">
        <span style="width:20px;height:20px;border-radius:50%;background:#6C63FF;display:inline-block;border:2px solid var(--border);"></span>
        <span style="width:20px;height:20px;border-radius:50%;background:#0EA5E9;display:inline-block;border:2px solid var(--border);"></span>
        <span style="width:20px;height:20px;border-radius:50%;background:#10B981;display:inline-block;border:2px solid var(--border);"></span>
        <span style="width:20px;height:20px;border-radius:50%;background:#F97316;display:inline-block;border:2px solid var(--border);"></span>
        <span style="width:20px;height:20px;border-radius:50%;background:#F43F5E;display:inline-block;border:2px solid var(--border);"></span>
        <span style="width:20px;height:20px;border-radius:50%;background:#0F172A;display:inline-block;border:2px solid var(--border-bright);"></span>
      </div>
    </div>

    <!-- Small card: Component Marketplace -->
    <div class="feat-card reveal d4" style="grid-column:span 4;border-radius:12px;">
      <div class="feat-icon">📦</div>
      <span class="label" style="margin-bottom:12px;display:block;">Marketplace</span>
      <h3 style="font-family:var(--font-display);font-size:28px;font-weight:900;line-height:1;letter-spacing:-0.02em;margin-bottom:16px;">
        pip install<br>your next widget.
      </h3>
      <p style="font-size:13px;line-height:1.7;color:var(--chalk-3);">
        Community components land in your app like built-ins. No wiring, no config.
      </p>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--phosphor);margin-top:16px;display:flex;flex-direction:column;gap:6px;">
        <div>pip install pyui-charts</div>
        <div>pip install pyui-maps</div>
        <div>pip install pyui-auth</div>
      </div>
    </div>

    <!-- Small card: Type Safety -->
    <div class="feat-card reveal d5" style="grid-column:span 4;border-radius:12px;">
      <div class="feat-icon">🔒</div>
      <span class="label" style="margin-bottom:12px;display:block;">Type Safety</span>
      <h3 style="font-family:var(--font-display);font-size:28px;font-weight:900;line-height:1;letter-spacing:-0.02em;margin-bottom:16px;">
        mypy strict.<br>All the way down.
      </h3>
      <p style="font-size:13px;line-height:1.7;color:var(--chalk-3);">
        Every component prop is typed. Your IDE knows exactly what goes where — before you run a single line.
      </p>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 8. COMPARE SECTION — VS TABLE
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section id="compare" style="padding:160px 48px;border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:var(--obsidian-2);">
  <div style="max-width:1400px;margin:0 auto;">

    <div class="section-num reveal" style="margin-bottom:80px;">
      <span>04 — Why Not the Others</span>
    </div>

    <h2 class="reveal d1" style="font-family:var(--font-display);font-size:clamp(40px,5vw,72px);font-weight:900;line-height:1;letter-spacing:-0.03em;margin-bottom:80px;">
      Everything else<br>is <em style="color:var(--chalk-3);">half</em> a solution.
    </h2>

    <div class="reveal d2" style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="border-bottom:1px solid var(--border-bright);">
            <th style="text-align:left;padding:16px 24px 16px 0;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);font-weight:400;width:200px;"></th>
            <th style="padding:16px 24px;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--phosphor);font-weight:700;background:rgba(0,255,136,0.04);border-radius:8px 8px 0 0;">PyUI</th>
            <th style="padding:16px 24px;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);font-weight:400;">Streamlit</th>
            <th style="padding:16px 24px;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);font-weight:400;">Flet</th>
            <th style="padding:16px 24px;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);font-weight:400;">Dash</th>
            <th style="padding:16px 24px;font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);font-weight:400;">tkinter</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Web output</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Desktop output</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Terminal / CLI output</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Reactive state built-in</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Hot reload</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Beautiful defaults</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.03);"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--gold);font-size:12px;">Partial</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
          <tr>
            <td style="padding:20px 24px 20px 0;font-size:13px;color:var(--chalk-2);">Zero JS/HTML knowledge</td>
            <td style="padding:20px 24px;text-align:center;background:rgba(0,255,136,0.04);border-radius:0 0 8px 8px;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--phosphor);font-size:16px;">✓</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
            <td style="padding:20px 24px;text-align:center;"><span style="color:var(--chalk-3);font-size:16px;">✗</span></td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 9. TESTIMONIALS / QUOTE STRIP
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section style="padding:160px 48px;max-width:1400px;margin:0 auto;">

  <div class="section-num reveal" style="margin-bottom:80px;">
    <span>05 — Early Adopters</span>
  </div>

  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:32px;">

    <div class="reveal d1" style="border:1px solid var(--border);border-radius:12px;padding:40px;background:var(--obsidian-2);position:relative;">
      <div style="font-family:var(--font-display);font-size:72px;line-height:0.7;color:var(--phosphor);opacity:0.2;position:absolute;top:24px;left:32px;">"</div>
      <p style="font-size:15px;line-height:1.8;color:var(--chalk-2);margin-bottom:28px;position:relative;z-index:1;">
        I built our entire ML dashboard in PyUI in a single afternoon. No frontend dev needed. It just compiled to a clean web app.
      </p>
      <div style="display:flex;align-items:center;gap:12px;border-top:1px solid var(--border);padding-top:24px;">
        <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--phosphor),var(--blue));"></div>
        <div>
          <div style="font-family:var(--font-mono);font-size:11px;font-weight:700;color:var(--chalk);">Ayesha R.</div>
          <div style="font-family:var(--font-mono);font-size:9px;color:var(--chalk-3);letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;">ML Engineer · Karachi</div>
        </div>
      </div>
    </div>

    <div class="reveal d2" style="border:1px solid var(--border);border-radius:12px;padding:40px;background:var(--obsidian-2);position:relative;">
      <div style="font-family:var(--font-display);font-size:72px;line-height:0.7;color:var(--phosphor);opacity:0.2;position:absolute;top:24px;left:32px;">"</div>
      <p style="font-size:15px;line-height:1.8;color:var(--chalk-2);margin-bottom:28px;position:relative;z-index:1;">
        The reactive state system is the cleanest I've used in any language. It just disappears into the background and lets you think about the product.
      </p>
      <div style="display:flex;align-items:center;gap:12px;border-top:1px solid var(--border);padding-top:24px;">
        <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--purple),var(--orange));"></div>
        <div>
          <div style="font-family:var(--font-mono);font-size:11px;font-weight:700;color:var(--chalk);">Marcus T.</div>
          <div style="font-family:var(--font-mono);font-size:9px;color:var(--chalk-3);letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;">Backend Engineer · Berlin</div>
        </div>
      </div>
    </div>

    <div class="reveal d3" style="border:1px solid var(--border);border-radius:12px;padding:40px;background:var(--obsidian-2);position:relative;">
      <div style="font-family:var(--font-display);font-size:72px;line-height:0.7;color:var(--phosphor);opacity:0.2;position:absolute;top:24px;left:32px;">"</div>
      <p style="font-size:15px;line-height:1.8;color:var(--chalk-2);margin-bottom:28px;position:relative;z-index:1;">
        This is what I wanted Tkinter to be in 2026. Finally an admin tool that doesn't look like it was designed in 1998.
      </p>
      <div style="display:flex;align-items:center;gap:12px;border-top:1px solid var(--border);padding-top:24px;">
        <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--gold),var(--orange));"></div>
        <div>
          <div style="font-family:var(--font-mono);font-size:11px;font-weight:700;color:var(--chalk);">Priya S.</div>
          <div style="font-family:var(--font-mono);font-size:9px;color:var(--chalk-3);letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;">Data Scientist · Bangalore</div>
        </div>
      </div>
    </div>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 10. CTA — TERMINAL STYLE CLOSER
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<section style="position:relative;overflow:hidden;border-top:1px solid var(--border);">

  <!-- Grid bg -->
  <div class="grid-bg noise" style="position:absolute;inset:0;opacity:0.4;"></div>

  <!-- Radial glow -->
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:800px;height:400px;background:radial-gradient(ellipse,rgba(0,255,136,0.06) 0%,transparent 70%);pointer-events:none;"></div>

  <div style="max-width:1400px;margin:0 auto;padding:160px 48px;position:relative;z-index:1;text-align:center;">

    <span class="label reveal" style="margin-bottom:32px;display:block;">Ready to build?</span>

    <h2 class="reveal d1" style="font-family:var(--font-display);font-size:clamp(56px,9vw,120px);font-weight:900;line-height:0.9;letter-spacing:-0.04em;margin-bottom:64px;">
      Your next app<br>starts with<br><em style="color:var(--phosphor);" class="caret">one import</em>
    </h2>

    <!-- Terminal block -->
    <div class="reveal d2 code-win glow-phosphor" style="max-width:600px;margin:0 auto 64px;text-align:left;">
      <div class="code-win-bar">
        <div class="code-dot" style="background:#ff5f56;"></div>
        <div class="code-dot" style="background:#ffbd2e;"></div>
        <div class="code-dot" style="background:#27c93f;"></div>
        <span style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);margin-left:8px;">Terminal</span>
      </div>
      <div class="code-body">
        <div><span style="color:var(--chalk-3);">~</span> <span style="color:var(--phosphor);">$</span> pip install pyui-framework</div>
        <div><span style="color:var(--chalk-3);">~</span> <span style="color:var(--phosphor);">$</span> pyui new my-app</div>
        <div><span style="color:var(--chalk-3);">~</span> <span style="color:var(--phosphor);">$</span> cd my-app && pyui run</div>
        <div style="color:var(--phosphor);margin-top:8px;">
          ✓ Dev server running at <span style="text-decoration:underline;">http://localhost:8000</span>
        </div>
      </div>
    </div>

    <div class="reveal d3" style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">
      <a href="#" class="btn-primary"><span>→ Get Started Free</span></a>
      <a href="#" class="btn-ghost">Read the Docs</a>
      <a href="#" class="btn-ghost">⭐ Star on GitHub</a>
    </div>

    <p class="reveal d4" style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);margin-top:32px;letter-spacing:0.1em;">
      MIT Licensed · Python 3.10+ · No credit card required
    </p>

  </div>
</section>
""")

        # ══════════════════════════════════════════════════════════════════
        # 11. FOOTER
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<footer style="border-top:1px solid var(--border);background:var(--obsidian);">
  <div style="max-width:1400px;margin:0 auto;padding:80px 48px 48px;">

    <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;margin-bottom:80px;">

      <div>
        <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:20px;">
          <span style="font-family:var(--font-display);font-size:20px;font-weight:900;color:var(--chalk);">Py</span>
          <span style="font-family:var(--font-mono);font-size:20px;font-weight:700;color:var(--phosphor);">UI</span>
        </div>
        <p style="font-size:13px;line-height:1.8;color:var(--chalk-3);max-width:280px;margin-bottom:24px;">
          The Python UI framework that compiles to web, desktop, and terminal — from a single, beautiful API.
        </p>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);">
          <span style="color:var(--phosphor);">$</span> pip install pyui-framework
        </div>
      </div>

      <div>
        <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-bottom:20px;">Product</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Documentation</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Components</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Changelog</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Roadmap</a>
        </div>
      </div>

      <div>
        <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-bottom:20px;">Community</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">GitHub</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Discord</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Twitter / X</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Blog</a>
        </div>
      </div>

      <div>
        <div style="font-family:var(--font-mono);font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:var(--chalk-3);margin-bottom:20px;">Legal</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">MIT License</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Privacy Policy</a>
          <a href="#" style="font-size:13px;color:var(--chalk-2);text-decoration:none;transition:color 0.3s;">Contributing</a>
        </div>
      </div>

    </div>

    <div style="border-top:1px solid var(--border);padding-top:40px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
      <span style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);letter-spacing:0.1em;">
        © 2026 PyUI Foundation. Built with PyUI. MIT Licensed.
      </span>
      <span style="font-family:var(--font-mono);font-size:10px;color:var(--chalk-3);letter-spacing:0.1em;">
        v0.3.0-beta &nbsp;·&nbsp; <span style="color:var(--phosphor);">●</span> All systems operational
      </span>
    </div>

  </div>
</footer>
""")

        # ══════════════════════════════════════════════════════════════════
        # JS — CURSOR, SCROLL REVEALS, TABS, COUNTERS, HERO CYCLE
        # ══════════════════════════════════════════════════════════════════
        Text("").inject_html("""
<script>
// ── Custom cursor
const ring = document.getElementById('cursor-ring');
const dot  = document.getElementById('cursor-dot');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  dot.style.left = mx + 'px';
  dot.style.top  = my + 'px';
});

function animateCursor() {
  rx += (mx - rx) * 0.14;
  ry += (my - ry) * 0.14;
  ring.style.left = rx + 'px';
  ring.style.top  = ry + 'px';
  requestAnimationFrame(animateCursor);
}
animateCursor();

// ── Scroll reveals
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in-view'); }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
  observer.observe(el);
});

// ── Code tabs
function switchTab(name) {
  ['counter','dashboard','theme'].forEach(t => {
    document.getElementById('panel-' + t).style.display = t === name ? 'block' : 'none';
    const tab = document.getElementById('tab-' + t);
    tab.style.color = t === name ? 'var(--phosphor)' : 'var(--chalk-3)';
    tab.style.borderBottomColor = t === name ? 'var(--phosphor)' : 'transparent';
  });
}

// ── Hero target cycling
const targets = ['Everything.', 'Web Apps.', 'Desktop Apps.', 'CLI Tools.', 'Dashboards.', 'Admin Panels.'];
let ti = 0;
const cycleEl = document.getElementById('target-cycle');

function cycleTarget() {
  if (!cycleEl) return;
  cycleEl.style.opacity = '0';
  cycleEl.style.transform = 'translateY(16px)';
  setTimeout(() => {
    ti = (ti + 1) % targets.length;
    cycleEl.textContent = targets[ti];
    cycleEl.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    cycleEl.style.opacity = '1';
    cycleEl.style.transform = 'translateY(0)';
  }, 300);
}
setInterval(cycleTarget, 2400);
cycleEl.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

// ── Hero headline entrance
['hero-line-1','hero-line-2','hero-line-3'].forEach((id, i) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.opacity = '0';
  el.style.transform = 'translateY(48px)';
  el.style.transition = `opacity 1s ${0.1 + i * 0.15}s cubic-bezier(0.16,1,0.3,1), transform 1s ${0.1 + i * 0.15}s cubic-bezier(0.16,1,0.3,1)`;
  setTimeout(() => { el.style.opacity = '1'; el.style.transform = 'translateY(0)'; }, 100);
});

// ── Nav link hover colour
document.querySelectorAll('nav a').forEach(a => {
  a.addEventListener('mouseenter', () => { if (!a.classList.contains('btn-primary') && !a.classList.contains('btn-ghost')) a.style.color = 'var(--chalk)'; });
  a.addEventListener('mouseleave', () => { if (!a.classList.contains('btn-primary') && !a.classList.contains('btn-ghost')) a.style.color = 'var(--chalk-3)'; });
});

// ── Footer link hover
document.querySelectorAll('footer a').forEach(a => {
  a.addEventListener('mouseenter', () => a.style.color = 'var(--phosphor)');
  a.addEventListener('mouseleave', () => a.style.color = 'var(--chalk-2)');
});

// ── Progress bar on scroll
const progressEl = document.createElement('div');
progressEl.style.cssText = 'position:fixed;top:0;left:0;height:2px;background:var(--phosphor);z-index:9997;transition:width 0.1s linear;width:0;';
document.body.appendChild(progressEl);
window.addEventListener('scroll', () => {
  const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100;
  progressEl.style.width = Math.min(pct, 100) + '%';
});
</script>
""")


class PortfolioApp(App):
    name = "PyUI — Write Python. Ship Everything."
    index = PortfolioPage()

    @classmethod
    def toggle_theme(cls) -> None:
        pass  # Theme toggle wired in Phase 5


if __name__ == "__main__":
    from pyui.server.dev_server import run_dev_server

    run_dev_server(PortfolioApp, port=9011)
