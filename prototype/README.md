# shithin.com — "Field Notes"

A second, quieter direction for the main domain. **ShithinOS '98 stays where it
is** (os.shithin.com); this is a parallel design to compare against it, not a
replacement for it yet.

## Run it

    cd prototype
    python3 ../serve.py 8130      # Range-capable; plain http.server is fine here

Then open <http://127.0.0.1:8130>.

## Rebuild

Every page is generated, so the top bar, the fixed rail, the chapter furniture
and the footer stay identical across all six:

    python3 tools/build.py                 # writes *.html from tools/build.py
    python3 tools/make_forest_art.py       # regenerates the forest image family
    python3 tools/make_art.py              # procedural atmosphere plates (og, legacy)
    python3 tools/make_footer_art.py       # legacy cloud scene (no longer referenced)

`tools/build.py` holds the nav, the footer link map and every page's markup.
**Edit there, not in the generated HTML.**

## Design direction

The brief was that the previous version read as a SaaS product site rather than
a personal one. The diagnosis was specific, and so is the fix:

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
- **Print furniture**: numbered chapters (`01 — The Field`), a house rule with a
  label on each side, coordinates (`11.2588° N / 75.7804° E`), a fixed rail
  carrying the running head and current chapter, and a 1px reading-progress line.
- **Asymmetry over centring.** Two-column spreads put the statement on one side
  and the running text on the other; nothing is stacked dead centre.
- **Motion is slow and subordinate to the type**: a masked line-reveal on the
  overture, a 26px parallax drift on plates, staggered fades elsewhere. All of it
  is disabled under `prefers-reduced-motion`, which renders the final state.
- **The footer is a colophon**, not a billboard: a thin forest plate carrying
  the name, then the credits, the link index and the ambience control. The old
  giant `SHITHIN.COM` over clouds was a different site's ending.
- **Cinema is the first line of the record**, not a footnote. The roles ledger —
  on the home page and in the Studio — opens with Creative director at
  Ekalavyan Studios, then theblackit, then the SEO lead, and closes with
  "Human". Experience in search is stated plainly; it is not allowed to lead.
- **Three doors, one page.** The coda and the contact page share a single
  component: Search & the website (→ contact), Share a story (→ contact), and
  Have a product idea (→ theblackit.com). No generic "book a call" block.
- **Cinema is treated as the emotional centre.** The Frame chapter and the
  Cinema page open the journal as chapter 01, and show the set photographs as
  film stills — 16:9 and 2.39:1 frames with frame numbers and timecodes —
  because a director's site should look at images the way a director does.
  The cream of the film is the shooting night itself, not a forest snapshot.
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
| `index.html` | Overture, then chapters: **The Frame (01)**, The Lab (02), The Field (03), The Person (04), Coda (05) |
| `work.html` | Products and extensions as a printed index |
| `studio.html` | Biography, roles ledger, working ethos |
| `services.html` | Engagement models, five-step process, FAQ |
| `cinema.html` | Ekalavyan Studios, directing, criticism |
| `contact.html` | Correspondence, and a directory of everything else |
| `css/site.css` | The whole design system, in numbered sections |
| `js/site.js` | Rail, progress, parallax, reveals, clock — no dependencies |
| `tools/build.py` | Page templates and all copy |
| `tools/make_art.py` | Procedural atmosphere plates |
| `tools/make_footer_art.py` | Composes the footer scene from the landscape photo |

## About the imagery

The site runs on **one forest image family**, all generated from the photographs
already in `img/` — nothing is fetched, nothing is licensed. `make_forest_art.py`
grades every source into the same palette (deep teal-green shadows, warm amber
highlights, vignette, grain) and cuts it to the shapes the layout needs:

| Asset | Use |
|---|---|
| `forest-hero.webp` | the overture (moss macro) |
| `forest-wide-01/02.webp` | page mastheads and plates |
| `forest-tall.webp` | the editorial figure beside the record |
| `forest-strip.webp` | the colophon plate |
| `forest-backdrop.webp` | blurred, very dark — the whole page's ground |
| `frame-set-01/02/03/wide.webp` | cinema stills cut from the supplied film-set photographs |
| `frame-01…04.webp` | forest stills: canopy, detail, ridge |

Because every page shares the family, the site reads as one place rather than as
six templates. Extra grades are applied live per climate through the `clim-img`
class, so a night visit is a night forest without shipping duplicate files.

Procedural plates (`page-*.webp`, `og.webp`) still exist for `og:image` and as
fallbacks but no longer appear in the layout.

The footer scene is built around the wordmark rather than the other way round: a
2:1 asset whose sky is graded dark exactly where the letters sit, stretched to
fill the box (`100% 100%`) rather than `cover`-cropped. Cover-cropping is what
once pushed the bright cumulus bank out of view and left the footer showing
nothing but dark sky.

## Notes

- The prototype is self-contained: no framework, no trackers. `tools/` is build
  time only and is not linked from the pages.
- Reveal animations are scoped to `.js`, so with JavaScript disabled every
  section is visible rather than blank.
- Copy is recovered from this repo's git history — the original `about.html`,
  `cinema.html` and `projects.html` prose before those files became redirect
  stubs — plus the services content. Only the opening lines are new.
- `img/hill-foreground.jpg`, `img/lotus-footer.jpg` and `img/clouds.jpg` are no
  longer referenced directly by any page; they are source material for the
  forest family (the ridge and the hanging-lotus set still are cut from them).
  `img/footer-scene.webp` from the old footer is also retained but unused.
- Share links, `sitemap.xml` and the redirect files still point at the current
  live URLs; they would need updating if this becomes the real site.
