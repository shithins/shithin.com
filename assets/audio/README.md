# assets/audio

The desktop wave on `index.html` plays a track from this folder.

## Required file

    assets/audio/theme.mp3

Put a **licensed or self-owned** track here under that exact filename. The
`<audio>` element in `index.html` points at it:

    <audio id="wave-audio" src="assets/audio/theme.mp3#t=20" preload="metadata" loop></audio>

## Playback starts 20 seconds in

The wave skips the intro and begins at **20 seconds**. Two places control this:

1. `#t=20` — the media fragment on the `<audio src>` above.
2. `WAVE_START_SECONDS = 20` — in the `initCrawlGraph()` function in
   `index.html`. This also re-applies the offset on `loadedmetadata`,
   `loadeddata`, `canplay`, `playing` and `timeupdate`, because some browsers
   drop a seek issued while the media is still loading.

Change both if you want a different start point, or a track whose duration is
under ~21 seconds (the offset is clamped to `duration - 0.5` so it can never
seek past the end).

## Why it is not in the repository

The tracks used here have been commercial copyrighted music, most recently a
song from *Manichitrathazhu* (1993). Committing that to a public repository
would be a licensing exposure and add ~6.7 MB to the git history permanently,
so `*.mp3` is ignored.

## If the file is missing

Nothing breaks. The wave still animates on click, and the hint under it shows
`⚠ AUDIO UNAVAILABLE` instead of playing. Check the browser console for the
load error.

## Keeping the page fast

Prefer a small file — a 60-90 second loop at 128 kbps is roughly 1 MB. The
audio is `preload="metadata"`, so nothing but the header is downloaded until
someone clicks the wave. A full-length 4:51 track at 192 kbps is ~6.7 MB, which
is only fetched on click but is heavy for anyone on mobile data.

To clip the track without losing quality, with ffmpeg:

    ffmpeg -i source.mp3 -ss 20 -t 75 -codec copy theme.mp3

That trims to a 75-second loop starting at 0:20; set `WAVE_START_SECONDS = 0`
and drop `#t=20` if you pre-trim it.
