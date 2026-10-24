# shithin.com — "Field Notes"

The live site for shithin.com: a cinematic editorial journal, generated as six
static pages. **ShithinOS '98 lives on at os.shithin.com** and is no longer the
main domain.

## Run it

    python3 serve.py 8099

Then open <http://127.0.0.1:8099>. Any static server works; `serve.py` is only
there because it supports HTTP Range requests, which the old media page needed.

## Rebuild

Every page is generated, so the top bar, the fixed rail, the chapter furniture
and the colophon stay identical across all six:

    python3 tools/build.py                 # writes *.html from tools/build.py
    python3 tools/make_forest_art.py       # regenerates the forest image family

`tools/build.py` holds the nav, the footer link map and every page's markup.
**Edit there, not in the generated HTML.**

Older generators are retained but no longer referenced by the layout:

    python3 tools/make_art.py              # procedural atmosphere plates (og, legacy)
    python3 tools/make_footer_art.py       # legacy cloud scene

## Design direction

The brief was that an earlier version read as a SaaS product site rather than a
personal one. The diagnosis was specific, and so is the fix:

| Was (SaaS signature) | Now (editorial signature) |
|---|---|
| Centred hero: pill badge with pulse dot, headline, sub, two CTAs | Full-bleed overture, type set low and left, one hairline of metadata |
| Three glassmorphic feature cards with emoji icons | Numbered chapters and a capability ledger — rules, not boxes |
| Product cards with status pills and tag chips | A printed **index**: number, name, line of description, folio |
| Capsule nav floating over the page | A full-width hairline bar; a fixed vertical rail down the left |
| Plus Jakarta Sans doing the UI work | **No sans-serif anywhere** — Instrument Serif, Newsreader, JetBrains Mono |
| Neon lime accent + glowing CTAs | One warm accent, golden-hour amber, on warm bone |

Concretely:

- **Instrument Serif** for display, **Newsreader** for body, **JetBrains Mono**
  for every label, folio, coordinate and running head. The absence of a neutral
  interface grotesque is the single biggest reason it stops reading as a template.
- **Print furniture**: numbered chapters, a house rule with a label on each side,
  coordinates (`11.2588° N / 75.7804° E`), a fixed rail carrying the running head
  and current chapter, and a 1px reading-progress line.
- **Asymmetry over centring.** Two-column spreads put the statement on one side
  and the running text on the other; nothing is stacked dead centre.
- **Motion is slow and subordinate to the type**: a masked line-reveal on the
  overture, a 26px parallax drift on plates, staggered fades elsewhere. All of it
  is disabled under `prefers-reduced-motion`, which renders the final state.
- **The footer is a colophon**, not a billboard: a thin forest plate carrying the
  name, then the credits, the link index, social links and the ambience control.
- **Cinema opens the journal as chapter 01** — The Frame, then The Lab, then The
  Field, then The Person, then the Coda. The roles ledger leads with Creative
  director at Ekalavyan Studios, then theblackit, then the SEO lead, and closes
  with "Human". Experience in search is stated plainly; it is not allowed to lead.
- **The cinema page shows set photographs as film stills** — 16:9 and 2.39:1
  frames with frame numbers and timecodes — because a director's site should look
  at images the way a director does.
- **Three doors, one page.** The coda and the contact page share a single
  component: Search & the website (→ contact), Share a story (→ email), and Have
  a product idea (→ theblackit.com). No generic "book a call" block.
- **The header carries only Work, Cinema and Contact.** Studio and Services live
  in the footer and are linked from the homepage sections that introduce them.
- All body and label colours meet WCAG AA on the ink background (lowest is
  4.62:1); the faintest tone is decorative only.

## The forest follows the visitor

The whole site sits in one forest. Its hour and weather change with the visitor:

| Climate | The forest does | Set by |
|---|---|---|
| **Night** | fireflies drift through the trees; deeper, cooler grade | local clock after 19:00, or the weather API's `is_day` |
| **Day** | butterflies and small birds cross the canopy; warmer grade | local clock 06:00–19:00 |
| **Rain** | rain falls over the whole place; desaturated grade | current `weather_code` in the rain ranges |

Everything is drawn on a canvas per scene (`[data-fauna]`) by `js/site.js`, with
`requestAnimationFrame` and per-field viewport culling so offscreen scenes cost
nothing.

Detection is intentionally shy and needs no keys:

1. The local clock paints the page immediately.
2. If — and only if — the network allows, the guess is refined by asking
   `ipapi.co` for a coarse location and `api.open-meteo.com` for the current
   weather. Both fail silently after 3.2s.
3. A visitor can pin **Auto / Day / Night / Rain** from the colophon; the choice
   is remembered in `localStorage`.

Two privacy notes, since this makes two third-party requests: the coarse
location is IP-derived (no permission prompt), and the results are cached in
`sessionStorage` for 30 minutes. Remove `refine()` in `js/site.js` to keep the
site fully offline — the clock fallback still works.

Under `prefers-reduced-motion` no canvas is created at all, and every reveal
renders in its final state.

## Structure

| File | Purpose |
|---|---|
| `index.html` | Overture, then: **The Frame (01)**, The Lab (02), The Field (03), The Person (04), Coda (05) |
| `cinema.html` | Ekalavyan Studios — the reel, statement, programme |
| `work.html` | Products and extensions as a printed index |
| `studio.html` | Biography, roles ledger, working ethos |
| `services.html` | Engagement models, five-step process, FAQ |
| `contact.html` | Three ways in, direct email, directory |
| `css/site.css` | The whole design system, in numbered sections |
| `js/site.js` | Climate, fauna, rail, progress, parallax, reveals, clock |
| `tools/build.py` | Page templates and all copy |
| `tools/make_forest_art.py` | Grades and cuts the forest image family |
| `serve.py` | Local dev server (Range-capable) |
| `.htaccess` | Hostinger MIME types, caching, compression |
| `_redirects` / `vercel.json` | Legacy URL redirects for Netlify/Cloudflare and Vercel |
| `sitemap.xml`, `robots.txt` | Crawling |

Archived, not linked: `about.html` and `projects.html` (redirect stubs retained
for old inbound links) and `assets/`.

## About the imagery

The site runs on **one forest image family**, all generated from the photographs
in `img/` — nothing is fetched, nothing is licensed. `make_forest_art.py` grades
every source into the same palette (deep teal-green shadows, warm amber
highlights, vignette, grain) and cuts it to the shapes the layout needs:

| Asset | Use |
|---|---|
| `forest-hero.webp` | the overture (moss macro) |
| `forest-wide-01/02.webp` | page mastheads and plates |
| `forest-tall.webp` | the editorial figure beside the record |
| `forest-strip.webp` | the colophon plate |
| `forest-backdrop.webp` | blurred, very dark — the whole page's ground |
| `frame-set-01…05`, `frame-set-wide.webp` | cinema stills cut from the film-set photographs |
| `frame-01…04.webp` | forest stills: canopy, detail, ridge |

Because every page shares the family, the site reads as one place rather than as
six templates. Extra grades are applied live per climate through the `clim-img`
class, so a night visit is a night forest without shipping duplicate files.

Procedural plates (`page-*.webp`, `og.webp`) still exist for `og:image` and as
fallbacks but no longer appear in the layout.

## Deploying

The site is plain static files served from the repository root. On Hostinger,
upload the tracked files (not `tools/`, `deploy-os/` or the zips) and keep
`.htaccess`; on Netlify/Cloudflare use `_redirects`, on Vercel `vercel.json`.

When this design was promoted to the main domain, the staging
`X-Robots-Tag: noindex` block was removed from `.htaccess` — **do not reintroduce
it**, or the whole site disappears from search. The old `/cinema.html → /`
redirect was also removed, because `/cinema.html` is a real page now.

## SEO

- Every page has a unique title and meta description, one `<h1>`, correct
  absolutes canonicals, Open Graph and Twitter cards, and a JSON-LD graph
  (`Person` + `Organization` + `WebSite` + `WebPage`, plus `BreadcrumbList` on
  subpages) built in `structured_data()`.
- `img/og.jpg` is a 1200×630 JPEG: WebP share previews are still unreliable on
  some platforms, LinkedIn in particular.
- Below-the-fold artwork is `loading="lazy"`; the overture and mastheads stay
  eager (the overture with `fetchpriority="high"`) so LCP is not deferred.
- `sitemap.xml` lists all six pages, `robots.txt` allows crawling, and legacy
  `/about.html` and `/projects.html` redirect home.

## Notes

- The site is self-contained: no framework, no trackers. `tools/` is build time
  only and is not linked from the pages.
- Reveal animations are scoped to `.js`, so with JavaScript disabled every
  section is visible rather than blank.
- Copy came from this repo's history — the original `about.html`, `cinema.html`
  and `projects.html` prose before those files became redirect stubs — plus the
  services content, rewritten.
- `img/hill-foreground.jpg`, `img/lotus-footer.jpg` and `img/clouds.jpg` are not
  referenced directly by any page; they are source material for the forest family.
