# -*- coding: utf-8 -*-
"""
Build the Carolinas target-market map.

Real state outlines projected from lat/lon rather than a hand-drawn blob, so the
shape reads as an actual map. Emits an inline SVG snippet (animation is driven
by the page's scroll-reveal observer, so it has to be inline, not an <img>).

    python tools/gen_map.py        -> writes site/assets/img/map-carolinas.svg
                                      and prints the inline snippet path
"""
import math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "img")

GOLD = "#B78C34"
GOLD3 = "#DFC181"
CREAM = "#F4F0E7"
F600 = "#2C6E59"
F500 = "#3E8A70"

# ---------------------------------------------------------------- geography
# Simplified boundaries, ~40-60 points per state. Accurate enough that the
# Outer Banks, Cape Fear and the Savannah River all read correctly.
NC = [
    (36.59, -83.68), (36.59, -82.60), (36.56, -81.68), (36.55, -80.30),
    (36.55, -79.14), (36.55, -77.90), (36.55, -76.92), (36.55, -75.87),
    (36.30, -75.83), (36.03, -75.67), (35.90, -75.60), (35.72, -75.50),
    (35.55, -75.47), (35.25, -75.53), (35.19, -75.75), (35.10, -76.00),
    (34.98, -76.20), (34.72, -76.53), (34.65, -76.90), (34.55, -77.20),
    (34.40, -77.55), (34.20, -77.90), (33.92, -77.95), (33.84, -78.02),
    (33.86, -78.54), (34.10, -78.80), (34.30, -79.07), (34.50, -79.30),
    (34.62, -79.45), (34.75, -80.05), (34.82, -80.80), (35.00, -81.05),
    (35.10, -81.20), (35.16, -81.35), (35.19, -81.90), (35.20, -82.30),
    (35.09, -82.60), (35.06, -82.78), (35.00, -83.10), (34.99, -83.62),
    (34.99, -84.32), (35.23, -84.03), (35.40, -83.85), (35.56, -83.50),
    (35.72, -83.25), (35.78, -83.00), (35.95, -82.80), (36.06, -82.60),
    (36.15, -82.35), (36.35, -82.00), (36.47, -81.80), (36.59, -81.68),
    (36.59, -83.68),
]

SC = [
    (35.00, -83.35), (35.06, -82.78), (35.09, -82.60), (35.20, -82.30),
    (35.19, -81.90), (35.16, -81.35), (35.10, -81.20), (35.00, -81.05),
    (34.82, -80.80), (34.75, -80.05), (34.62, -79.45), (34.50, -79.30),
    (34.30, -79.07), (34.10, -78.80), (33.86, -78.54), (33.72, -78.80),
    (33.55, -79.02), (33.35, -79.15), (33.20, -79.20), (33.05, -79.35),
    (32.90, -79.55), (32.78, -79.85), (32.62, -80.10), (32.50, -80.35),
    (32.32, -80.55), (32.15, -80.78), (32.03, -80.88), (32.22, -81.13),
    (32.50, -81.15), (32.75, -81.30), (33.00, -81.50), (33.25, -81.75),
    (33.50, -82.00), (33.70, -82.25), (33.90, -82.40), (34.10, -82.60),
    (34.30, -82.70), (34.50, -82.90), (34.65, -83.00), (34.80, -83.20),
    (35.00, -83.35),
]

# Faint context so the two states do not float in a void.
GA = [(35.00, -83.62), (34.99, -84.32), (34.80, -85.30), (34.10, -85.42),
      (33.20, -85.30), (32.40, -85.05), (31.60, -85.10), (31.00, -85.10),
      (30.70, -84.90), (30.65, -83.00), (30.75, -82.20), (30.90, -81.50),
      (31.60, -81.20), (32.03, -80.88), (32.50, -81.15), (33.00, -81.50),
      (33.50, -82.00), (34.10, -82.60), (34.65, -83.00), (35.00, -83.35)]

TN = [(36.60, -83.68), (36.59, -81.68), (36.35, -82.00), (36.06, -82.60),
      (35.78, -83.00), (35.56, -83.50), (35.23, -84.03), (34.99, -84.32),
      (34.99, -88.20), (36.62, -88.20), (36.60, -83.68)]

VA = [(36.55, -75.87), (36.55, -79.14), (36.55, -80.30), (36.56, -81.68),
      (36.59, -83.68), (37.20, -82.70), (37.50, -80.50), (38.00, -78.50),
      (38.20, -77.00), (37.60, -76.30), (37.00, -76.00), (36.90, -75.98),
      (36.55, -75.87)]

CITIES = [
    ("Charlotte, NC", 35.227, -80.843, "end"),
    ("Greenville, SC", 34.851, -82.394, "end"),
    ("Columbia, SC", 34.001, -81.035, "start"),
]

# ---------------------------------------------------------------- projection
ALL = NC + SC
LAT0 = sum(p[0] for p in ALL) / len(ALL)
K = math.cos(math.radians(LAT0))

W, H, PAD = 720, 560, 46
xs = [p[1] * K for p in ALL]
ys = [-p[0] for p in ALL]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
scale = min((W - 2 * PAD) / (maxx - minx), (H - 2 * PAD) / (maxy - miny))
offx = (W - (maxx - minx) * scale) / 2
offy = (H - (maxy - miny) * scale) / 2


def proj(lat, lon):
    return ((lon * K - minx) * scale + offx, (-lat - miny) * scale + offy)


def path(pts, close=True):
    d = "".join(("M" if i == 0 else "L") + "%.1f %.1f" % proj(*p)
                for i, p in enumerate(pts))
    return d + ("Z" if close else "")


# ---------------------------------------------------------------- svg
s = []
s.append('<svg class="cmap" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
         'role="img" aria-labelledby="cmapTitle">' % (W, H))
s.append('<title id="cmapTitle">Target markets: Charlotte North Carolina, '
         'Greenville South Carolina and Columbia South Carolina</title>')
s.append('''<defs>
<linearGradient id="cmapFill" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="%s" stop-opacity=".55"/>
  <stop offset="1" stop-color="%s" stop-opacity=".22"/>
</linearGradient>
<linearGradient id="cmapEdge" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>
</linearGradient>
<filter id="cmapGlow" x="-70%%" y="-70%%" width="240%%" height="240%%">
  <feGaussianBlur stdDeviation="7" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>''' % (F500, F600, GOLD3, GOLD))

# graticule
s.append('<g class="cmap__grid">')
for i in range(1, 8):
    y = H * i / 8.0
    s.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f"/>' % (y, W, y))
for i in range(1, 10):
    x = W * i / 10.0
    s.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d"/>' % (x, x, H))
s.append('</g>')

# context states
s.append('<g class="cmap__ctx">')
for poly in (GA, TN, VA):
    s.append('<path d="%s"/>' % path(poly))
s.append('</g>')

# target states
s.append('<g class="cmap__states">')
for poly in (NC, SC):
    s.append('<path class="cmap__state" d="%s"/>' % path(poly))
s.append('</g>')

# pins
s.append('<g class="cmap__pins">')
for i, (name, lat, lon, anchor) in enumerate(CITIES):
    x, y = proj(lat, lon)
    dx = -16 if anchor == "end" else 16
    s.append('<g class="cmap__pin" style="--i:%d">' % i)
    s.append('  <ellipse class="cmap__shadow" cx="%.1f" cy="%.1f" rx="7" ry="2.5"/>' % (x, y + 1))
    s.append('  <circle class="cmap__pulse" cx="%.1f" cy="%.1f" r="6"/>' % (x, y))
    s.append('  <g class="cmap__drop">')
    s.append('    <path class="cmap__needle" d="M%.1f %.1f l-7.5 -13 a8.5 8.5 0 1 1 15 0 Z"/>' % (x, y))
    s.append('    <circle class="cmap__bead" cx="%.1f" cy="%.1f" r="3.2"/>' % (x, y - 17))
    s.append('  </g>')
    s.append('  <text class="cmap__label" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
             % (x + dx, y - 20, anchor, name))
    s.append('</g>')
s.append('</g>')
s.append('</svg>')

svg = "\n".join(s)
with open(os.path.join(OUT, "map-carolinas.svg"), "w", encoding="utf-8") as f:
    f.write(svg)

with open(os.path.join(ROOT, "tools", "_map_snippet.html"), "w", encoding="utf-8") as f:
    f.write(svg)

print("wrote map-carolinas.svg (%d bytes)" % len(svg))
for name, lat, lon, _ in CITIES:
    x, y = proj(lat, lon)
    print("  %-16s -> %6.1f, %6.1f" % (name, x, y))
