#!/usr/bin/env python3
"""
Build the forest image family for shithin.com — "Field Notes".

The site needs one consistent visual world, so every photograph is graded into
the same cinematic palette (deep teal-green shadows, warm amber highlights,
vignette, fine grain) and cut to the shapes the layout needs:

    forest-hero.webp      2400x1350  the overture (moss macro)
    forest-wide-01.webp   2200x1100  warm canopy — mastheads, plates
    forest-wide-02.webp   2200x1100  cool ridge  — mastheads, plates
    forest-tall.webp      1100x1500  vertical editorial figure
    forest-strip.webp     2400x520   letterbox band for section breaks
    forest-backdrop.webp  1600x900   heavily blurred, very dark: the page ground
    frame-01..04.webp     1600x900   cinema stills (canopy, set, location, detail)

Sources are the photographs already in img/: nature-hero.jpg, canopy.jpg,
hill-foreground.jpg and lotus-footer.jpg. Nothing is fetched.

Run from the prototype folder:
    python3 tools/make_forest_art.py [--preview]
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "img")


def load(name):
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    return im


def crop_norm(im, box):
    """box = (x0, y0, x1, y1) as fractions of width/height."""
    w, h = im.size
    x0, y0, x1, y1 = box
    return im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))


def grade(im, size, blur=0.0, lift=(0.02, 0.05, 0.05), warm=0.06,
          sat=0.88, contrast=1.06, vignette=0.55, grain=2.2, dark=1.0):
    """Push an image into the house palette.

    lift    — colour added to the shadows (keeps blacks teal, never grey)
    warm    — how far the highlights lean amber
    dark    — overall exposure multiplier
    """
    im = im.resize(size, Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))

    a = np.asarray(im).astype(np.float32) / 255.0
    h, w = a.shape[:2]

    # contrast around a slightly lifted pivot, then exposure
    a = (a - 0.42) * contrast + 0.42
    a *= dark

    # split-tone: lift shadows toward teal, highlights toward amber
    lum = a.mean(2, keepdims=True)
    shadow_w = np.clip(1.0 - lum * 2.2, 0, 1)
    high_w = np.clip((lum - 0.45) * 2.0, 0, 1)
    a += shadow_w * np.array(lift, np.float32)
    a += high_w * np.array([warm, warm * 0.72, warm * 0.30], np.float32)

    # saturation
    g = a.mean(2, keepdims=True)
    a = g + (a - g) * sat

    # vignette
    vy, vx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (((vx / w - 0.5) * 2) ** 2 + ((vy / h - 0.5) * 2) ** 2) ** 1.35
    a *= np.clip(1.0 - vignette * d, 0, 1)[..., None]

    # grain
    rng = np.random.default_rng(7)
    a += (rng.random((h, w, 1)).astype(np.float32) - 0.5) * (grain / 255.0)

    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8), "RGB")


def save(im, name, quality=84):
    path = os.path.join(IMG, name)
    im.save(path, "WEBP", quality=quality, method=6)
    print(f"  {name:22} {im.size[0]}x{im.size[1]}  {os.path.getsize(path)/1024:7.1f} KB")


def main():
    moss = load("nature-hero.jpg")
    canopy = load("canopy.jpg")
    hills = load("hill-foreground.jpg")
    lotus = load("lotus-footer.jpg")

    # ---- the overture: moss macro, warm shadow, deep vignette
    save(grade(crop_norm(moss, (0.03, 0.10, 0.97, 0.94)), (2400, 1350),
               lift=(0.020, 0.048, 0.044), warm=0.05, sat=0.86,
               contrast=1.07, vignette=0.62, grain=2.4, dark=0.95), "forest-hero.webp")

    # ---- warm canopy, for mastheads and plates
    save(grade(crop_norm(canopy, (0.02, 0.04, 0.98, 0.90)), (2200, 1100),
               lift=(0.018, 0.044, 0.040), warm=0.10, sat=0.82,
               contrast=1.05, vignette=0.60, grain=2.2, dark=0.92), "forest-wide-01.webp")

    # ---- cool ridge, for the quieter pages
    # crop below the photograph's blown-out sky band so only the field reads
    save(grade(crop_norm(hills, (0.02, 0.44, 0.98, 1.00)), (2200, 1100),
               lift=(0.012, 0.038, 0.050), warm=0.03, sat=0.80,
               contrast=1.10, vignette=0.70, grain=2.2, dark=0.72), "forest-wide-02.webp")

    # ---- vertical editorial figure
    save(grade(crop_norm(canopy, (0.28, 0.02, 0.78, 0.98)), (1100, 1500),
               lift=(0.016, 0.042, 0.038), warm=0.08, sat=0.84,
               contrast=1.06, vignette=0.58, grain=2.3, dark=0.90), "forest-tall.webp")

    # ---- letterbox band
    save(grade(crop_norm(canopy, (0.00, 0.16, 1.00, 0.62)), (2400, 520),
               lift=(0.014, 0.040, 0.040), warm=0.09, sat=0.84,
               contrast=1.06, vignette=0.44, grain=2.0, dark=0.94), "forest-strip.webp")

    # ---- the page ground: blurred so type never competes with it
    save(grade(crop_norm(canopy, (0.05, 0.10, 0.95, 0.85)), (1600, 900),
               blur=9.0, lift=(0.010, 0.030, 0.034), warm=0.05, sat=0.72,
               contrast=1.02, vignette=0.70, grain=1.4, dark=0.55), "forest-backdrop.webp")

    # ---- cinema stills -----------------------------------------------------
    # 01 the light through the canopy — the "hero frame"
    save(grade(crop_norm(canopy, (0.16, 0.06, 0.92, 0.74)), (1600, 900),
               lift=(0.016, 0.042, 0.040), warm=0.12, sat=0.82,
               contrast=1.08, vignette=0.58, grain=2.6, dark=0.90), "frame-01.webp")

    # 02 the production design — hanging lotus leaves, lit like a set
    # the lotus set is the only high-key source; pull it right down and tint it
    # green so it sits inside the family instead of glowing out of it
    save(grade(crop_norm(lotus, (0.02, 0.04, 0.94, 0.96)), (1600, 900),
               lift=(0.014, 0.048, 0.036), warm=0.05, sat=0.62,
               contrast=1.16, vignette=0.55, grain=2.8, dark=0.40), "frame-02.webp")

    # 03 the location — the ridge and the rider
    save(grade(crop_norm(hills, (0.06, 0.46, 0.98, 0.98)), (1600, 900),
               lift=(0.014, 0.038, 0.046), warm=0.05, sat=0.80,
               contrast=1.12, vignette=0.66, grain=2.6, dark=0.70), "frame-03.webp")

    # 04 the detail — a close crop of the moss, shallow and warm
    save(grade(crop_norm(moss, (0.20, 0.30, 0.80, 0.94)), (1600, 900),
               lift=(0.018, 0.042, 0.036), warm=0.09, sat=0.86,
               contrast=1.06, vignette=0.58, grain=2.6, dark=0.86), "frame-04.webp")

    # ---- cinema: production stills cut from the supplied set photographs.
    # These are samples, not final art — graded into the house palette and
    # cropped differently, so they sit inside the forest family rather than
    # looking like stock dropped in.
    set1 = load("film-set-01.jpg")
    set2 = load("film-set-02.jpg")

    save(grade(crop_norm(set1, (0.00, 0.02, 1.00, 0.98)), (1600, 900),
               lift=(0.020, 0.052, 0.056), warm=0.10, sat=0.86,
               contrast=1.06, vignette=0.52, grain=2.4, dark=0.80), "frame-set-01.webp")

    save(grade(crop_norm(set1, (0.22, 0.06, 0.74, 0.98)), (1600, 900),
               lift=(0.018, 0.050, 0.052), warm=0.08, sat=0.84,
               contrast=1.08, vignette=0.56, grain=2.6, dark=0.78), "frame-set-02.webp")

    save(grade(crop_norm(set2, (0.00, 0.00, 1.00, 1.00)), (800, 450),
               lift=(0.020, 0.052, 0.056), warm=0.10, sat=0.86,
               contrast=1.06, vignette=0.50, grain=2.8, dark=0.84), "frame-set-03.webp")

    save(grade(crop_norm(set1, (0.00, 0.16, 1.00, 0.84)), (1600, 686),
               lift=(0.020, 0.052, 0.056), warm=0.10, sat=0.86,
               contrast=1.06, vignette=0.50, grain=2.4, dark=0.82), "frame-set-wide.webp")

    # Two more framings of the same shooting night, so the reel reads as a
    # sequence of set-ups rather than one photograph cropped twice.
    save(grade(crop_norm(set1, (0.06, 0.08, 0.52, 0.92)), (1600, 900),
               lift=(0.024, 0.058, 0.050), warm=0.16, sat=0.90,
               contrast=1.10, vignette=0.58, grain=2.6, dark=0.74), "frame-set-04.webp")

    crew = set1.transpose(Image.FLIP_LEFT_RIGHT)
    save(grade(crop_norm(crew, (0.50, 0.06, 1.00, 0.94)), (1600, 900),
               lift=(0.016, 0.048, 0.062), warm=0.04, sat=0.80,
               contrast=1.10, vignette=0.60, grain=2.6, dark=0.76), "frame-set-05.webp")

    if "--preview" in sys.argv:
        # a contact sheet so the family can be judged as a set, not one by one
        names = ["forest-hero.webp", "forest-wide-01.webp", "forest-wide-02.webp",
                 "forest-tall.webp", "forest-strip.webp", "forest-backdrop.webp",
                 "frame-01.webp", "frame-03.webp",
                 "frame-set-01.webp", "frame-set-02.webp", "frame-set-03.webp",
                 "frame-set-04.webp", "frame-set-05.webp", "frame-set-wide.webp"]
        thumbs = []
        for n in names:
            im = Image.open(os.path.join(IMG, n)).convert("RGB")
            im.thumbnail((420, 420), Image.LANCZOS)
            thumbs.append((n, im))
        cols, cw, ch = 3, 430, 320
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rows * ch), (8, 9, 10))
        for i, (n, im) in enumerate(thumbs):
            x = (i % cols) * cw + 5
            y = (i // cols) * ch + 5
            sheet.paste(im, (x, y))
        p = "/tmp/forest-family.png"
        sheet.save(p)
        print(f"  contact sheet -> {p}")


if __name__ == "__main__":
    main()
