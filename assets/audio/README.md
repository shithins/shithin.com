# assets/audio

The desktop wave on `index.html` plays a track from this folder.

## Required file

    assets/audio/the-sign.mp3

Put a **licensed or self-owned** track here under that exact filename. The
`<audio>` element in `index.html` points at it:

    <audio id="wave-audio" src="assets/audio/the-sign.mp3" preload="metadata" loop></audio>

## Why it is not in the repository

The track originally used here was commercial copyrighted music ("The Sign" by
Ace of Base). Committing it to a public repository would be a licensing
exposure and add ~6.4 MB to the git history permanently, so `*.mp3` is ignored.

## If the file is missing

Nothing breaks. The wave still animates on click, and the hint under it shows
`⚠ AUDIO UNAVAILABLE` instead of playing. Check the browser console for the
load error.

Prefer a small file (a 60-90 second loop at 128 kbps is roughly 1 MB) so the
page stays fast — the audio is `preload="metadata"`, so it is not downloaded
until someone clicks the wave.
