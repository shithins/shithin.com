#!/usr/bin/env python3
"""
Build the shithin.com high-class nature-glass prototype pages.
Includes active verified links for theblackit, clockroach.work, Brain Crawl,
plus a high-class WANDER footer matrix.

Outputs *.html in the prototype root.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [
    ("Work", "work.html"),
    ("Studio", "studio.html"),
    ("Cinema", "cinema.html"),
    ("Contact", "contact.html"),
]

SOCIAL = [
    ("GitHub", "https://github.com/shithins/", "GitHub"),
    ("LinkedIn", "https://www.linkedin.com/in/shithin-ram-158327246/", "LinkedIn"),
    ("TheBlackit", "https://theblackit.com", "TheBlackit"),
    ("YouTube", "https://www.youtube.com/@EkalavyansStudio", "YouTube"),
    ("Email", "mailto:shithinrams2001@gmail.com", "Email"),
]

DESC = "Shithin Ram — Technical SEO Specialist, Software Builder & Co-Founder @ theblackit. Kozhikode, Kerala."


def head(title, desc, canonical, page_css=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Shithin Ram S">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://shithin.com/{canonical}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://shithin.com/{canonical}">
<meta property="og:site_name" content="Shithin Ram">
<meta property="og:image" content="https://shithin.com/img/og.webp">
<link rel="icon" type="image/svg+xml" href="img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
{page_css}<script>document.documentElement.className+=' js';</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'        <a href="{href}"{cur}>{label}</a>')
    links = "\n".join(links)
    return f"""<header class="bar" id="bar">
  <div class="wrap">
    <div class="bar__nav-shell">
      <a class="brand" href="./">
        <span class="brand-dot"></span>
        Shithin Ram
      </a>
      <nav class="nav" aria-label="Primary">
{links}
      </nav>
      <div class="bar__actions">
        <a class="btn btn--glass btn--sm" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit.com ↗</a>
        <a class="btn btn--lime btn--sm" href="https://os.shithin.com" target="_blank" rel="noopener noreferrer">ShithinOS ↗</a>
      </div>
    </div>
  </div>
</header>
"""


def footer():
    """WANDER landscape scene, then a single hairline link bar."""
    return f"""</main>

<footer class="wander-footer" id="wander-footer">
  <!-- Landscape scene, with the giant wordmark resting on the horizon -->
  <div class="wander-scene">
    <div class="wander-bg" aria-hidden="true"></div>
    <div class="wander-letters" aria-hidden="true">
      <span class="wander-text">SHITHIN.COM</span>
    </div>

    <div class="wander-labels">
      <div class="wander-label-item"><span>01</span> KOZHIKODE, KERALA</div>
      <div class="wander-label-item">TECHNICAL SEO</div>
      <div class="wander-label-item">THEBLACKIT PRODUCT LAB</div>
      <div class="wander-label-item">SERENE IS THE SUMMIT</div>
      <a class="wander-label-item wander-label-btn" href="work.html">EXPLORE WORK ↗</a>
    </div>
  </div>

  <!-- One quiet, evenly divided link bar instead of a four-column block -->
  <div class="wrap">
    <nav class="wander-links" aria-label="Footer">
      <a href="work.html">Work</a>
      <a href="studio.html">Studio</a>
      <a href="cinema.html">Cinema</a>
      <a href="services.html">Services</a>
      <a href="contact.html">Contact</a>
      <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer">TheBlackit ↗</a>
      <a href="https://os.shithin.com" target="_blank" rel="noopener noreferrer">ShithinOS '98 ↗</a>
    </nav>

    <div class="wander-footer__bottom">
      <div>© <span id="yr">2026</span> Shithin Ram</div>
      <div class="wander-footer__tag">Curiosity in code · Kozhikode, Kerala</div>
      <div class="wander-footer__meta">
        <span class="beyond-social">
          <a href="https://github.com/shithins/" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer">YouTube</a>
          <a href="mailto:shithinrams2001@gmail.com">Email</a>
        </span>
        <span id="clock">--:--:--</span> IST
      </div>
    </div>
  </div>
</footer>

<script src="js/site.js" defer></script>
</body>
</html>
"""


def page(filename, title, desc, canonical, active, body, page_css=""):
    html = head(title, desc, canonical, page_css) + header(active) + body + footer()
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"  {filename:16} {len(html)/1024:6.1f} KB")


# =============================================================================
#  PAGES
# =============================================================================

def home():
    body = f"""<main id="main">
  <!-- Hero Section: Macro Moss Nature Atmosphere (Verdant Style) -->
  <section class="hero">
    <div class="hero__bg" aria-hidden="true">
      <img src="img/nature-hero.jpg" alt="" width="2560" height="1440" fetchpriority="high">
    </div>
    <div class="hero__inner wrap">
      <div class="hero__badge">
        <span class="pulse-dot"></span>
        <span>CO-FOUNDER @ <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="color:var(--lime); text-decoration:underline;">THEBLACKIT</a> · SEO LEAD @ ACODEZ</span>
      </div>

      <h1 class="display">
        Curiosity in code,<br>
        <span class="glow-word">intelligence</span> in search.
      </h1>

      <p class="hero__sub">
        I'm Shithin Ram — technical SEO specialist, product builder, and co-founder of theblackit based in Kozhikode, Kerala. I bridge complex search engines, sovereign software tools, and creative cinema.
      </p>

      <div class="hero__cta-row">
        <a class="btn btn--lime btn--lg" href="work.html">Explore My Work →</a>
      </div>

      <!-- Floating Glass Cards (Verdant Style - Clean Alignment, Zero Collision) -->
      <div class="glass-grid">
        <div class="glass-card">
          <div class="glass-card__icon-box">❖</div>
          <div class="glass-card__eyebrow">Product Lab</div>
          <h3 class="glass-card__title">TheBlackit</h3>
          <p class="glass-card__desc">Co-Founder &amp; builder of sovereign community software and Chrome extensions without recurring SaaS drag.</p>
          <div class="glass-card__footer">
            <div class="glass-card__footer-meta">
              <span class="glass-card__pill">Venture Studio</span>
              <span class="glass-card__note">Flagship Product Lab</span>
            </div>
          </div>
        </div>

        <div class="glass-card">
          <div class="glass-card__icon-box">⚡</div>
          <div class="glass-card__eyebrow">Search Architecture</div>
          <h3 class="glass-card__title">SEO Team Lead</h3>
          <p class="glass-card__desc">Leading technical search at Acodez IT Solutions. Core Web Vitals, crawl budget engineering, and Generative Engine Optimization (GEO).</p>
          <div class="glass-card__footer">
            <div class="glass-card__footer-meta">
              <span class="glass-card__pill">Enterprise Scale</span>
              <span class="glass-card__note">4+ Years Lead</span>
            </div>
          </div>
        </div>

        <div class="glass-card">
          <div class="glass-card__icon-box">🎬</div>
          <div class="glass-card__eyebrow">Visual Narrative</div>
          <h3 class="glass-card__title">Ekalavyan Studios</h3>
          <p class="glass-card__desc">Directing, writing, and exploring world cinema. Grounding cold algorithms in human rhythm, emotion, and storytelling.</p>
          <div class="glass-card__footer">
            <div class="glass-card__footer-meta">
              <span class="glass-card__pill">Film &amp; Art</span>
              <span class="glass-card__note">Directing &amp; Essays</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- Featured Products Section: Pure Frosted Glass Cards with Live Links -->
  <section id="featured-work">
    <div class="wrap">
      <div class="sec-head">
        <div class="sec-head__body">
          <span class="label label--lime">❖ In-House Creations</span>
          <h2 class="h2">Tools built to eliminate friction.</h2>
          <p class="body" style="margin-top:12px;">Software incubated under TheBlackit to solve actual engineering and productivity bottlenecks.</p>
        </div>
        <a class="btn btn--glass" href="work.html">View All Products →</a>
      </div>

      <div class="prod-grid">
        <!-- 1. theblackit -->
        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Flagship Studio</span>
              <h3 class="prod-card__title">theblackit</h3>
            </div>
            <span class="glass-card__pill">Launching 2026</span>
          </div>
          <p class="prod-card__desc">An independent digital product studio from Kerala. Turning original ideas into community-driven software, built to scale cleanly without recurring SaaS drag.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Community App</span>
              <span class="tag">Software Studio</span>
              <span class="tag">Kerala</span>
            </div>
            <a class="prod-card__link" href="work.html">All Products →</a>
          </div>
        </article>

        <!-- 2. Clockroach -->
        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Productivity Tool</span>
              <h3 class="prod-card__title">Clockroach</h3>
            </div>
            <span class="glass-card__pill">Live</span>
          </div>
          <p class="prod-card__desc">A lightweight, friction-free developer time-tracking tool and Chrome extension that logs sprint tasks into cloud storage with zero overhead.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Vanilla JS</span>
              <span class="tag">Cloud Sync</span>
              <span class="tag">Web Store</span>
            </div>
            <a class="prod-card__link" href="https://clockroach.work/" target="_blank" rel="noopener noreferrer">clockroach.work ↗</a>
          </div>
        </article>

        <!-- 3. Brain Crawl -->
        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Chrome Extension</span>
              <h3 class="prod-card__title">Brain Crawl</h3>
            </div>
            <span class="glass-card__pill">Live On Web Store</span>
          </div>
          <p class="prod-card__desc">Daily interactive micro-quizzes on technical SEO, Core Web Vitals, and algorithm shifts served directly into developer and marketer new tabs.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Gamified UI</span>
              <span class="tag">SEO Engineering</span>
              <span class="tag">New Tab</span>
            </div>
            <a class="prod-card__link" href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer">Chrome Web Store ↗</a>
          </div>
        </article>

        <!-- 4. Keeptime -->
        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Enterprise Chrome Extension</span>
              <h3 class="prod-card__title">Keeptime</h3>
            </div>
            <span class="glass-card__pill">In Pilot</span>
          </div>
          <p class="prod-card__desc">Full-scale attendance &amp; HRM living inside a browser extension, syncing directly to Google Sheets on a private BYOD architecture.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Manifest V3</span>
              <span class="tag">Sheets API</span>
              <span class="tag">Zero SaaS Fee</span>
            </div>
            <a class="prod-card__link" href="work.html#keeptime">Details →</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- Cinema & Ethos Spotlight Section (Clean Editorial Glass) -->
  <section id="spotlight">
    <div class="wrap">
      <div class="spotlight-card">
        <span class="label label--lime">🎬 Creative Realm</span>
        <h2 class="h2" style="margin: 14px 0 20px;">Cinema as an antidote to cold code.</h2>
        <p class="body" style="max-width:70ch;">
          Under <strong>Ekalavyan Studios</strong>, I explore short films, scriptwriting, and cinema criticism. While algorithms seek computational efficiency, storytelling explores the quiet and complex beauty of human emotion.
        </p>
        <div style="margin-top:28px;">
          <a class="btn btn--glass" href="cinema.html">Explore Ekalavyan Studios →</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Core Capabilities Section -->
  <section id="capabilities">
    <div class="wrap">
      <div class="sec-head">
        <div class="sec-head__body">
          <span class="label label--lime">⚡ Core Competencies</span>
          <h2 class="h2">Where technical depth meets design.</h2>
          <p class="body" style="margin-top:12px;">The four pillars that define how I engineer software and scale digital discovery.</p>
        </div>
      </div>

      <div class="cap-grid">
        <div class="cap-item">
          <span class="cap-num">01</span>
          <h3 class="cap-title">Technical SEO &amp; Vitals</h3>
          <p class="cap-desc">Crawl budgets, server logs, JavaScript hydration, and sub-second Core Web Vitals optimization (LCP / INP / CLS).</p>
        </div>

        <div class="cap-item">
          <span class="cap-num">02</span>
          <h3 class="cap-title">Generative Engine Opt (GEO)</h3>
          <p class="cap-desc">Structuring knowledge graphs, entity disambiguation, and content embeddings so AI search engines cite you as ground truth.</p>
        </div>

        <div class="cap-item">
          <span class="cap-num">03</span>
          <h3 class="cap-title">Sovereign Software Builds</h3>
          <p class="cap-desc">Building fast, zero-bloat web apps and Manifest V3 extensions that respect user privacy and avoid recurring SaaS taxes.</p>
        </div>

        <div class="cap-item">
          <span class="cap-num">04</span>
          <h3 class="cap-title">Cinematic Storytelling</h3>
          <p class="cap-desc">Directing narrative shorts, video essays, and scripts under Ekalavyan Studios. Balancing computational logic with poetic art.</p>
        </div>
      </div>
    </div>
  </section>
"""
    page("index.html", "Shithin Ram — SEO Specialist, Product Builder & Co-Founder @ TheBlackit", DESC, "", "./", body)


def work_page():
    body = f"""<main id="main">
  <section class="phero">
    <div class="phero__inner wrap">
      <span class="label label--lime">❖ Innovation Lab</span>
      <h1 class="h1">Software and tools <em>built to endure</em>.</h1>
      <p class="lede phero__sub">Products, browser extensions, and experiments incubated under <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="color:var(--lime); text-decoration:underline;">TheBlackit</a> and shipped to live users.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="wrap">
      <div class="prod-grid">
        <!-- theblackit -->
        <article class="prod-card" id="theblackit">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Studio Venture</span>
              <h3 class="prod-card__title">theblackit</h3>
            </div>
            <span class="glass-card__pill">Launching 2026</span>
          </div>
          <p class="prod-card__desc">An independent product studio founded by Shithin Ram and close collaborators in Kerala. Building community-first software designed to eliminate unnecessary SaaS friction.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Community App</span>
              <span class="tag">Product Lab</span>
            </div>
            <a class="prod-card__link" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit.com ↗</a>
          </div>
        </article>

        <!-- Clockroach -->
        <article class="prod-card" id="clockroach">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Developer Tool</span>
              <h3 class="prod-card__title">Clockroach</h3>
            </div>
            <span class="glass-card__pill">Live</span>
          </div>
          <p class="prod-card__desc">A lightweight, friction-free time-logging tool and Chrome extension designed for engineering teams and freelancers. Client-side cloud sync logs sprint tasks with zero tracking lag.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Chrome API</span>
              <span class="tag">Cloud Sync</span>
              <span class="tag">Vanilla JS</span>
            </div>
            <a class="prod-card__link" href="https://clockroach.work/" target="_blank" rel="noopener noreferrer">clockroach.work ↗</a>
          </div>
        </article>

        <!-- Brain Crawl -->
        <article class="prod-card" id="brain-crawl">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Chrome Extension</span>
              <h3 class="prod-card__title">Brain Crawl</h3>
            </div>
            <span class="glass-card__pill">Live</span>
          </div>
          <p class="prod-card__desc">A gamified new-tab Chrome extension presenting daily interactive micro-quizzes on technical SEO, Core Web Vitals, and search algorithm updates.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Gamified UI</span>
              <span class="tag">Web Vitals</span>
              <span class="tag">SEO EdTech</span>
            </div>
            <a class="prod-card__link" href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer">Chrome Web Store ↗</a>
          </div>
        </article>

        <!-- Keeptime -->
        <article class="prod-card" id="keeptime">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Chrome Extension</span>
              <h3 class="prod-card__title">Keeptime</h3>
            </div>
            <span class="glass-card__pill">In Pilot</span>
          </div>
          <p class="prod-card__desc">A full-scale attendance and HRM extension built on a BYOD (Bring Your Own Data) model. Connects directly to a team's private Google Sheets backend for clocking, breaks, and leave approval workflows.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Manifest V3</span>
              <span class="tag">Sheets API</span>
              <span class="tag">Privacy First</span>
            </div>
            <span class="prod-card__link" style="color:var(--text-3);">Private Pilot</span>
          </div>
        </article>
      </div>
    </div>
  </section>
"""
    page("work.html", "Work & Software — Shithin Ram", "Sovereign software, Chrome extensions and tools built by Shithin Ram under theblackit.", "work.html", "work.html", body)


def studio_page():
    body = f"""<main id="main">
  <section class="phero">
    <div class="phero__inner wrap">
      <span class="label label--lime">⚡ Background &amp; Story</span>
      <h1 class="h1">Who I am, what I believe, and <em>how I build</em>.</h1>
      <p class="lede phero__sub">Product builder and technical SEO specialist based in Kozhikode, Kerala. Dedicated to quiet execution and sovereign craft.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="wrap">
      <div style="display:grid; grid-template-columns:1.2fr 0.8fr; gap:clamp(32px, 5vw, 64px); align-items:start;">
        <div style="background:var(--glass-bg); backdrop-filter:blur(24px); border:1px solid var(--glass-border); border-radius:24px; padding:clamp(28px, 4vw, 44px);">
          <span class="label label--lime">The Journey</span>
          <h2 class="h2" style="margin: 14px 0 24px;">From Computer Science to Enterprise Search Leadership.</h2>
          <div class="body" style="display:flex; flex-direction:column; gap:16px;">
            <p>
              I graduated with a BSc in Computer Science, grounded in programming fundamentals, operating systems, and web architecture. Early on, I realized that writing code alone isn't enough if people cannot find what you build.
            </p>
            <p>
              That led me deep into <strong>Technical SEO</strong> — not keyword stuffing or vanity metrics, but the hard engineering layer: crawl budgets, server logs, rendering performance, and structured entity graphs. Today, as <strong>SEO Team Lead at Acodez IT Solutions</strong>, I guide organic search strategy across global enterprises, outranking multi-billion-dollar SaaS players.
            </p>
            <p>
              Simultaneously, together with close friends and collaborators, I co-founded <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="color:var(--lime); text-decoration:underline;">theblackit</a> — an independent product lab from Kerala where we incubate sovereign software, Chrome extensions, and community apps.
            </p>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:20px;">
          <div style="background:var(--glass-bg); backdrop-filter:blur(24px); border:1px solid var(--glass-border); border-radius:20px; padding:28px;">
            <span class="label label--lime">Key Roles</span>
            <div style="margin-top:16px; display:flex; flex-direction:column; gap:14px;">
              <div>
                <strong style="color:var(--text); font-size:16px; display:block;">Co-Founder &amp; Builder</strong>
                <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="font-family:var(--mono); font-size:12px; color:var(--lime);">theblackit.com ↗ (2024–Present)</a>
              </div>
              <div style="border-top:1px solid var(--line); padding-top:12px;">
                <strong style="color:var(--text); font-size:16px; display:block;">SEO Team Lead</strong>
                <span style="font-family:var(--mono); font-size:12px; color:var(--lime);">Acodez IT Solutions · 2022–Present</span>
              </div>
              <div style="border-top:1px solid var(--line); padding-top:12px;">
                <strong style="color:var(--text); font-size:16px; display:block;">Creative Director</strong>
                <span style="font-family:var(--mono); font-size:12px; color:var(--lime);">Ekalavyan Studios · Independent</span>
              </div>
            </div>
          </div>

          <div style="background:var(--glass-bg); backdrop-filter:blur(24px); border:1px solid var(--glass-border); border-radius:20px; padding:28px;">
            <span class="label label--lime">Location &amp; Ethos</span>
            <p class="body" style="font-size:14px; margin-top:12px;">
              Based in Kozhikode, Kerala, India (UTC+5:30). Focused on building tools that solve immediate friction and creating cinema with narrative depth.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    page("studio.html", "Studio & Bio — Shithin Ram", "Background, experience, and leadership story of Shithin Ram.", "studio.html", "studio.html", body)


def cinema_page():
    body = f"""<main id="main">
  <section class="phero">
    <div class="phero__inner wrap">
      <span class="label label--lime">🎬 Cinema &amp; Narrative</span>
      <h1 class="h1">Ekalavyan Studios: <em>Stories in Motion</em>.</h1>
      <p class="lede phero__sub">Writing, directing, and film criticism. Where code dissolves into visual human empathy.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="wrap">
      <div class="prod-grid">
        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Creative Channel</span>
              <h3 class="prod-card__title">Ekalavyan Studios</h3>
            </div>
            <span class="glass-card__pill">Active</span>
          </div>
          <p class="prod-card__desc">The independent creative collective where I explore short films, scriptwriting, and cinema analysis. Bringing Kerala's rich storytelling tradition to digital screens.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Directing</span>
              <span class="tag">Writing</span>
            </div>
            <a class="prod-card__link" href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a>
          </div>
        </article>

        <article class="prod-card">
          <div class="prod-card__top">
            <div>
              <span class="label label--lime">Film Analysis</span>
              <h3 class="prod-card__title">Visual Criticism &amp; Rhythm</h3>
            </div>
            <span class="glass-card__pill">Essays</span>
          </div>
          <p class="prod-card__desc">Dissecting cinematic grammar, pacing, blocking, and thematic subtext across Malayalam, Indian, and international cinema.</p>
          <div class="prod-card__footer">
            <div class="prod-card__tags">
              <span class="tag">Cinematography</span>
              <span class="tag">Editing</span>
            </div>
            <span class="prod-card__link" style="color:var(--text-3);">Essays Archive</span>
          </div>
        </article>
      </div>
    </div>
  </section>
"""
    page("cinema.html", "Cinema — Shithin Ram (Ekalavyan Studios)", "Filmmaking, directing, and narrative essays by Shithin Ram.", "cinema.html", "cinema.html", body)


def contact_page():
    body = f"""<main id="main">
  <section class="phero">
    <div class="phero__inner wrap">
      <span class="label label--lime">✉️ Connection</span>
      <h1 class="h1">Let's build something <em>memorable</em>.</h1>
      <p class="lede phero__sub">Whether it's discussing <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="color:var(--lime); text-decoration:underline;">theblackit</a>, technical search architecture, or cinema collaborations, my inbox is always open.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="wrap">
      <div style="background:var(--glass-bg); backdrop-filter:blur(28px); border:1px solid var(--glass-border); border-radius:24px; padding:clamp(32px, 5vw, 60px); max-width:800px; margin:0 auto;">
        <span class="label label--lime">Direct Inquiries</span>
        <h2 class="h2" style="margin:14px 0 24px;">Always happy to connect with fellow thinkers &amp; builders.</h2>
        
        <div style="display:flex; flex-direction:column; gap:16px; margin-bottom:32px;">
          <a class="btn btn--glass" href="mailto:shithinrams2001@gmail.com" style="justify-content:flex-start; font-family:var(--mono);">
            ✉️ Email: shithinrams2001@gmail.com
          </a>
          <a class="btn btn--glass" href="https://theblackit.com" target="_blank" rel="noopener noreferrer" style="justify-content:flex-start; font-family:var(--mono);">
            ❖ Venture: https://theblackit.com ↗
          </a>
          <a class="btn btn--glass" href="https://clockroach.work/" target="_blank" rel="noopener noreferrer" style="justify-content:flex-start; font-family:var(--mono);">
            🪲 Product: https://clockroach.work/ ↗
          </a>
          <a class="btn btn--glass" href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer" style="justify-content:flex-start; font-family:var(--mono);">
            🧠 Extension: Brain Crawl on Chrome Web Store ↗
          </a>
          <a class="btn btn--glass" href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer" style="justify-content:flex-start; font-family:var(--mono);">
            🔗 LinkedIn: /in/shithin-ram ↗
          </a>
          <a class="btn btn--glass" href="https://github.com/shithins/" target="_blank" rel="noopener noreferrer" style="justify-content:flex-start; font-family:var(--mono);">
            💻 GitHub: @shithins ↗
          </a>
        </div>

        <div style="border-top:1px solid var(--line); padding-top:20px; font-family:var(--mono); font-size:12px; color:var(--text-3);">
          Location: Kozhikode, Kerala, India · IST (UTC+5:30)
        </div>
      </div>
    </div>
  </section>
"""
    page("contact.html", "Contact — Shithin Ram", "Get in touch with Shithin Ram directly for collaborations and ideas.", "contact.html", "contact.html", body)


def main():
    print("Building shithin.com high-class prototype...")
    home()
    work_page()
    studio_page()
    cinema_page()
    contact_page()
    print("✓ All prototype pages generated successfully.")


if __name__ == "__main__":
    main()
