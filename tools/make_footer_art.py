#!/usr/bin/env python3
"""
Build the dark WANDER footer scene from the photograph.

  img/footer-landscape.jpg  ->  img/footer-scene.webp

Why the previous footer looked cheap
------------------------------------
Three separate faults, all in the footer art:

1. `clouds.jpg` was tiled with `repeat-x`. A JPEG edge is a hard seam, so the
   tiling showed as rectangular blocks across the letters.
2. `mix-blend-mode: screen` over a near-black base lifted the whole middle band
   into a grey haze instead of leaving individual clouds.
3. The photograph's bright cumulus bank sits in a fixed band — rows 320-360 of
   768, mean luminance 122 — and `object-fit: cover` slides that band vertically
   but never removes it. A measured sweep of 8 crop positions x 6 text offsets
   put the glyphs on that band every time, worst case 3.04:1 contrast, below the
   4.5:1 WCAG AA floor.

What this does
--------------
Keeps the photograph's landscape and rebuilds the sky above it as a dark graded
field the white wordmark can sit on. The finished asset is 2:1, the same
proportion as the footer's scene box, and the CSS stretches it to exactly fill
that box (`background-size: 100% 100%`) rather than cropping it.

That last point is the one that is easy to get wrong. With `cover`, the asset is
scaled to cover the box and the excess is cropped: a 1376x1536 asset in a
1440x633 box lost 39% of its height, which pushed the bright cumulus bank
completely out of the visible window. The footer then showed nothing but dark
sky — the landscape never appeared at all. Matching the proportions and
stretching means every zone below lands where it is meant to at every width.

Zones (fractions of the asset, which map 1:1 onto the scene box):

     0% - 32%    dark graded night sky        <- the wordmark sits here
    32% - 62%    the photo's own sky, darkened to meet it
    62% - 72%    the photo's bright cumulus   <- the glowing horizon
    72% - 100%   hills, grass, cyclist        <- untouched

Run from the prototype folder:
    python3 tools/make_footer_art.py [--preview]
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "img")

SRC = os.path.join(OUT, "footer-landscape.jpg")
DST = os.path.join(OUT, "footer-scene.webp")

OUT_W, OUT_H = 2000, 1000          # 2:1, matching the scene box exactly
CLOUD_LINE_OUT = 0.62              # where the photo's bright cumulus lands
SKY_TOP_DARKEN = 0.040             # sky multiplier at the very top
PHOTO_SKY_DARKEN = 0.22            # sky multiplier at the extension join


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3.0 - 2.0 * t)


def main():
    img = Image.open(SRC).convert("RGB")
    iw, ih = img.size

    # The photo's own bright cumulus begins at ~41.5% of its height; scale the
    # photo so that line lands on CLOUD_LINE_OUT of the output.
    photo_scale = (OUT_H * CLOUD_LINE_OUT) / (ih * 0.415)
    pw, ph = int(round(iw * photo_scale)), int(round(ih * photo_scale))

    # Place it so the cloud line lands exactly on CLOUD_LINE_OUT.
    photo_top = int(round(OUT_H * CLOUD_LINE_OUT - 0.415 * ph))

    photo = np.asarray(img.resize((pw, ph), Image.LANCZOS)).astype(np.float32) / 255.0

    # darken the photo's sky (everything above its cloud line), leaving the
    # cumulus, hills and grass untouched. The exponent keeps the sky dark for
    # longer and then opens up quickly near the cloud line, so the top edge of
    # the asset fades into the page's own background colour instead of starting
    # as a visible lighter band.
    yp = np.linspace(0, 1, ph, dtype=np.float32)[:, None]
    t = np.clip(yp / 0.415, 0, 1)
    # a linear ramp: darkest at the top, reaching full brightness at the cloud
    # line. Smoothstep would hold a mid grey across the top half, which reads as
    # a lighter band where the footer meets the page.
    ramp = PHOTO_SKY_DARKEN + (1.0 - PHOTO_SKY_DARKEN) * t
    ramp = np.where(yp > 0.415, 1.0, ramp)
    photo *= ramp[..., None]

    # ---- canvas: dark sky above, the photo below it
    canvas = np.zeros((OUT_H, OUT_W, 3), np.float32)
    pad = max(0, (OUT_W - pw) // 2)

    # the photo is narrower than the output only if it was upscaled a lot; fill
    # the side margins with the photo's own darkest tone so they never read as bars
    side = float(photo[-1].mean())
    canvas[:, :] = side * 0.35

    src_x0, src_y0 = 0, 0
    dst_x0, dst_y0 = pad, max(0, photo_top)
    copy_w = min(pw, OUT_W - dst_x0)
    copy_h = min(ph, OUT_H - dst_y0)
    if copy_w > 0 and copy_h > 0:
        canvas[dst_y0:dst_y0 + copy_h, dst_x0:dst_x0 + copy_w] = \
            photo[src_y0:src_y0 + copy_h, src_x0:src_x0 + copy_w]

    # ---- the sky above the photo: dark, graded, with faint structure so it does
    # not read as a flat wash. Texture is the photo's own clouds, heavily blurred.
    ext_h = dst_y0
    if ext_h > 8:
        tex_img = img.filter(ImageFilter.GaussianBlur(3.0)).filter(ImageFilter.GaussianBlur(9.0))
        tex = np.asarray(tex_img.resize((OUT_W, ext_h), Image.LANCZOS)).astype(np.float32) / 255.0
        tex = tex.mean(2, keepdims=True)
        tex = np.clip(tex / max(tex.mean(), 1e-6) * 0.08, 0.0, 0.10)

        # a gradient rather than the photo: the photo's top row is far too bright
        # to sit above the wordmark
        ye = np.linspace(0, 1, ext_h, dtype=np.float32)[:, None]
        base = np.array([0.030, 0.052, 0.049], np.float32)
        ramp_ext = SKY_TOP_DARKEN + (PHOTO_SKY_DARKEN - SKY_TOP_DARKEN) * smoothstep(ye)
        canvas[:ext_h] = base * ramp_ext[..., None] * 9.0 * (1.0 + tex)

    # ---- feather the join so no horizontal line shows
    band = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8))
    canvas = np.asarray(band.filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255.0

    # ---- cool the deep sky so night reads as sky rather than fog
    cool = np.array([0.90, 1.00, 1.04], np.float32)
    y = np.linspace(0, 1, OUT_H, dtype=np.float32)[:, None]
    amt = np.clip(1.0 - y / CLOUD_LINE_OUT, 0, 1) ** 0.8
    canvas = canvas * (1 - amt[..., None] * 0.28) + canvas * cool * amt[..., None] * 0.28

    # ---- fade the very top edge into the page background (#050806). Without
    # this the scene starts as a lighter band across the top of the footer.
    page = np.array([5, 8, 6], np.float32) / 255.0
    h = max(1, int(OUT_H * 0.035))
    f = smoothstep(np.linspace(0, 1, h, dtype=np.float32))[:, None, None]
    canvas[:h] = page * (1 - f) + canvas[:h] * f

    # ---- verify the zones that decide whether the footer works
    em = canvas.mean(2) * 255

    def contrast(lum):
        l = lum / 255.0
        srgb = l / 12.92 if l <= 0.03928 else ((l + 0.055) / 1.055) ** 2.4
        return 1.05 / (srgb + 0.05)

    # the wordmark occupies roughly the top 2%-30% of the scene box
    y0, y1 = int(OUT_H * 0.02), int(OUT_H * 0.30)
    tb = em[y0:y1]
    worst = 0.0
    for cx in range(0, OUT_W, 100):
        col = tb[:, cx:cx + 100]
        if col.size:
            worst = max(worst, np.percentile(col, 99.5))

    cl0, cl1 = int(OUT_H * CLOUD_LINE_OUT), int(OUT_H * (CLOUD_LINE_OUT + 0.06))
    cb = em[cl0:cl1]

    print(f"  photo {iw}x{ih} -> {pw}x{ph}  placed at y={dst_y0}  (pad x={pad})")
    print(f"  canvas {OUT_W}x{OUT_H}   cloud line at {CLOUD_LINE_OUT:.0%}")
    print(f"  wordmark band y={y0}-{y1}: mean {tb.mean():5.1f}  "
          f"p99 {np.percentile(tb, 99):5.1f}  max {tb.max():5.1f}")
    print(f"  cumulus band {CLOUD_LINE_OUT:.0%}-{CLOUD_LINE_OUT + 0.06:.0%}: "
          f"mean {cb.mean():5.1f}  max {cb.max():5.1f}   <- must stay bright")
    print(f"  white-on-band worst-case contrast: {contrast(worst):.2f}:1  "
          f"(WCAG AA large text needs 3.0, normal 4.5)")

    out = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8))
    out.save(DST, "WEBP", quality=86, method=6)
    print(f"  {os.path.basename(DST):24} {OUT_W}x{OUT_H}  {os.path.getsize(DST)/1024:7.1f} KB")

    if "--preview" in sys.argv:
        p = "/tmp/footer-scene-preview.png"
        out.resize((900, 450), Image.LANCZOS).save(p)
        print(f"  preview -> {p}")


if __name__ == "__main__":
    main()
