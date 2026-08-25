# -*- coding: utf-8 -*-
"""
Build the two logo variants the site needs from the supplied white-background PNG.

  mallard-logo.png        transparent background, brand colours  -> light surfaces
  mallard-logo-light.png  transparent background, forest recoloured to cream,
                          indigo lifted -> dark surfaces (nav over hero, footer)

The source is flat RGB on white, so a CSS filter cannot make it usable on a dark
ground: brightness(0) invert(1) whitens the whole rectangle, background included.
Alpha has to be extracted properly instead.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Mallard Logo.png")
OUT = os.path.join(ROOT, "site", "assets", "img")

CREAM = (244, 240, 231)
INDIGO_LIFT = (124, 118, 214)

im = Image.open(SRC).convert("RGB")

# --- white background -> alpha, un-premultiplying so edges stay clean ---
px = im.load()
w, h = im.size
rgba = Image.new("RGBA", (w, h))
out = rgba.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        a = 255 - min(r, g, b)          # distance from white
        if a <= 2:
            out[x, y] = (0, 0, 0, 0)
            continue
        f = a / 255.0
        # observed = C*f + 255*(1-f)  ->  C = (observed - 255*(1-f)) / f
        c = tuple(max(0, min(255, int(round((v - 255 * (1 - f)) / f)))) for v in (r, g, b))
        out[x, y] = c + (a,)

# --- trim to the mark ---
rgba = rgba.crop(rgba.getbbox())


def resized(img, width=240):
    return img.resize((width, int(round(width * img.height / img.width))), Image.LANCZOS)


light_surface = resized(rgba)
light_surface.save(os.path.join(OUT, "mallard-logo.png"), optimize=True)

# --- dark-surface variant: forest -> cream, indigo lifted, gold untouched ---
dark = rgba.copy()
dp = dark.load()
for y in range(dark.height):
    for x in range(dark.width):
        r, g, b, a = dp[x, y]
        if a == 0:
            continue
        mx = max(r, g, b)
        if b > r + 24 and b > g + 24:                       # indigo wing
            dp[x, y] = INDIGO_LIFT + (a,)
        elif g >= r and g >= b and mx < 170:                # forest green
            dp[x, y] = CREAM + (a,)
        elif mx < 90:                                        # near-black details
            dp[x, y] = CREAM + (a,)

resized(dark).save(os.path.join(OUT, "mallard-logo-light.png"), optimize=True)

# --- emblem only ---------------------------------------------------------
# In the nav the mark sits beside an HTML wordmark, so the lockup's own type
# would be both duplicated and illegible at 46px. Crop to the duck roundel at
# the first full-width transparent band beneath it.
def emblem(img):
    alpha = img.getchannel("A")
    w2, h2 = img.size
    for y in range(int(h2 * 0.35), h2):
        if alpha.crop((0, y, w2, y + 1)).getextrema()[1] <= 8:
            img = img.crop((0, 0, w2, y))
            break
    return img.crop(img.getbbox())


resized(emblem(rgba), 132).save(os.path.join(OUT, "mallard-mark.png"), optimize=True)
resized(emblem(dark), 132).save(os.path.join(OUT, "mallard-mark-light.png"), optimize=True)

for f in ("mallard-logo.png", "mallard-logo-light.png",
          "mallard-mark.png", "mallard-mark-light.png"):
    p = os.path.join(OUT, f)
    print("%-26s %7.1f KB  %s" % (f, os.path.getsize(p) / 1024, Image.open(p).size))
