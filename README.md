# shithin.com

Personal website of Shithin Ram — product builder, SEO specialist and
co-founder of TheBlackit.

## What this is

A single self-contained page that presents the site as **ShithinOS '98**, a
vintage desktop OS: draggable windows, a working CLI terminal, start menu,
taskbar, CRT scanlines and switchable themes.

Everything lives in `index.html` — markup, styles and script — with no build
step, no framework and no external runtime dependencies.

## Local development

Any static server works:

    python3 -m http.server 8099

Then open <http://127.0.0.1:8099>.

## Layout

    index.html            the OS desktop (windows, terminal, snake game)
    services.html         retired page, still reachable by URL
    index-minimal.html    previous crimson design, kept for reference
    projects.html         redirect stub -> index.html#products
    cinema.html           redirect stub -> index.html
    about.html            redirect stub -> index.html
    css/site.css          styles for the retired crimson pages
    js/site.js            script for the retired crimson pages
    assets/               favicon and audio
    _redirects            Netlify / Cloudflare Pages 301s
    vercel.json           Vercel 301s

## Audio note

The desktop wave plays `assets/audio/the-sign.mp3`, which is **not tracked in
git** — the original track was commercial copyrighted music. See
[assets/audio/README.md](assets/audio/README.md). Without that file the wave
still animates and shows "AUDIO UNAVAILABLE".

## Deploying

The repository is the deployable artifact: publish the directory as static
files. Keep `_redirects` (Netlify/Cloudflare) or `vercel.json` (Vercel) so the
retired URLs keep returning 301s.
