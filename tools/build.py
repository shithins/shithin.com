#!/usr/bin/env python3
"""
Build shithin.com — "Field Notes", a cinematic editorial journal.

Every page is generated here so the top bar, the fixed rail, the chapter
furniture and the colophon stay identical across all six.

Design intent (see the header comment in css/site.css):
  · serif + monospace only, no interface sans-serif
  · hairline rules, numbered chapters, folios and coordinates — print furniture
  · asymmetry over centred stacks; index lists over feature cards
  · one warm accent (amber / golden hour) instead of tech green
  · cinema first: the film work is the top of the record, not a footnote

Outputs *.html in the prototype root.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The header carries only the three things a visitor needs to decide with.
# Studio and Services live in the footer, and are linked from the homepage
# sections that introduce them.
NAV = [
    ("Work", "work.html"),
    ("Cinema", "cinema.html"),
    ("Contact", "contact.html"),
]

DESC = "Shithin Ram — filmmaker, technical SEO lead and co-founder of theblackit. Kozhikode, Kerala."
COORD = "11.2588° N / 75.7804° E"
SITE = "https://shithin.com"
SOCIAL = [
    "https://www.linkedin.com/in/shithin-ram-158327246/",
    "https://www.instagram.com/_shithin_s_/",
    "https://www.youtube.com/@EkalavyansStudio",
    "https://github.com/shithins/",
]
PAGE_LABELS = {
    "work.html": "Work",
    "studio.html": "Studio",
    "services.html": "Services",
    "cinema.html": "Cinema",
    "contact.html": "Contact",
}


def structured_data(title, desc, canonical):
    """One JSON-LD graph per page: Person, Organization, WebSite, WebPage, breadcrumb.

    The Person and WebSite nodes are identical everywhere; only the WebPage and
    BreadcrumbList change per page, so search engines get a consistent entity
    description for "Shithin Ram" from any URL.
    """
    page_url = SITE + "/" + canonical
    graph = [
        {
            "@type": "Person",
            "@id": SITE + "/#person",
            "name": "Shithin Ram",
            "alternateName": "Shithin Ram S",
            "url": SITE + "/",
            "image": SITE + "/img/og.jpg",
            "jobTitle": "SEO Team Lead",
            "worksFor": {"@type": "Organization", "name": "Acodez IT Solutions"},
            "memberOf": {"@id": "https://theblackit.com/#organization"},
            "knowsAbout": [
                "Technical SEO", "Core Web Vitals", "Generative engine optimisation",
                "Search engine architecture", "Filmmaking", "Screenwriting", "Film criticism",
            ],
            "sameAs": SOCIAL,
        },
        {
            "@type": "Organization",
            "@id": "https://theblackit.com/#organization",
            "name": "theblackit",
            "url": "https://theblackit.com",
            "description": "Independent product studio in Kerala building sovereign software, browser extensions and community apps.",
            "founder": {"@id": SITE + "/#person"},
        },
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": "Shithin Ram — Field Notes",
            "inLanguage": "en",
            "publisher": {"@id": SITE + "/#person"},
        },
        {
            "@type": "WebPage",
            "@id": page_url + "#webpage",
            "url": page_url,
            "name": title,
            "description": desc,
            "inLanguage": "en",
            "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#person"},
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/img/og.jpg"},
        },
    ]
    if canonical:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2,
                 "name": PAGE_LABELS.get(canonical, title.split(" — ")[0]),
                 "item": page_url},
            ],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


def head(title, desc, canonical, page_css=""):
    ld = structured_data(title, desc, canonical)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Shithin Ram S">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}/{canonical}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{canonical}">
<meta property="og:site_name" content="Shithin Ram">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A dark forest clearing, lit by low light">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/img/og.jpg">
<meta name="twitter:image:alt" content="A dark forest clearing, lit by low light">
<meta name="theme-color" content="#08090a">
<link rel="icon" type="image/svg+xml" href="img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,200;0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
{page_css}<script>document.documentElement.className+=' js';</script>
<script type="application/ld+json">{ld}</script>
</head>
<body class="has-rail">
<div class="progress" id="progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
"""


def topbar(active):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'      <a href="{href}"{cur}>{label}</a>')
    links = "\n".join(links)
    return f"""<header class="topbar" id="bar">
    <a class="wordmark" href="./">
      <span class="wordmark__dot" aria-hidden="true"></span>
      Shithin <em>Ram</em>
    </a>
    <nav class="nav" aria-label="Primary">
{links}
    </nav>
</header>
"""


def rail(section_label):
    """The fixed spine of the journal: running head, chapter ticks, current chapter."""
    ticks = "\n".join(
        f'      <span class="rail__tick" data-rail-tick="{i}"></span>'
        for i in range(1, 6)
    )
    return f"""<aside class="rail" aria-hidden="true">
    <span class="rail__text">Field Notes — Shithin Ram — {COORD}</span>
    <span class="rail__ticks">
{ticks}
    </span>
    <span class="rail__now" id="rail-now">{section_label}</span>
</aside>
"""


def footer():
    """Colophon: a thin forest plate carrying the name, then the credits."""
    return f"""</main>

<footer class="colophon">
  <div class="colophon__plate">
    <div class="colophon__plate-img clim-img" aria-hidden="true"></div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="colophon__fin">Shithin <em>Ram</em></div>
    <div class="colophon__plate-meta">Kozhikode, Kerala<br>{COORD}</div>
  </div>

  <div class="wrap">
    <div class="colophon__body">
      <div>
        <span class="label">Colophon</span>
        <p class="colophon__name">Cinema first. Search by trade. Software by instinct.</p>
        <p class="colophon__line">A journal kept in Kozhikode, on the Malabar coast — notes on films,
          crawlers, and the tools in between.</p>
      </div>

      <div class="colophon__links">
        <div class="colophon__col">
          <h4>Index</h4>
          <a href="work.html">Work</a>
          <a href="studio.html">Studio</a>
          <a href="services.html">Services</a>
          <a href="cinema.html">Cinema</a>
          <a href="contact.html">Contact</a>
        </div>
        <div class="colophon__col">
          <h4>Elsewhere</h4>
          <a href="https://theblackit.com" target="_blank" rel="noopener noreferrer">TheBlackit ↗</a>
          <a href="https://os.shithin.com" target="_blank" rel="noopener noreferrer">ShithinOS '98 ↗</a>
          <a href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer">Ekalavyan ↗</a>
          <a href="https://github.com/shithins/" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
          <a href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
          <a href="https://www.instagram.com/_shithin_s_/" target="_blank" rel="noopener noreferrer">Instagram ↗</a>
        </div>
      </div>
    </div>

    <div class="colophon__foot">
      <span>© <span id="yr">2026</span> Shithin Ram</span>
      <span>Kozhikode · <span id="clock">--:--:--</span> IST</span>
      <div class="ambience" role="group" aria-label="Ambience">
        <span class="ambience__label">Ambience</span>
        <button type="button" data-ambience="auto" aria-pressed="true">Auto</button>
        <button type="button" data-ambience="day" aria-pressed="false">Day</button>
        <button type="button" data-ambience="night" aria-pressed="false">Night</button>
        <button type="button" data-ambience="rain" aria-pressed="false">Rain</button>
      </div>
    </div>
  </div>
</footer>

<script src="js/site.js" defer></script>
</body>
</html>
"""


def page(filename, title, desc, canonical, active, body, section_label):
    html = (
        head(title, desc, canonical)
        + topbar(active)
        + rail(section_label)
        + body
        + footer()
    )
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"  {filename:16} {len(html)/1024:6.1f} KB")


def chapter(num, kicker, title, note, inner, ident):
    return f"""  <section class="chapter" id="{ident}" data-chapter="{num}">
    <div class="wrap">
      <div class="chapter__head">
        <div>
          <div class="chapter__kicker">
            <span class="chapter__num">{num}</span>
            <span>{kicker}</span>
          </div>
          <h2 class="h2 chapter__title">{title}</h2>
        </div>
        <p class="chapter__note">{note}</p>
      </div>
{inner}
    </div>
  </section>
"""


# The three ways in. Used on the home coda and at the top of the contact page,
# so the destination matches the invitation.
PATHS = """      <div class="paths">
        <a class="path" data-reveal href="contact.html">
          <span class="path__no">01</span>
          <span class="path__body">
            <span class="path__title">Search &amp; the website</span>
            <span class="path__desc">Send the URL and the requirement — crawlability, rendering, vitals, entity clarity. I will reply with the three things I would fix first.</span>
          </span>
          <span class="path__arrow" aria-hidden="true">→</span>
        </a>

        <a class="path" data-reveal href="mailto:shithinrams2001@gmail.com">
          <span class="path__no">02</span>
          <span class="path__body">
            <span class="path__title">Share a story</span>
            <span class="path__desc">If there is a film in you — a short, a scene, a feeling you cannot shake — tell me. Let us make it cinema.</span>
          </span>
          <span class="path__cta">Email ↗</span>
        </a>

        <a class="path" data-reveal href="https://theblackit.com" target="_blank" rel="noopener noreferrer">
          <span class="path__no">03</span>
          <span class="path__body">
            <span class="path__title">Have a product idea?</span>
            <span class="path__desc">Let us build it. Sovereign software, browser extensions and community tools — under theblackit.</span>
          </span>
          <span class="path__cta">theblackit.com ↗</span>
        </a>
      </div>
"""


# =============================================================================
#  HOME
# =============================================================================

def home():
    ledger_field = """      <div class="ledger">
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">i.</span>
          <span class="ledger__term">Technical SEO &amp; Core Web Vitals</span>
          <span class="ledger__desc">Crawl budgets, render paths, server logs and sub-second LCP / INP / CLS work on sites that cannot afford to be slow.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">ii.</span>
          <span class="ledger__term">Generative engine optimisation</span>
          <span class="ledger__desc">Knowledge graphs, entity disambiguation and citable structure, so answer engines quote you as ground truth rather than paraphrase a competitor.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">iii.</span>
          <span class="ledger__term">Search engineering</span>
          <span class="ledger__desc">The layer between the ranking plan and the repository: templates, JavaScript hydration, internal linking, and migrations that keep their equity.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">iv.</span>
          <span class="ledger__term">Measurement</span>
          <span class="ledger__desc">Field data tied to pipeline, not vanity dashboards. If a fix cannot be proven to have shipped and moved a number, it is not finished.</span>
        </div>
      </div>
"""

    index_lab = """      <div class="index">
        <a class="index__row" data-reveal href="work.html#theblackit">
          <span class="index__num">01</span>
          <span class="index__name">theblackit</span>
          <span class="index__desc">An independent product studio from Kerala. Community software and browser tools built to scale without recurring SaaS drag.</span>
          <span class="index__meta">Studio · 2026</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>
        <a class="index__row" data-reveal href="https://clockroach.work/" target="_blank" rel="noopener noreferrer">
          <span class="index__num">02</span>
          <span class="index__name">Clockroach</span>
          <span class="index__desc">A friction-free time-logging tool and Chrome extension. Client-side cloud sync with zero tracking overhead.</span>
          <span class="index__meta">Live · Tool</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>
        <a class="index__row" data-reveal href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer">
          <span class="index__num">03</span>
          <span class="index__name">Brain Crawl</span>
          <span class="index__desc">Daily micro-quizzes on technical SEO and search algorithms, served into the new tab of people who should know better.</span>
          <span class="index__meta">Live · Extension</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>
        <a class="index__row" data-reveal href="work.html#keeptime">
          <span class="index__num">04</span>
          <span class="index__name">Keeptime</span>
          <span class="index__desc">Attendance and HRM living inside a browser extension, on a bring-your-own-Google-Sheets architecture.</span>
          <span class="index__meta">Pilot · Extension</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>
      </div>
"""

    roles = """      <div class="ledger">
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">Always</span>
          <span class="ledger__term">Creative director</span>
          <span class="ledger__desc">Ekalavyan Studios. Short films, scripts, stage and screen — the work that came first and will outlast the rest.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">2025—</span>
          <span class="ledger__term">Co-founder &amp; builder</span>
          <span class="ledger__desc"><a class="ital" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit</a> — an independent product lab in Kerala, incubating sovereign software, extensions and community apps.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">2022—</span>
          <span class="ledger__term">SEO Team Lead</span>
          <span class="ledger__desc">Acodez IT Solutions. Organic search strategy across global enterprise accounts, outranking far larger SaaS competitors.</span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">Always</span>
          <span class="ledger__term">Human</span>
          <span class="ledger__desc">Walks the same forests, watches the same films, keeps the notes. The part of the work that does not fit in a ledger at all.</span>
        </div>
      </div>
"""

    screening = """      <div class="screening screening--feature">
        <figure class="frame frame--drift" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-01.webp" alt="A film crew at work among trees, lit by lamps" width="1600" height="900">
            <div class="fauna-field" data-fauna aria-hidden="true"></div>
          </div>
          <figcaption><span class="frame__no">01</span><span>The set</span><span class="frame__tc">00:04:12</span></figcaption>
        </figure>
        <figure class="frame" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-02.webp" alt="A camera on a tripod, crew silhouetted behind the lights" width="1600" height="900">
          </div>
          <figcaption><span class="frame__no">02</span><span>The camera</span><span class="frame__tc">00:11:38</span></figcaption>
        </figure>
        <figure class="frame" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-05.webp" alt="The night crew at the edge of the light" width="1600" height="900">
          </div>
          <figcaption><span class="frame__no">03</span><span>The night crew</span><span class="frame__tc">00:18:05</span></figcaption>
        </figure>
      </div>
"""

    body = f"""<main id="main">
  <section class="overture" id="overture" data-chapter="00">
    <div class="overture__media" data-parallax>
      <img class="clim-img" src="img/forest-hero.webp" alt="" width="2400" height="1350" fetchpriority="high">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="overture__inner wrap">
      <div class="overture__meta" data-reveal>
        <span>Field Notes — Vol. 01</span>
        <span class="divider" aria-hidden="true"></span>
        <span>Kozhikode, Kerala</span>
        <span class="coord">{COORD}</span>
      </div>
      <h1 class="display overture__title" data-line>
        Search, software,<br>and the <em>stories</em> I frame.
      </h1>
      <p class="overture__lede" data-reveal>I look for what hides between a query and a frame — and build the thing that finds it.</p>
      <div class="overture__foot" data-reveal>
        <span>Shithin Ram — cinema, software, technical SEO</span>
        <span class="overture__scroll">Scroll to read</span>
        <span class="overture__aside">A journal of film, search engines and software from the Malabar coast.</span>
      </div>
    </div>
  </section>

{chapter(
    "01", "The Frame",
    "Cinema is the antidote to <em>cold work</em>.",
    "Writing, directing, acting and criticism. The forest keeps getting cast.",
    screening + '''
      <div class="spread" style="margin-top: clamp(44px, 6vw, 76px);">
        <div class="spread__main body" data-reveal>
          <p>I am a writer, a director and an actor — with a stage presence earned in front of live audiences, where a room either listens or it does not. The craft is grammar, pacing, blocking and subtext: which beat to cut, which silence to keep, where the light should fall. To make a film is to speak from a thousand stages: to give voice to our protests, to speak our dreams aloud, and to show the world we wish the way it deserves to be seen. My life itself is a cinema.</p>
          <p style="margin-top:22px;"><a class="ital" href="cinema.html" style="font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;">Enter the studio ↗</a></p>
        </div>
        <div class="spread__aside">
          <p class="lede" data-reveal>Two disciplines, one habit: look at the thing itself, not the dashboard that describes it.</p>
        </div>
      </div>
''',
    "frame")}

{chapter(
    "02", "The Lab",
    "Software without the <em>subscription</em> tax.",
    "Products, extensions and experiments incubated under theblackit and shipped to real users.",
    index_lab,
    "lab")}

{chapter(
    "03", "The Field",
    "Search is an <em>engineering</em> discipline.",
    "Not keywords and vanity charts. Crawl budgets, render paths, and the machines that decide what exists at all.",
    f'''      <div class="spread">
        <div class="spread__main" data-reveal>
          <h3 class="h2">Most sites don't have a content problem. They have a <em>plumbing</em> problem.</h3>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>I lead technical search at <strong>Acodez IT Solutions</strong>, where the work is rarely about writing more pages. It is about whether the pages already written can be crawled, rendered, understood and trusted — and whether the team shipping them can see the difference in a number they care about.</p>
          <p>That means reading server logs the way a doctor reads a chart, treating JavaScript hydration as a search-surface decision, and refusing to recommend anything that cannot be verified in production a month later.</p>
        </div>
      </div>

      <div style="margin-top: clamp(44px, 6vw, 76px);">{ledger_field}</div>

      <p style="margin-top: clamp(26px, 4vw, 42px);" data-reveal>
        <a class="ital" href="services.html" style="font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;">Practice &amp; engagements ↗</a>
      </p>
''',
    "field")}

  <section class="chapter" id="person" data-chapter="04">
    <div class="wrap">
      <div class="chapter__head">
        <div>
          <div class="chapter__kicker">
            <span class="chapter__num">04</span>
            <span>The Person</span>
          </div>
          <h2 class="h2 chapter__title">A short <em>record</em>.</h2>
        </div>
        <p class="chapter__note">Where the hours have gone, and what they were for.</p>
      </div>

      <div class="figure-spread">
        <figure class="frame frame--tall" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/forest-tall.webp" alt="Sunlight through a moss-covered tree" width="1100" height="1500">
            <div class="fauna-field" data-fauna aria-hidden="true"></div>
          </div>
          <figcaption><span class="frame__no">04</span><span>Home ground, Kerala</span></figcaption>
        </figure>
        <div class="figure-spread__text">
          {roles}
        </div>
      </div>

      <p style="margin-top: clamp(30px, 4vw, 48px);" data-reveal>
        <a class="ital" href="studio.html" style="font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;">The longer story ↗</a>
      </p>
    </div>
  </section>

  <section class="coda" id="contact" data-chapter="05">
    <div class="wrap">
      <div class="rule" data-reveal style="margin-bottom: clamp(30px, 4vw, 48px);">
        <span><span class="rule__num">05</span> — Coda</span>
        <span>Three ways in</span>
      </div>
      <h2 class="h2" data-reveal style="max-width: 15ch;">Tell me what you are <em>making</em>.</h2>
      <p class="lede" data-reveal style="margin-top: clamp(20px, 3vw, 30px);">Whether it is a site that cannot be found, a story that wants to be a film, or a product that should not exist yet — there is a door for it.</p>

{PATHS}

      <div class="coda__links" data-reveal>
        <a href="mailto:shithinrams2001@gmail.com"><span>→</span> shithinrams2001@gmail.com</a>
        <a href="tel:+917025638802"><span>→</span> +91 70256 38802</a>
        <a href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer"><span>→</span> LinkedIn</a>
        <a href="https://www.instagram.com/_shithin_s_/" target="_blank" rel="noopener noreferrer"><span>→</span> Instagram</a>
      </div>
    </div>
  </section>
"""
    page(
        "index.html",
        "Shithin Ram — Filmmaker, Technical SEO & Co-Founder @ theblackit",
        DESC, "", "./", body, "00 / Overture",
    )


# =============================================================================
#  WORK
# =============================================================================

def work_page():
    body = f"""<main id="main">
  <section class="masthead" data-chapter="01">
    <div class="masthead__bg" aria-hidden="true">
      <img class="clim-img" src="img/forest-wide-01.webp" alt="" width="2200" height="1100">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="masthead__inner wrap">
      <div class="masthead__index">
        <span class="masthead__no">II</span>
        <span>Work — software &amp; tools</span>
        <span>{COORD}</span>
      </div>
      <h1 class="h1">Sovereign software, <em>built to endure</em>.</h1>
      <p class="lede masthead__sub">Products, browser extensions and experiments incubated under
        <a class="ital" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit</a>
        and shipped to live users. No venture deck, no growth loop — just tools that remove friction.</p>
    </div>
  </section>

  <section class="chapter" style="padding-top: clamp(48px, 7vw, 90px);">
    <div class="wrap">
      <div class="rule" style="margin-bottom: clamp(26px, 3.5vw, 40px);">
        <span><span class="rule__num">01–04</span> — The Index</span>
        <span>Four products, in the order they were built</span>
      </div>

      <div class="index">
        <a class="index__row" id="theblackit" data-reveal href="https://theblackit.com" target="_blank" rel="noopener noreferrer">
          <span class="index__num">01</span>
          <span class="index__name">theblackit</span>
          <span class="index__desc">An independent product studio founded in Kerala. Community-first software designed to eliminate unnecessary SaaS friction.</span>
          <span class="index__meta">Launching 2026</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>

        <a class="index__row" id="clockroach" data-reveal href="https://clockroach.work/" target="_blank" rel="noopener noreferrer">
          <span class="index__num">02</span>
          <span class="index__name">Clockroach</span>
          <span class="index__desc">A lightweight time-logging tool and Chrome extension for engineering teams and freelancers. Client-side cloud sync, zero tracking lag.</span>
          <span class="index__meta">Live · clockroach.work</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>

        <a class="index__row" id="brain-crawl" data-reveal href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer">
          <span class="index__num">03</span>
          <span class="index__name">Brain Crawl</span>
          <span class="index__desc">A gamified new-tab extension serving daily micro-quizzes on technical SEO, Core Web Vitals and search algorithm updates.</span>
          <span class="index__meta">Live · Chrome Web Store</span>
          <span class="index__arrow" aria-hidden="true">↗</span>
        </a>

        <div class="index__row" id="keeptime" data-reveal>
          <span class="index__num">04</span>
          <span class="index__name">Keeptime</span>
          <span class="index__desc">Attendance and HRM living inside a browser extension, on a bring-your-own-data Google Sheets architecture. Clocking, breaks and leave approval without a per-seat fee.</span>
          <span class="index__meta">Pilot · Private</span>
          <span class="index__arrow" aria-hidden="true">—</span>
        </div>
      </div>
    </div>
  </section>

  <section class="chapter">
    <div class="wrap">
      <div class="spread">
        <div class="spread__main" data-reveal>
          <h2 class="h2">Made for people who are <em>tired</em> of renting software.</h2>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>The common thread in all of it: the tool should cost what it costs, own what it stores, and disappear when the job is done. Vanilla JavaScript where a framework would only add weight. Manifest V3 extensions that respect the browser they live in.</p>
          <p>Some are products, some are fixes to my own problems. All of them ship.</p>
        </div>
      </div>
    </div>
  </section>
"""
    page(
        "work.html",
        "Work & Software — Shithin Ram",
        "Sovereign software, Chrome extensions and tools built by Shithin Ram under theblackit.",
        "work.html", "work.html", body, "II / Work",
    )


# =============================================================================
#  STUDIO
# =============================================================================

def studio_page():
    body = f"""<main id="main">
  <section class="masthead" data-chapter="01">
    <div class="masthead__bg" aria-hidden="true">
      <img class="clim-img" src="img/forest-wide-02.webp" alt="" width="2200" height="1100">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="masthead__inner wrap">
      <div class="masthead__index">
        <span class="masthead__no">I</span>
        <span>Studio — biography</span>
        <span>{COORD}</span>
      </div>
      <h1 class="h1">Who I am, what I believe, and <em>how I build</em>.</h1>
      <p class="lede masthead__sub">Filmmaker first, technical SEO lead by trade, product builder by instinct. Kozhikode, Kerala.</p>
    </div>
  </section>

  <section class="chapter" style="padding-top: clamp(48px, 7vw, 90px);">
    <div class="wrap">
      <div class="rule" style="margin-bottom: clamp(30px, 4vw, 52px);">
        <span><span class="rule__num">01</span> — The Journey</span>
        <span>Craft, trade, and the thing that came first</span>
      </div>

      <div class="spread">
        <div class="spread__main" data-reveal>
          <h2 class="h2">The film came first. The rest pays for <em>it</em>.</h2>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>I graduated with a BSc in Computer Science — programming fundamentals, operating systems, web architecture. Early on it became obvious that shipping was not the same as being visible.</p>
          <p>That led me into <strong>technical SEO</strong>: not keyword stuffing or vanity metrics, but the hard engineering layer. Crawl budgets, server logs, rendering performance, structured entity graphs. Today, as <strong>SEO Team Lead at Acodez IT Solutions</strong>, I guide organic search strategy across global enterprises, outranking far larger competitors.</p>
          <p>Alongside that, with close friends and collaborators, I co-founded
            <a class="ital" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit</a>
            — an independent product lab from Kerala incubating sovereign software, Chrome extensions and community apps.</p>
          <p>But the thing that came first, and the thing that will outlast the rest, is <strong>cinema</strong>. I write, direct and act — the stage, the set, the frame. Search and software are disciplines; this is the reason.</p>
        </div>
      </div>

      <div style="margin-top: clamp(56px, 8vw, 104px);">
        <div class="rule" style="margin-bottom: 0;">
          <span><span class="rule__num">02</span> — The Record</span>
          <span>Roles &amp; years</span>
        </div>
        <div class="ledger">
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">Always</span>
            <span class="ledger__term">Creative director</span>
            <span class="ledger__desc">Ekalavyan Studios. Directing, writing, acting and film criticism — the first thing, not the side thing.</span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">2025—</span>
            <span class="ledger__term">Co-founder &amp; builder</span>
            <span class="ledger__desc"><a class="ital" href="https://theblackit.com" target="_blank" rel="noopener noreferrer">theblackit</a> — independent product lab. Sovereign software, extensions, community apps.</span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">2022—</span>
            <span class="ledger__term">SEO Team Lead</span>
            <span class="ledger__desc">Acodez IT Solutions. Strategy, technical direction and reporting across global enterprise accounts.</span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">Always</span>
            <span class="ledger__term">Human</span>
            <span class="ledger__desc">The part that watches the light change, keeps the notes, and still prefers the long way home through the trees.</span>
          </div>
        </div>
      </div>

      <div style="margin-top: clamp(56px, 8vw, 104px);">
        <div class="rule" style="margin-bottom: 0;">
          <span><span class="rule__num">03</span> — Ethos</span>
          <span>How I work</span>
        </div>
        <div class="ledger">
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">i.</span>
            <span class="ledger__term">Verify, don't assume</span>
            <span class="ledger__desc">Every claim should be checkable in production. Logs, field data, a crawl you can rerun. Opinions are cheap; evidence is not.</span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">ii.</span>
            <span class="ledger__term">Subtract</span>
            <span class="ledger__desc">Most sites have three real problems, not eighty. The job is choosing which three, and having the discipline to ignore the rest for now.</span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">iii.</span>
            <span class="ledger__term">Own the output</span>
            <span class="ledger__desc">If the fix matters, write the ticket, review the implementation, and confirm it shipped. Handing over a PDF is not the end of the work.</span>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    page(
        "studio.html",
        "Studio & Bio — Shithin Ram",
        "Background, experience, and leadership story of Shithin Ram.",
        "studio.html", "studio.html", body, "I / Studio",
    )


# =============================================================================
#  SERVICES
# =============================================================================

def services_page():
    body = f"""<main id="main">
  <section class="masthead" data-chapter="01">
    <div class="masthead__bg" aria-hidden="true">
      <img class="clim-img" src="img/forest-wide-01.webp" alt="" width="2200" height="1100">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="masthead__inner wrap">
      <div class="masthead__index">
        <span class="masthead__no">III</span>
        <span>Services — engagement</span>
        <span>{COORD}</span>
      </div>
      <h1 class="h1">Search work that pays for itself, <em>measurably</em>.</h1>
      <p class="lede masthead__sub">A small number of engagements at a time: audits, Core Web Vitals and migration
        projects, fractional search leadership, and SEO-first builds where the engineering and the ranking
        plan are the same conversation.</p>
    </div>
  </section>

  <section class="chapter" style="padding-top: clamp(48px, 7vw, 90px);">
    <div class="wrap">
      <div class="rule" style="margin-bottom: clamp(30px, 4vw, 52px);">
        <span><span class="rule__num">01</span> — Engagement</span>
        <span>Three ways to work together</span>
      </div>

      <div class="spread">
        <div class="spread__main" data-reveal>
          <h2 class="h2">Fixed scope where the problem is clear. A <em>retainer</em> where it is not.</h2>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>No long lock-ins and no junior handover. I take on a handful of engagements at a time so the
            person who diagnoses the problem is the person who sees it through.</p>
        </div>
      </div>

      <div class="ledger" style="margin-top: clamp(40px, 6vw, 70px);">
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">01</span>
          <span class="ledger__term">Technical audit &amp; roadmap</span>
          <span class="ledger__desc">One deep pass over the site, the crawlers and the data. Findings ranked by
            business impact, not a ninety-page PDF. Full crawl, log and render analysis; Core Web Vitals field
            and lab diagnosis; indexation, schema and entity review; a prioritised ninety-day roadmap; and a
            walkthrough call with your dev team. <em>2–3 weeks · fixed fee</em></span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">02</span>
          <span class="ledger__term">Fractional SEO leadership</span>
          <span class="ledger__desc">I own search outcomes with your team: strategy, technical direction,
            reporting, and the uncomfortable prioritisation calls. Monthly strategy and execution plan,
            dev-ready tickets, a GEO and AI-citation programme, content briefs and internal linking, and
            reporting tied to pipeline. <em>Monthly retainer · two slots</em></span>
        </div>
        <div class="ledger__row" data-reveal>
          <span class="ledger__num">03</span>
          <span class="ledger__term">SEO-first build or migration</span>
          <span class="ledger__desc">When the site itself is the problem. I engineer the replacement so speed,
            structure and crawlability are built in from line one: migrating without losing equity, a
            zero-bloat front end with semantic markup, schema and template architecture, and extensions or
            automation around it. <em>Scoped per project</em></span>
        </div>
      </div>

      <div style="margin-top: clamp(64px, 9vw, 120px);">
        <div class="rule" style="margin-bottom: clamp(30px, 4vw, 52px);">
          <span><span class="rule__num">02</span> — Process</span>
          <span>Five steps, every time</span>
        </div>
        <div class="ledger">
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">i.</span>
            <span class="ledger__term">Measure</span>
            <span class="ledger__desc">Crawl, logs, field data, Search Console, analytics and the money pages.
              We agree the baseline before anyone touches the site. <em>You get a baseline report and a
              definition of winning, in numbers.</em></span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">ii.</span>
            <span class="ledger__term">Diagnose</span>
            <span class="ledger__desc">Separate what moves revenue from what merely looks broken. Most sites
              have three real problems, not eighty. <em>You get root-cause findings with evidence, ranked by
              impact and effort.</em></span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">iii.</span>
            <span class="ledger__term">Build</span>
            <span class="ledger__desc">Dev-ready tickets, code where it is mine to write, and verification
              that each fix actually shipped to production. <em>You get tickets, implementations, QA and
              crawl verification.</em></span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">iv.</span>
            <span class="ledger__term">Compound</span>
            <span class="ledger__desc">Once the foundation holds: entity work, GEO, content structure and
              internal linking to raise the ceiling. <em>You get a content and GEO programme aligned to query
              intent.</em></span>
          </div>
          <div class="ledger__row" data-reveal>
            <span class="ledger__num">v.</span>
            <span class="ledger__term">Report</span>
            <span class="ledger__desc">Plain-language reporting on the numbers that matter: qualified organic
              sessions, rankings that convert, AI citations. <em>You get a monthly readout with next month's
              bets.</em></span>
          </div>
        </div>
      </div>

      <div style="margin-top: clamp(64px, 9vw, 120px);">
        <div class="rule" style="margin-bottom: clamp(30px, 4vw, 52px);">
          <span><span class="rule__num">03</span> — FAQ</span>
          <span>Questions I get asked</span>
        </div>
        <div class="spread">
          <div class="spread__main" data-reveal>
            <h2 class="h2">The things worth asking <em>before</em> you hire anyone.</h2>
          </div>
          <div class="spread__aside body" data-reveal>
            <details>
              <summary>Can you work with our existing development team?</summary>
              <p>That is the usual setup. I produce tickets your engineers can act on, review implementations
                and verify what shipped. If they are comfortable with me contributing code directly, that is
                usually faster.</p>
            </details>
            <details>
              <summary>Do you do content writing as well?</summary>
              <p>I do content strategy, briefs and structural editing, plus technical writing where the topic
                is search. For long-form editorial at volume I will brief and review rather than write
                everything myself.</p>
            </details>
            <details>
              <summary>How long before we see something?</summary>
              <p>Technical wins often show within weeks: indexation recoveries, crawl budget, page speed.
                Competitive ranking and entity gains compound over three to six months. I will tell you which
                kind of result to expect at each stage.</p>
            </details>
            <details>
              <summary>What about AI search and GEO?</summary>
              <p>It runs alongside classic SEO, not instead of it. Entities, schema, structure and citable
                content are the same foundation that makes answer engines comfortable quoting you.</p>
            </details>
            <details>
              <summary>Do you sign NDAs and work with agencies?</summary>
              <p>Yes to both. A good share of my work is specialist support behind agency teams, including
                white-label technical audits.</p>
            </details>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="coda">
    <div class="wrap">
      <div class="rule" data-reveal style="margin-bottom: clamp(30px, 4vw, 48px);">
        <span><span class="rule__num">→</span> Start</span>
        <span>Send the website and the requirement</span>
      </div>
      <h2 class="h2" data-reveal style="max-width: 16ch;">Send the URL and the requirement. Decide <em>after</em> that.</h2>
      <p class="lede" data-reveal style="margin-top: clamp(22px, 3vw, 34px);">Twenty minutes on crawlability,
        rendering, vitals and entity clarity — then the three things I would fix first. No deck, no obligation.</p>
      <p style="margin-top: clamp(26px, 4vw, 40px);" data-reveal>
        <a class="path__cta" href="contact.html">Go to contact ↗</a>
      </p>
      <div class="coda__links" data-reveal>
        <a href="mailto:shithinrams2001@gmail.com"><span>→</span> Email</a>
        <a href="tel:+917025638802"><span>→</span> +91 70256 38802</a>
        <a href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer"><span>→</span> LinkedIn</a>
      </div>
    </div>
  </section>
"""
    page(
        "services.html",
        "Services & Engagement — Shithin Ram",
        "SEO consulting, technical audits, Core Web Vitals programmes, GEO and SEO-first web builds. Engagement models, process and FAQ.",
        "services.html", "services.html", body, "III / Services",
    )


# =============================================================================
#  CINEMA
# =============================================================================

def cinema_page():
    body = f"""<main id="main">
  <section class="masthead" data-chapter="01">
    <div class="masthead__bg" aria-hidden="true">
      <img class="clim-img" src="img/forest-wide-01.webp" alt="" width="2200" height="1100">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="masthead__inner wrap">
      <div class="masthead__index">
        <span class="masthead__no">IV</span>
        <span>Cinema — Ekalavyan Studios</span>
        <span>{COORD}</span>
      </div>
      <h1 class="h1">Ekalavyan Studios: <em>stories in motion</em>.</h1>
      <p class="lede masthead__sub">Writing, directing, acting and film criticism. The forest is the set, the set is
        the forest — this is where the work begins.</p>
    </div>
  </section>

  <section class="chapter" style="padding-top: clamp(48px, 7vw, 90px);">
    <div class="wrap">
      <div class="rule" style="margin-bottom: clamp(26px, 3.5vw, 42px);">
        <span><span class="rule__num">01</span> — The Reel</span>
        <span>Forest, late light · 00:04:12</span>
      </div>

      <div class="screening screening--feature">
        <figure class="frame frame--drift" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-01.webp" alt="A film crew at work among trees, lit by lamps" width="1600" height="900">
            <div class="fauna-field" data-fauna aria-hidden="true"></div>
          </div>
          <figcaption><span class="frame__no">01</span><span>The set</span><span class="frame__tc">00:04:12</span></figcaption>
        </figure>
        <figure class="frame" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-03.webp" alt="Crew and camera in lantern light" width="800" height="450">
          </div>
          <figcaption><span class="frame__no">02</span><span>The crew</span><span class="frame__tc">00:11:38</span></figcaption>
        </figure>
        <figure class="frame" data-reveal>
          <div class="frame__media">
            <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-04.webp" alt="A softbox lamp and the camera beside it" width="1600" height="900">
          </div>
          <figcaption><span class="frame__no">03</span><span>The lamp</span><span class="frame__tc">00:18:05</span></figcaption>
        </figure>
      </div>

      <figure class="frame frame--drift" data-reveal style="margin-top: clamp(16px, 2.4vw, 28px);">
        <div class="frame__media" style="aspect-ratio: 21 / 9;">
          <img class="clim-img" loading="lazy" decoding="async" src="img/frame-set-wide.webp" alt="The whole set, in the trees at night" width="1600" height="686">
          <div class="fauna-field" data-fauna aria-hidden="true"></div>
        </div>
        <figcaption><span class="frame__no">04</span><span>The whole set</span><span class="frame__tc">00:23:47</span></figcaption>
      </figure>

      <div class="spread" style="margin-top: clamp(44px, 6vw, 78px);">
        <div class="spread__main" data-reveal>
          <h2 class="h2">The frame is a decision about what to <em>withhold</em>.</h2>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>Film is a discipline of rhythm and restraint — knowing exactly how long to hold a shot before
            letting it go, and what the silence afterwards is for.</p>
          <p>I write, direct and act under Ekalavyan Studios: short films, scripts and cinema criticism —
            Kerala's storytelling tradition, carried to a screen that is usually in a hurry.</p>
        </div>
      </div>

      <div style="margin-top: clamp(56px, 8vw, 104px);">
        <div class="rule" style="margin-bottom: 0;">
          <span><span class="rule__num">02</span> — The Programme</span>
          <span>Two ongoing bodies of work</span>
        </div>
        <div class="index">
          <a class="index__row" data-reveal href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer">
            <span class="index__num">01</span>
            <span class="index__name">Ekalavyan Studios</span>
            <span class="index__desc">The independent creative collective: short films, scriptwriting, acting and cinema analysis. Active.</span>
            <span class="index__meta">YouTube · Active</span>
            <span class="index__arrow" aria-hidden="true">↗</span>
          </a>
          <div class="index__row" data-reveal>
            <span class="index__num">02</span>
            <span class="index__name">Visual criticism</span>
            <span class="index__desc">Dissecting cinematic grammar, pacing, blocking and thematic subtext across Malayalam, Indian and international cinema.</span>
            <span class="index__meta">Essays</span>
            <span class="index__arrow" aria-hidden="true">—</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="coda">
    <div class="wrap">
      <div class="rule" data-reveal style="margin-bottom: clamp(30px, 4vw, 48px);">
        <span><span class="rule__num">→</span> Watch</span>
        <span>New work, occasionally</span>
      </div>
      <h2 class="h2" data-reveal style="max-width: 18ch;">Short films, scripts and essays appear <em>quietly</em>.</h2>
      <p class="lede" data-reveal style="margin-top: clamp(22px, 3vw, 34px);">The channel is where the finished
        work lands. If there is a story you want made, that is the door.</p>
      <p style="margin-top: clamp(26px, 4vw, 40px);" data-reveal>
        <a class="path__cta" href="contact.html">Share a story ↗</a>
      </p>
      <div class="coda__links" data-reveal>
        <a href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer"><span>→</span> YouTube</a>
        <a href="https://www.instagram.com/_shithin_s_/" target="_blank" rel="noopener noreferrer"><span>→</span> Instagram</a>
        <a href="contact.html"><span>→</span> Collaborations</a>
        <a href="mailto:shithinrams2001@gmail.com"><span>→</span> Email</a>
      </div>
    </div>
  </section>
"""
    page(
        "cinema.html",
        "Cinema — Shithin Ram (Ekalavyan Studios)",
        "Filmmaking, directing, and narrative essays by Shithin Ram.",
        "cinema.html", "cinema.html", body, "IV / Cinema",
    )


# =============================================================================
#  CONTACT
# =============================================================================

def contact_page():
    body = f"""<main id="main">
  <section class="masthead" data-chapter="01">
    <div class="masthead__bg" aria-hidden="true">
      <img class="clim-img" src="img/forest-wide-02.webp" alt="" width="2200" height="1100">
    </div>
    <div class="fauna-field" data-fauna aria-hidden="true"></div>
    <div class="masthead__inner wrap">
      <div class="masthead__index">
        <span class="masthead__no">V</span>
        <span>Contact — correspondence</span>
        <span>{COORD}</span>
      </div>
      <h1 class="h1">Tell me what you are <em>making</em>.</h1>
      <p class="lede masthead__sub">A site that cannot be found, a story that wants to be a film, or a product
        that does not exist yet — pick the door that fits.</p>
    </div>
  </section>

  <section class="chapter" style="padding-top: clamp(48px, 7vw, 90px);">
    <div class="wrap">
      <div class="rule" style="margin-bottom: clamp(24px, 3.5vw, 40px);">
        <span><span class="rule__num">01</span> — Three ways in</span>
        <span>One inbox, read by one person</span>
      </div>

{PATHS}

      <div style="margin-top: clamp(48px, 7vw, 84px);">
        <div class="rule" style="margin-bottom: clamp(26px, 3.5vw, 42px);">
          <span><span class="rule__num">02</span> — Direct</span>
          <span>Or write straight to the inbox</span>
        </div>
        <p data-reveal>
          <a class="coda__email" href="mailto:shithinrams2001@gmail.com">shithinrams2001@gmail.com</a>
        </p>
        <p class="lede" data-reveal style="margin-top: clamp(20px, 3vw, 30px);">Say what you are working on and
          what is stuck. If it is a good fit I will answer with a time; if it is not, I will say so.</p>
      </div>

      <div style="margin-top: clamp(52px, 7vw, 90px);">
        <div class="rule" style="margin-bottom: 0;">
          <span><span class="rule__num">03</span> — Elsewhere</span>
          <span>Ventures, tools and profiles</span>
        </div>
        <div class="ledger">
          <a class="ledger__row" data-reveal href="https://theblackit.com" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Studio</span>
            <span class="ledger__term">theblackit ↗</span>
            <span class="ledger__desc">The product lab — sovereign software and community apps.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://clockroach.work/" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Tool</span>
            <span class="ledger__term">Clockroach ↗</span>
            <span class="ledger__desc">Time tracking that gets out of the way.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://chromewebstore.google.com/detail/brain-crawl/opgjgghmabeencknffaifddjcnallngp" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Extension</span>
            <span class="ledger__term">Brain Crawl ↗</span>
            <span class="ledger__desc">Daily search quizzes, in the new tab.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://www.linkedin.com/in/shithin-ram-158327246/" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Profile</span>
            <span class="ledger__term">LinkedIn ↗</span>
            <span class="ledger__desc">Professional history and slow replies.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://www.instagram.com/_shithin_s_/" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Social</span>
            <span class="ledger__term">Instagram ↗</span>
            <span class="ledger__desc">Frames, stills and whatever the light was doing that day.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://github.com/shithins/" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Code</span>
            <span class="ledger__term">GitHub ↗</span>
            <span class="ledger__desc">Repositories, experiments and half-finished ideas.</span>
          </a>
          <a class="ledger__row" data-reveal href="https://www.youtube.com/@EkalavyansStudio" target="_blank" rel="noopener noreferrer">
            <span class="ledger__num">Film</span>
            <span class="ledger__term">Ekalavyan Studios ↗</span>
            <span class="ledger__desc">Short films and moving images.</span>
          </a>
        </div>
      </div>

      <div class="spread" style="margin-top: clamp(56px, 8vw, 100px);">
        <div class="spread__main" data-reveal>
          <h2 class="h2">Kozhikode, Kerala. <em>IST</em> (UTC+5:30).</h2>
        </div>
        <div class="spread__aside body" data-reveal>
          <p>Remote by default, on the Malabar coast by preference. The best time to reach me is the morning,
            before the crawlers wake up.</p>
          <p><a href="tel:+917025638802">+91 70256 38802</a> — call or WhatsApp.</p>
        </div>
      </div>
    </div>
  </section>
"""
    page(
        "contact.html",
        "Contact — Shithin Ram",
        "Get in touch with Shithin Ram directly for collaborations and ideas.",
        "contact.html", "contact.html", body, "V / Contact",
    )


def main():
    print("Building shithin.com — Field Notes…")
    home()
    work_page()
    studio_page()
    services_page()
    cinema_page()
    contact_page()
    print("✓ All pages generated.")


if __name__ == "__main__":
    main()
