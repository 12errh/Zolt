"""
Custom CSS for the agency landing page.
Injected via App.extra_css into the page <style> block.
"""

AGENCY_CSS = """
/* ── Google Fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&display=swap');

/* ── Font utilities ───────────────────────────────────────────── */
.font-heading { font-family: 'Instrument Serif', serif; font-style: italic; }
.font-body    { font-family: 'Barlow', sans-serif; }

/* ── Liquid glass — subtle ────────────────────────────────────── */
.liquid-glass {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0)    40%,
    rgba(255,255,255,0)    60%,
    rgba(255,255,255,0.15) 80%,
    rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box,
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

/* ── Liquid glass — strong ────────────────────────────────────── */
.liquid-glass-strong {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  border: none;
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05),
              inset 0 1px 1px rgba(255,255,255,0.15);
  position: relative;
  overflow: hidden;
}
.liquid-glass-strong::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.5)  0%,
    rgba(255,255,255,0.2)  20%,
    rgba(255,255,255,0)    40%,
    rgba(255,255,255,0)    60%,
    rgba(255,255,255,0.2)  80%,
    rgba(255,255,255,0.5)  100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box,
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

/* ── Video section helpers ────────────────────────────────────── */
.video-section { position: relative; overflow: hidden; }
.video-section video {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover; z-index: 0;
}
.video-fade-top {
  position: absolute; top: 0; left: 0; right: 0;
  height: 200px; z-index: 1; pointer-events: none;
  background: linear-gradient(to bottom, black, transparent);
}
.video-fade-bottom {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 200px; z-index: 1; pointer-events: none;
  background: linear-gradient(to top, black, transparent);
}
.video-fade-hero {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 300px; z-index: 1; pointer-events: none;
  background: linear-gradient(to top, black, transparent);
}

/* ── Blur-in animation ────────────────────────────────────────── */
@keyframes blurIn {
  from { filter: blur(10px); opacity: 0; transform: translateY(20px); }
  to   { filter: blur(0px);  opacity: 1; transform: translateY(0); }
}
.blur-in {
  animation: blurIn 0.6s cubic-bezier(0.16,1,0.3,1) both;
}
.blur-in-delay-1 { animation-delay: 0.8s; }
.blur-in-delay-2 { animation-delay: 1.1s; }

/* ── Word-by-word blur reveal ─────────────────────────────────── */
@keyframes wordReveal {
  0%   { filter: blur(10px); opacity: 0; transform: translateY(50px); }
  50%  { filter: blur(5px);  opacity: 0.5; transform: translateY(-5px); }
  100% { filter: blur(0px);  opacity: 1; transform: translateY(0); }
}
.word-reveal span {
  display: inline-block;
  animation: wordReveal 0.7s cubic-bezier(0.16,1,0.3,1) both;
}

/* ── Desaturate filter for stats video ───────────────────────── */
.desaturate { filter: saturate(0); }

/* ── Navbar pill ──────────────────────────────────────────────── */
.nav-pill {
  position: fixed; top: 1rem; left: 0; right: 0;
  z-index: 50; padding: 0.75rem 4rem;
  display: flex; align-items: center; justify-content: space-between;
}

/* ── Section spacing ──────────────────────────────────────────── */
.agency-section {
  padding: 6rem 4rem;
  position: relative;
}
"""
