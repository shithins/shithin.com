#!/usr/bin/env python3
"""
Generate the atmospheric artwork for the shithin.com minimal prototype.

Procedural stand-ins for the photographic hero images in the mood board.
The recipe that reads correctly, after a first attempt came out as a washed-out
haze:

  1. a near-black base,
  2. ONE tight warm glow at the horizon,
  3. vegetation painted as thin DARK silhouettes against that glow (the light
     does not sit on top of the stems — that is what made it look like rain),
  4. a light particle field, then grain and vignette.

Run from the prototype folder:
    python3 tools/make_art.py
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")


def fbm(h, w, octaves=6, base=2, gain=0.5, seed=0):
    r = np.random.default_rng(seed)
    total = np.zeros((h, w), np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        ry = max(2, int(base * (2 ** o)))
        rx = max(2, int(ry * (w / h)))
        grid = r.random((ry, rx)).astype(np.float32)
        img = Image.fromarray((grid * 255).astype(np.uint8), "L").resize((w, h), Image.BICUBIC)
        total += amp * (np.asarray(img, np.float32) / 255.0)
        norm += amp
        amp *= gain
    return total / norm


def gauss(h, w, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - cx * w) / (rx * w)) ** 2 + ((yy - cy * h) / (ry * h)) ** 2
    return np.exp(-np.clip(d, 0, 40))


def compose(h, w, seed, warm=0.5, horizon=0.62, glow=1.0, density=1.0):
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]

    # ---- 1. base: very dark, faintly gradient
    base = 0.030 + 0.020 * (1 - yy)

    # ---- 2. one tight warm glow at the horizon
    # Horizontal falloff has to kill the light toward the left/right edges,
    # otherwise the glow reads as a hard pill-shaped spotlight.
    xx = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    side = np.clip(1.0 - (np.abs(xx - 0.5) * 2.0) ** 1.9, 0, 1)

    core = gauss(h, w, 0.5, horizon, 0.20, 0.105)          # hot centre
    bloom = gauss(h, w, 0.5, horizon, 0.42, 0.240)         # soft falloff
    wide = gauss(h, w, 0.5, horizon - 0.04, 0.74, 0.440)   # broad lift
    light = (core * 0.95 + bloom * 0.34 + wide * 0.11) * side
    light *= glow

    # texture within the light so it is not a flat blob; multiply keeps the
    # grain inside the glow instead of speckling the whole frame
    tex = fbm(h, w, octaves=7, seed=seed + 5)
    light *= 0.62 + 0.74 * tex
    # faint volumetric wisps drifting through the beam
    wisp = fbm(h, w, octaves=5, seed=seed + 909)
    light *= 0.86 + 0.28 * wisp

    lum = base + light

    # ---- 3. vegetation as dark silhouettes
    sil = np.zeros((h, w), np.float32)

    # 3a. canopy mass hanging from the top, feathered
    canopy = fbm(h, w, octaves=8, seed=seed + 77)
    canopy_top = np.clip((0.62 - yy) / 0.62, 0, 1) ** 1.15
    mass = np.clip((canopy - 0.42) * 2.4, 0, 1) * canopy_top
    sil = np.maximum(sil, mass * 0.92)

    # 3b. stems + heads, drawn as shapes then softened
    layer = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(layer)
    imax = int(210 * density)
    for _ in range(imax):
        x = float(rng.integers(int(w * .015), int(w * .985)))
        head_y = h * (horizon - rng.uniform(0.05, 0.44))
        foot_y = h * (horizon + rng.uniform(0.06, 0.26))
        lean = rng.uniform(-0.06, 0.06) * w
        sway = rng.uniform(-0.02, 0.02) * w
        thick = rng.choice([1, 1, 1, 2, 2, 3])
        shade = int(rng.uniform(150, 255))
        pts = []
        steps = 22
        for s in range(steps + 1):
            f = s / steps
            px = x + lean * f * f + sway * np.sin(f * 3.1)
            py = head_y + (foot_y - head_y) * f
            pts.append((px, py))
        dr.line(pts, fill=shade, width=thick, joint="curve")
        # seed head / flower cluster
        if rng.random() < 0.45:
            r = rng.uniform(1.6, 4.6)
            dr.ellipse([x - r, head_y - r, x + r, head_y + r], fill=shade)
        if rng.random() < 0.22:  # branch
            bx = x + lean * 0.55
            by = head_y + (foot_y - head_y) * 0.45
            ex = bx + rng.uniform(-0.05, 0.05) * w
            ey = by - rng.uniform(0.03, 0.10) * h
            dr.line([(bx, by), (ex, ey)], fill=int(shade * 0.9), width=1)
    lay = np.asarray(layer.filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255.0

    # stems only read where there is backlight; fade them out of the dark
    backlight = np.clip(light * 1.5, 0, 1)
    sil = np.maximum(sil, lay * (0.30 + 0.70 * backlight))

    # a soft dark floor so the base of the stems grounds
    floor = np.clip((yy - (horizon + 0.18)) / 0.22, 0, 1) ** 0.8
    sil = np.maximum(sil, floor * 0.75)

    # shallow depth of field: a blurred out-of-focus band in the foreground,
    # which is what stops a procedural field looking like a flat cut-out
    fg = fbm(h, w, octaves=6, seed=seed + 1313)
    fg_mask = np.clip((yy - (horizon + 0.16)) / 0.34, 0, 1) ** 1.1
    fg_blur = np.asarray(
        Image.fromarray((fg * 255).astype(np.uint8), "L").filter(
            ImageFilter.GaussianBlur(18)), np.float32) / 255.0
    sil = np.maximum(sil, fg_mask * np.clip((fg_blur - 0.34) * 2.0, 0, 1) * 0.85)

    lum = lum * (1.0 - np.clip(sil, 0, 1) * 0.90)

    # ---- palette
    night = np.array([6, 10, 16], np.float32)
    teal = np.array([34, 78, 92], np.float32)
    amber = np.array([196, 152, 96], np.float32)
    cream = np.array([250, 240, 216], np.float32)

    t = np.clip(lum * 1.55, 0, 1)[..., None]
    a = np.clip(t / 0.34, 0, 1)
    b = np.clip((t - 0.34) / 0.34, 0, 1)
    c = np.clip((t - 0.68) / 0.42, 0, 1)

    rgb = night * (1 - a) + teal * a
    rgb = rgb * (1 - b) + amber * b
    rgb = rgb * (1 - c) + cream * c

    rgb[..., 0] *= (1.0 + 0.14 * warm)
    rgb[..., 2] *= (1.0 - 0.20 * warm)

    # ---- 4. dust motes, grain, vignette
    motes = rng.random((h, w)).astype(np.float32)
    motes = np.asarray(Image.fromarray((motes * 255).astype(np.uint8), "L").filter(
        ImageFilter.GaussianBlur(0.6)), np.float32) / 255.0
    spike = np.clip((motes - 0.9975) / 0.0025, 0, 1)
    rgb += spike[..., None] * np.array([255, 246, 226], np.float32) * 1.15

    grain = (rng.random((h, w)).astype(np.float32) - 0.5) * 6.0
    rgb += grain[..., None]

    vy, vx = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = 1 - 0.70 * (((vx / w - 0.5) * 2) ** 2 + ((vy / h - 0.5) * 2) ** 2) ** 1.3
    rgb *= np.clip(vig, 0, 1)[..., None]

    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


JOBS = [
    # name,               w,    h,   seed, warm, horizon, glow, density
    ("hero.webp",        2400, 1350,  11, 0.62, 0.60, 1.00, 1.00),
    ("hero-sm.webp",     1200,  900,  11, 0.62, 0.60, 1.00, 0.62),
    ("page-work.webp",   2000,  900,  29, 0.34, 0.56, 1.45, 0.80),
    ("page-studio.webp", 2000,  900,  47, 0.72, 0.58, 1.35, 0.86),
    ("page-svc.webp",    2000,  900,  63, 0.22, 0.55, 1.30, 0.80),
    ("page-cinema.webp", 2000,  900,  81, 0.85, 0.60, 1.32, 0.72),
    ("og.webp",          1200,  630,  11, 0.62, 0.60, 1.00, 0.80),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, w, h, seed, warm, horizon, glow, density in JOBS:
        img = compose(h, w, seed, warm=warm, horizon=horizon, glow=glow, density=density)
        path = os.path.join(OUT, name)
        img.save(path, "WEBP", quality=80, method=6)
        print(f"  {name:18} {w}x{h}  {os.path.getsize(path)/1024:7.1f} KB")


if __name__ == "__main__":
    main()
