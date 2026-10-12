# shithin.com — minimal prototype

A second, quieter direction for the main domain. **ShithinOS '98 stays where it
is** (os.shithin.com); this is a parallel design to compare against it, not a
replacement for it yet.

## Run it

    cd prototype
    python3 ../serve.py 8130      # Range-capable; plain http.server is fine here

Then open <http://127.0.0.1:8130>.

## Rebuild

Pages are generated so the header, the four-column footer and the reveal delays
stay identical across all six:

    python3 tools/build.py                 # writes ../*.html from tools/build.py
    python3 tools/make_art.py              # regenerates img/*.webp

`tools/build.py` holds the nav, the footer link map and every page's markup.
Edit there, not in the generated HTML.

## Design direction

Drawn from the supplied mood board, deliberately mixed rather than copied:

- **Editorial serif display** (Newsreader) with a single italic emphasis word per
  headline — the "Built for the *thinkers*" / "Where dreams rise through the
  *silence*" device.
- **Dark, image-led hero** on a near-black canvas with one warm light source and
  hairline vegetation silhouettes backlit against it.
- **Capsule chrome**: pill navigation, pill CTAs, one luminous amber button.
  Only one primary action per screen.
- **Monospace micro-labels** in wide letterspacing for section eyebrows.
- **Four-column editorial footer** with monospace column headings over serif-ish
  links, a brand block with social pills, and a divided bottom bar carrying the
  copyright, a tagline and a live clock.

## Structure

| File | Purpose |
|---|---|
| `index.html` | Minimal hero, ticker, four featured projects, three services, one CTA |
| `work.html` | Products, extensions and applications |
| `studio.html` | Bio, experience ledger, capabilities, facts |
| `services.html` | Engagement models, five-step process, FAQ |
| `cinema.html` | Ekalavyan Studios, directing, acting, criticism |
| `contact.html` | Contact paths, what to send, subscribe |
| `css/site.css` | The whole design system |
| `js/site.js` | Header state, reveal-on-scroll, clock, subscribe |
| `img/*.webp` | Generated artwork |

## About the imagery

`img/*.webp` is **procedurally generated**, not photography: a dark field, one
warm glow at the horizon, and thin backlit vegetation silhouettes. It is a
placeholder that matches the *mood* of the references. Swap in real photographs
when you have them — the CSS only depends on the aspect ratio and a bright focal
area roughly centred and slightly below middle, so a photo drop-in needs no CSS
change.

Generated files are safe to overwrite.

## Notes

- The prototype is self-contained: no build step, no framework, no trackers.
- Reveal animations are scoped to `.js`, so with JavaScript disabled every
  section is visible rather than blank.
- Copy is recovered from this repo's git history — the original `about.html`,
  `cinema.html` and `projects.html` prose before those files became redirect
  stubs — plus the services content. Only the hero lines are new.
- All text colours meet WCAG AA on the ink background (lowest is 4.63:1).
- Share links, `sitemap.xml` and the redirect files still point at the current
  live URLs; they would need updating if this becomes the real site.
