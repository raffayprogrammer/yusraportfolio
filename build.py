# -*- coding: utf-8 -*-
"""Build index.html from .content.json.

Design: Swiss Modernism — "Technical Index".
Paper and ink, one cobalt accent, a 12-column grid, and the work presented as a
numbered index of rows rather than a card wall. Deliberately light-first so it
reads nothing like the dark portfolio this content was previously styled as.

Run:  python build.py
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(io.open(os.path.join(HERE, ".content.json"), encoding="utf-8"))

sys.path.insert(0, r"C:\brag-yusra\work")
from films import FILMS  # demo titles / blurbs / stack

SITE = dict(
    name="Yusra Khan",
    role="AI Automation Engineer",
    lede=("I turn loosely defined business problems into automation architecture — document "
          "processing, CRM workflows, voice agents and content pipelines that run reliably "
          "without anyone watching them."),
    email="iyusrak@gmail.com",
    linkedin="https://linkedin.com/in/yusra-khan/",
    github="https://github.com/iyusrakhan",
)

ABOUT = [
 "I'm an AI automation engineer. My work sits where n8n, third-party APIs, AI models and cloud "
 "platforms meet — mapping how disconnected systems actually depend on each other, then wiring "
 "them together so the process runs without anyone supervising it.",
 "Most of what I build is applied rather than experimental: OCR and document processing, CRM "
 "workflows, voice agents, scheduling, content pipelines, reporting. Real business operations, "
 "with testing protocols behind them, because the failure mode of an unattended system is that "
 "nobody notices it stopped.",
 "The part I find most interesting is the translation step — taking a problem someone has "
 "described loosely, working out what the system actually has to guarantee, and designing around "
 "the places where an API will quietly return the wrong thing rather than an error.",
]

CSS = """
/* ── Tokens ───────────────────────────────────────────────────────────
   Light-first. The dark block only restates tokens, so every component
   below styles through them and never hardcodes a colour.
─────────────────────────────────────────────────────────────────────── */
:root{
  --paper:#f6f6f4;
  --paper-2:#efefec;
  --ink:#0c0c0d;
  --graphite:#5a5c60;
  --faint:#8b8d93;
  --rule:#dededa;
  --rule-strong:#c6c6c0;
  --accent:#1a3fcb;
  --accent-soft:#e8ecfb;

  --display:"Familjen Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;

  --gut:clamp(1.25rem,4vw,2.5rem);
  --max:78rem;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#0f0f10; --paper-2:#17171a; --ink:#f2f2f0; --graphite:#a7a9af;
    --faint:#7e8086; --rule:#27272b; --rule-strong:#3a3a40;
    --accent:#8ea4ff; --accent-soft:#191d33;
  }
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:5rem}
body{
  background:var(--paper);color:var(--ink);font-family:var(--display);
  font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased;
  font-feature-settings:"ss01" 1;
}
ul,ol{list-style:none}
a{color:inherit;text-decoration:none}
img,video{display:block;max-width:100%}
::selection{background:var(--accent);color:#fff}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}

.wrap{max-width:var(--max);margin-inline:auto;padding-inline:var(--gut)}
.rule{border-top:1px solid var(--rule)}

/* ── Masthead ─────────────────────────────────────────────────────── */
.mast{
  position:sticky;top:0;z-index:60;background:var(--paper);
  border-bottom:1px solid var(--rule);
}
.mast-in{display:flex;align-items:center;justify-content:space-between;height:4rem;gap:1rem}
.wordmark{font-weight:700;letter-spacing:-.03em;font-size:1.0625rem}
.wordmark span{color:var(--accent)}
.navlinks{display:none;gap:.25rem;align-items:center}
@media (min-width:52rem){.navlinks{display:flex}}
.navlinks a{
  font-family:var(--mono);font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--graphite);padding:.5rem .7rem;transition:color .15s;
}
.navlinks a:hover{color:var(--ink)}
.navlinks a.cta{color:var(--accent)}
.menu-btn{
  display:flex;width:2.75rem;height:2.75rem;align-items:center;justify-content:center;
  border:1px solid var(--rule);background:none;color:var(--ink);cursor:pointer;
}
@media (min-width:52rem){.menu-btn{display:none}}
#mobnav{display:none;border-top:1px solid var(--rule)}
#mobnav.open{display:block}
#mobnav a{
  display:block;padding:.9rem 0;border-bottom:1px solid var(--rule);
  font-family:var(--mono);font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;
}
#mobnav a:last-child{border-bottom:0}

/* ── Type scale ───────────────────────────────────────────────────── */
h1,h2,h3{font-weight:700;letter-spacing:-.035em;line-height:1.02;text-wrap:balance}
h1{font-size:clamp(3rem,12vw,8.5rem)}
h2{font-size:clamp(2rem,5.5vw,3.5rem);letter-spacing:-.03em}
h3{font-size:1.25rem;letter-spacing:-.02em;line-height:1.2}
.lede{font-size:clamp(1.0625rem,2vw,1.375rem);line-height:1.5;color:var(--graphite);max-width:46ch;text-wrap:pretty}
.label{
  font-family:var(--mono);font-size:.6875rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--faint);
}
.label-accent{color:var(--accent)}

section{padding-block:clamp(4rem,9vw,7.5rem)}

/* section head: label in col 1, title in cols 2-12 (Swiss asymmetry) */
.shead{display:grid;gap:1rem 2rem;grid-template-columns:1fr}
@media (min-width:52rem){.shead{grid-template-columns:14rem 1fr}}
.shead .lede{margin-top:1rem}

/* ── Hero ─────────────────────────────────────────────────────────── */
.hero{padding-top:clamp(3rem,8vw,6rem);padding-bottom:clamp(3rem,7vw,5rem)}
.hero h1{margin-top:1.25rem}
.hero-role{
  font-family:var(--mono);font-size:clamp(.875rem,2vw,1.125rem);letter-spacing:.2em;
  text-transform:uppercase;color:var(--accent);margin-top:1.25rem;
}
.hero-grid{display:grid;gap:2.5rem;margin-top:2.5rem}
@media (min-width:52rem){.hero-grid{grid-template-columns:1fr 1fr;align-items:end}}
.actions{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}
.btn{
  display:inline-flex;align-items:center;gap:.6rem;min-height:2.75rem;padding:.75rem 1.4rem;
  background:var(--accent);color:#fff;font-weight:600;font-size:.9375rem;
  transition:opacity .15s;
}
.btn:hover{opacity:.86}
.btn-ghost{background:none;color:var(--ink);border:1px solid var(--rule-strong)}
.btn-ghost:hover{border-color:var(--ink);opacity:1}

/* stats as a ruled row, not boxes */
.stats{display:grid;grid-template-columns:1fr;border-top:1px solid var(--ink);margin-top:3.5rem}
@media (min-width:40rem){.stats{grid-template-columns:repeat(3,1fr)}}
.stat{padding:1.5rem 0;border-bottom:1px solid var(--rule)}
@media (min-width:40rem){
  .stat{padding:1.75rem 1.5rem 1.75rem 0;border-bottom:0;border-right:1px solid var(--rule)}
  .stat:last-child{border-right:0}
}
.stat b{display:block;font-family:var(--mono);font-size:clamp(2rem,5vw,3rem);font-weight:600;letter-spacing:-.04em;line-height:1}
.stat span{display:block;margin-top:.6rem;font-size:.9375rem;color:var(--graphite)}

/* ── Work index ───────────────────────────────────────────────────── */
.index{border-top:1px solid var(--ink);margin-top:3.5rem}
.row{
  display:grid;gap:.5rem 2rem;grid-template-columns:1fr;
  padding:2rem 0;border-bottom:1px solid var(--rule);
}
@media (min-width:52rem){.row{grid-template-columns:3.5rem 23rem 1fr;padding:2.5rem 0}}
.row-num{font-family:var(--mono);font-size:.8125rem;color:var(--accent);padding-top:.35rem}
.row-tag{margin-top:.5rem}
.row-media{margin-top:1.25rem}
.row-media video{width:100%;aspect-ratio:16/9;background:var(--paper-2);border:1px solid var(--rule);object-fit:cover}
.row p{color:var(--graphite);font-size:.9375rem;line-height:1.6;max-width:62ch}
.row .p2{margin-top:.75rem;color:var(--faint)}
.figs{display:flex;flex-wrap:wrap;gap:1.75rem;margin-top:1.25rem}
.figs b{display:block;font-family:var(--mono);font-size:1.0625rem;font-weight:600;color:var(--ink)}
.figs span{display:block;font-size:.75rem;color:var(--faint);margin-top:.2rem}
.pills{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.25rem}
.pills span{
  font-family:var(--mono);font-size:.6875rem;letter-spacing:.02em;color:var(--graphite);
  border:1px solid var(--rule);padding:.3rem .55rem;
}

/* ── Demos ────────────────────────────────────────────────────────── */
.demos{display:grid;gap:2.5rem 2rem;margin-top:3.5rem;grid-template-columns:1fr}
@media (min-width:52rem){.demos{grid-template-columns:repeat(2,1fr)}}
.demo video{width:100%;aspect-ratio:16/9;background:var(--paper-2);border:1px solid var(--rule);object-fit:cover}
.demo-meta{display:flex;gap:1rem;margin-top:1rem}
.demo-meta .n{font-family:var(--mono);font-size:.75rem;color:var(--accent);padding-top:.15rem}
.demo p{margin-top:.6rem;font-size:.9375rem;line-height:1.6;color:var(--graphite)}

/* ── Skills: label left, items right ──────────────────────────────── */
.kit{border-top:1px solid var(--ink);margin-top:3.5rem}
.kit-row{display:grid;gap:.75rem 2rem;grid-template-columns:1fr;padding:1.5rem 0;border-bottom:1px solid var(--rule)}
@media (min-width:52rem){.kit-row{grid-template-columns:14rem 1fr;align-items:baseline}}
.kit-items{display:flex;flex-wrap:wrap;gap:.4rem .5rem}
.kit-items li{font-size:.9375rem;color:var(--graphite)}
.kit-items li::after{content:"·";margin-left:.5rem;color:var(--rule-strong)}
.kit-items li:last-child::after{content:""}

/* ── Experience ───────────────────────────────────────────────────── */
.cv{border-top:1px solid var(--ink);margin-top:3.5rem}
.cv-row{display:grid;gap:.75rem 2rem;grid-template-columns:1fr;padding:2rem 0;border-bottom:1px solid var(--rule)}
@media (min-width:52rem){.cv-row{grid-template-columns:14rem 1fr}}
.cv-when{font-family:var(--mono);font-size:.75rem;color:var(--faint);letter-spacing:.04em}
.cv-org{color:var(--accent);font-size:.9375rem;margin-top:.3rem}
.cv-row h3{margin-top:.25rem}
.cv-points{margin-top:1rem;display:flex;flex-direction:column;gap:.5rem}
.cv-points li{font-size:.9375rem;line-height:1.6;color:var(--graphite);padding-left:1.1rem;position:relative;max-width:66ch}
.cv-points li::before{content:"";position:absolute;left:0;top:.65em;width:.4rem;height:1px;background:var(--rule-strong)}

/* ── Contact ──────────────────────────────────────────────────────── */
.contact h2{max-width:16ch}
.mail{
  display:inline-block;margin-top:2rem;font-family:var(--mono);
  font-size:clamp(1rem,3.2vw,1.75rem);color:var(--accent);
  border-bottom:2px solid var(--accent);padding-bottom:.2rem;word-break:break-all;
}
.elsewhere{display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:2.5rem}
.elsewhere a{font-family:var(--mono);font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;color:var(--graphite);border-bottom:1px solid var(--rule-strong);padding-bottom:.15rem}
.elsewhere a:hover{color:var(--ink);border-color:var(--ink)}

.foot{border-top:1px solid var(--rule);padding-block:2.5rem}
.foot-in{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;
         font-family:var(--mono);font-size:.75rem;color:var(--faint);letter-spacing:.04em}

/* ── Reveal ───────────────────────────────────────────────────────── */
.rv{opacity:0;transform:translateY(14px);transition:opacity .5s cubic-bezier(.16,1,.3,1),transform .5s cubic-bezier(.16,1,.3,1)}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rv{opacity:1;transform:none;transition:none}
  *,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}
"""

def page():
    P, S, E, ED, ST = C["projects"], C["skills"], C["experience"], C["education"], C["stats"]

    stats = "".join(
        '<div class="stat"><b>%s</b><span>%s</span></div>' % (v, d) for d, v in ST)

    rows = []
    for i, p in enumerate(P, 1):
        figs = "".join('<div><b>%s</b><span>%s</span></div>' % (a, b) for a, b in p["figures"])
        pills = "".join("<span>%s</span>" % x for x in p["pills"])
        rows.append(
            '<article class="row rv">'
            '<div class="row-num">%02d</div>'
            '<div><h3>%s</h3><p class="label row-tag">%s</p>'
            '<div class="row-media"><video controls preload="none" playsinline '
            'poster="demos/%s.png"><source src="demos/%s.mp4" type="video/mp4">'
            '</video></div></div>'
            '<div><p>%s</p>%s%s%s</div>'
            '</article>' % (i, p["title"], p["tag"],
                            FILMS[i-1]["slug"], FILMS[i-1]["slug"], p["p1"],
                            '<p class="p2">%s</p>' % p["p2"] if p["p2"] else "",
                            '<div class="figs">%s</div>' % figs if figs else "",
                            '<div class="pills">%s</div>' % pills if pills else ""))

    kit = "".join(
        '<div class="kit-row rv"><p class="label">%s</p>'
        '<ul class="kit-items">%s</ul></div>'
        % (g["name"], "".join("<li>%s</li>" % x for x in g["items"])) for g in S)

    cv = "".join(
        '<div class="cv-row rv"><div><p class="cv-when">%s</p><p class="cv-org">%s</p></div>'
        '<div><p class="label label-accent">%s</p><h3>%s</h3>'
        '<ul class="cv-points">%s</ul></div></div>'
        % (e["when"] or "&nbsp;", e["org"], e["kicker"], e["role"],
           "".join("<li>%s</li>" % x for x in e["points"])) for e in E)

    edu = "".join(
        '<div class="cv-row rv"><p class="label">%s</p>'
        '<div><h3>%s</h3><p class="cv-org">%s</p></div></div>'
        % (e["kicker"], e["title"], e["org"]) for e in ED)

    about = "".join('<p class="lede rv" style="max-width:60ch;margin-top:1.5rem">%s</p>' % a
                    for a in ABOUT)

    tpl = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{NAME}} &mdash; {{ROLE}}</title>
<meta name="description" content="AI Automation Engineer building production automation systems across document processing, CRM workflows, voice agents and content pipelines.">
<meta name="theme-color" content="#f6f6f4">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{{CSS}}</style>
</head>
<body>

<header class="mast">
  <div class="wrap mast-in">
    <a class="wordmark" href="#top">{{NAME}}<span>.</span></a>
    <nav class="navlinks" aria-label="Main">
      <a href="#work">Work</a><a href="#about">About</a>
      <a href="#kit">Toolkit</a><a href="#cv">Background</a><a class="cta" href="#contact">Contact</a>
    </nav>
    <button class="menu-btn" id="mb" aria-expanded="false" aria-controls="mobnav" aria-label="Menu">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </div>
  <div class="wrap" id="mobnav">
    <a href="#work">Work</a><a href="#about">About</a>
    <a href="#kit">Toolkit</a><a href="#cv">Background</a><a href="#contact">Contact</a>
  </div>
</header>

<main id="top">

  <section class="wrap hero">
    <p class="label">Portfolio &mdash; 2026</p>
    <h1>{{NAME}}</h1>
    <p class="hero-role">{{ROLE}}</p>
    <div class="hero-grid">
      <p class="lede">{{LEDE}}</p>
      <div class="actions">
        <a class="btn" href="#work">See the work</a>
        <a class="btn btn-ghost" href="#contact">Get in touch</a>
      </div>
    </div>
    <div class="stats">{{STATS}}</div>
  </section>

  <section class="wrap rule" id="work">
    <div class="shead rv">
      <p class="label">Selected work</p>
      <div><h2>Sixteen systems, built end to end</h2>
        <p class="lede">From the API call that starts the process to the moment a person stops doing the job by hand. Each one has a short film.</p></div>
    </div>
    <div class="index">{{ROWS}}</div>
  </section>

  <section class="wrap rule" id="about">
    <div class="shead">
      <p class="label rv">About</p>
      <div><h2 class="rv">The short version</h2>{{ABOUT}}</div>
    </div>
  </section>

  <section class="wrap rule" id="kit">
    <div class="shead rv">
      <p class="label">Toolkit</p>
      <div><h2>What I work with</h2>
        <p class="lede">Tools I've used to ship something real, not just read about.</p></div>
    </div>
    <div class="kit">{{KIT}}</div>
  </section>

  <section class="wrap rule" id="cv">
    <div class="shead rv">
      <p class="label">Background</p>
      <div><h2>Where I've been</h2></div>
    </div>
    <div class="cv">{{CV}}</div>
    <div class="shead rv" style="margin-top:4.5rem">
      <p class="label">Education</p>
      <div><h2>Where I studied</h2></div>
    </div>
    <div class="cv">{{EDU}}</div>
  </section>

  <section class="wrap rule contact" id="contact">
    <p class="label rv">Contact</p>
    <h2 class="rv" style="margin-top:1rem">Have a process that should run itself?</h2>
    <p class="lede rv" style="margin-top:1.5rem">I'm open to freelance and full-time work. The fastest way to reach me is email &mdash; I reply to everything.</p>
    <a class="mail rv" href="mailto:{{EMAIL}}">{{EMAIL}}</a>
    <div class="elsewhere rv">
      <a href="{{LINKEDIN}}" target="_blank" rel="noreferrer noopener">LinkedIn</a>
      <a href="{{GITHUB}}" target="_blank" rel="noreferrer noopener">GitHub</a>
    </div>
  </section>

</main>

<footer class="foot">
  <div class="wrap foot-in">
    <span>&copy; 2026 {{NAME}}</span>
    <span>{{ROLE}}</span>
  </div>
</footer>

<script>
(function(){
  var mb=document.getElementById('mb'),mn=document.getElementById('mobnav');
  mb.addEventListener('click',function(){
    var o=mn.classList.toggle('open');
    mb.setAttribute('aria-expanded',o?'true':'false');
  });
  mn.addEventListener('click',function(e){
    if(e.target.tagName==='A'){mn.classList.remove('open');mb.setAttribute('aria-expanded','false');}
  });
  var els=document.querySelectorAll('.rv');
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in');});return;}
  var io=new IntersectionObserver(function(en){
    en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});
  },{threshold:.08,rootMargin:'0px 0px -6% 0px'});
  els.forEach(function(e,i){e.style.transitionDelay=(i%3*60)+'ms';io.observe(e);});
})();
</script>
</body>
</html>
"""
    vals = dict(SITE, CSS=CSS, STATS=stats, ROWS="".join(rows),
                ABOUT=about, KIT=kit, CV=cv, EDU=edu,
                NAME=SITE["name"], ROLE=SITE["role"], LEDE=SITE["lede"],
                EMAIL=SITE["email"], LINKEDIN=SITE["linkedin"], GITHUB=SITE["github"])
    for k in ("NAME","ROLE","LEDE","EMAIL","LINKEDIN","GITHUB","CSS","STATS",
              "ROWS","ABOUT","KIT","CV","EDU"):
        tpl = tpl.replace("{{%s}}" % k, vals[k])
    return tpl

if __name__ == "__main__":
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(page())
    print("built index.html")
