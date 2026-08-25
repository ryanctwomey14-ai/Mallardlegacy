# -*- coding: utf-8 -*-
"""Mallard Legacy Partners — brand artwork generator.

Emits every SVG in site/assets/img from the palette sampled off the logo.
Run from the repo root:  python tools/gen_art.py
"""
import os, random
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site"))

OUT = "assets/img"
FOREST_950="#071D17"; FOREST_900="#0B2B22"; FOREST_850="#0F372C"
FOREST_800="#164338"; FOREST_700="#1E5646"; FOREST_600="#2C6E59"
GOLD="#B78C34"; GOLD3="#DFC181"; TAUPE="#ABA098"; CREAM="#F4F0E7"

def elevation(seed, name, blocks, lit=0.30, trees=True):
    r = random.Random(seed)
    W,H = 800,600
    s=[]
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-hidden="true" preserveAspectRatio="xMidYMid slice">')
    s.append(f'''<defs>
  <linearGradient id="sky{seed}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{FOREST_800}"/><stop offset=".55" stop-color="{FOREST_900}"/><stop offset="1" stop-color="{FOREST_950}"/>
  </linearGradient>
  <linearGradient id="glow{seed}" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="face{seed}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{FOREST_700}"/><stop offset="1" stop-color="{FOREST_850}"/>
  </linearGradient>
</defs>''')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#sky{seed})"/>')
    # sun disc
    s.append(f'<circle cx="{r.randint(120,660)}" cy="{r.randint(90,170)}" r="{r.randint(34,52)}" fill="{GOLD}" opacity=".14"/>')
    s.append(f'<rect y="{H*0.45:.0f}" width="{W}" height="{H*0.55:.0f}" fill="url(#glow{seed})"/>')

    ground = 470
    for (x,w,top,cols,rows) in blocks:
        s.append(f'<rect x="{x}" y="{top}" width="{w}" height="{ground-top}" fill="url(#face{seed})"/>')
        # cornice
        s.append(f'<rect x="{x-4}" y="{top-6}" width="{w+8}" height="6" fill="{FOREST_600}" opacity=".85"/>')
        # window grid
        pad=16; gx=(w-pad*2)/cols; gy=(ground-top-pad*2)/rows
        ww=gx*0.56; wh=gy*0.52
        for cx in range(cols):
            for cy in range(rows):
                px = x+pad+gx*cx+(gx-ww)/2
                py = top+pad+gy*cy+(gy-wh)/2
                on = r.random()<lit
                fill = GOLD3 if on else CREAM
                op = f'{r.uniform(.55,.9):.2f}' if on else f'{r.uniform(.07,.14):.2f}'
                s.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{ww:.1f}" height="{wh:.1f}" fill="{fill}" opacity="{op}"/>')
        # balcony rails
        for cy in range(1,rows,2):
            by = top+pad+gy*cy-3
            s.append(f'<rect x="{x+8}" y="{by:.1f}" width="{w-16}" height="1.2" fill="{CREAM}" opacity=".16"/>')
    # ground plane
    s.append(f'<rect y="{ground}" width="{W}" height="{H-ground}" fill="{FOREST_950}"/>')
    s.append(f'<rect y="{ground}" width="{W}" height="1.2" fill="{GOLD}" opacity=".35"/>')
    if trees:
        for i in range(r.randint(5,8)):
            tx=r.randint(20,780); th=r.randint(48,96); tw=th*0.42
            s.append(f'<path d="M{tx} {ground} L{tx-tw/2:.0f} {ground-th*0.55:.0f} L{tx-tw*0.3:.0f} {ground-th*0.55:.0f} L{tx:.0f} {ground-th} L{tx+tw*0.3:.0f} {ground-th*0.55:.0f} L{tx+tw/2:.0f} {ground-th*0.55:.0f} Z" fill="{FOREST_950}" opacity=".9"/>')
    # water ripples in foreground
    for i,(y,o) in enumerate([(505,.30),(528,.20),(552,.13),(578,.08)]):
        s.append(f'<path d="M-20 {y} C 140 {y-9}, 300 {y+9}, 460 {y} S 700 {y-8}, 830 {y}" fill="none" stroke="{GOLD}" stroke-width="1" opacity="{o}"/>')
    s.append('</svg>')
    open(os.path.join(OUT,name),"w",encoding="utf-8").write("\n".join(s))

elevation(11,"prop-oakbend.svg",[(70,190,235,4,7),(275,255,180,5,9),(555,190,255,4,6)],lit=.32)
elevation(23,"prop-cypress.svg",[(50,215,205,5,8),(290,180,270,4,5),(495,265,190,6,9)],lit=.26)
elevation(37,"prop-hollow.svg",[(90,300,215,7,8),(410,150,265,3,6),(580,180,240,4,7)],lit=.36)
elevation(52,"prop-birchpoint.svg",[(40,175,250,4,6),(240,290,185,6,9),(555,200,225,4,7)],lit=.29)
elevation(64,"prop-mallardrun.svg",[(60,250,195,6,9),(335,165,260,3,6),(525,235,215,5,8)],lit=.34)
elevation(78,"prop-stillwater.svg",[(80,200,230,4,7),(305,225,200,5,8),(560,180,245,4,6)],lit=.24)
elevation(91,"prop-sawgrass.svg",[(55,240,200,6,9),(320,195,245,4,7),(540,215,220,5,8)],lit=.31)
print("built", os.listdir(OUT))

F950="#071D17"; F900="#0B2B22"; F850="#0F372C"; F800="#164338"; F700="#1E5646"; F600="#2C6E59"
GOLD="#B78C34"; GOLD3="#DFC181"; CREAM="#F4F0E7"; INDIGO="#353087"

# ---------- HERO: wetland horizon at dawn, distant multifamily skyline ----------
r=random.Random(7)
W,H=1600,1000
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">']
s.append(f'''<defs>
<linearGradient id="hsky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#0A2A21"/><stop offset=".38" stop-color="{F800}"/>
 <stop offset=".62" stop-color="#215C4A"/><stop offset="1" stop-color="{F950}"/></linearGradient>
<radialGradient id="hsun" cx=".72" cy=".30" r=".42">
 <stop offset="0" stop-color="{GOLD3}" stop-opacity=".38"/>
 <stop offset=".45" stop-color="{GOLD}" stop-opacity=".12"/>
 <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<linearGradient id="hwater" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#123A2F"/><stop offset="1" stop-color="{F950}"/></linearGradient>
<linearGradient id="hshaft" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="{GOLD}" stop-opacity=".26"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
</defs>''')
s.append(f'<rect width="{W}" height="{H}" fill="url(#hsky)"/>')
s.append(f'<rect width="{W}" height="{H}" fill="url(#hsun)"/>')
s.append(f'<circle cx="{W*.72:.0f}" cy="{H*.30:.0f}" r="76" fill="{GOLD3}" opacity=".16"/>')
s.append(f'<circle cx="{W*.72:.0f}" cy="{H*.30:.0f}" r="150" fill="none" stroke="{GOLD3}" stroke-width="1" opacity=".10"/>')
s.append(f'<circle cx="{W*.72:.0f}" cy="{H*.30:.0f}" r="240" fill="none" stroke="{GOLD3}" stroke-width="1" opacity=".06"/>')

# far skyline (soft, low contrast)
horizon=610
x=-40
while x<W+60:
    w=r.randint(46,120); h=r.randint(60,215); top=horizon-h
    s.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{F850}" opacity=".72"/>')
    cols=max(2,w//24); rows=max(3,h//26)
    pad=7; gx=(w-pad*2)/cols; gy=(h-pad*2)/rows
    for cx in range(cols):
        for cy in range(rows):
            if r.random()<0.30:
                px=x+pad+gx*cx+gx*0.2; py=top+pad+gy*cy+gy*0.2
                s.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{gx*0.55:.1f}" height="{gy*0.45:.1f}" fill="{GOLD3}" opacity="{r.uniform(.2,.6):.2f}"/>')
    x+=w+r.randint(6,26)

# nearer band of apartment blocks, darker
x=-60
while x<W+80:
    w=r.randint(90,210); h=r.randint(120,300); top=horizon-h+34
    s.append(f'<rect x="{x}" y="{top}" width="{w}" height="{horizon+34-top}" fill="{F950}" opacity=".82"/>')
    cols=max(3,w//34); rows=max(4,h//34)
    pad=12; gx=(w-pad*2)/cols; gy=(h-pad*2)/rows
    for cx in range(cols):
        for cy in range(rows):
            if r.random()<0.26:
                px=x+pad+gx*cx+gx*0.18; py=top+pad+gy*cy+gy*0.2
                s.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{gx*0.6:.1f}" height="{gy*0.4:.1f}" fill="{GOLD3}" opacity="{r.uniform(.3,.85):.2f}"/>')
    x+=w+r.randint(14,52)

# reed silhouettes
for i in range(46):
    rx=r.randint(-20,W+20); rh=r.randint(40,150)
    bend=r.randint(-24,24)
    s.append(f'<path d="M{rx} {horizon+40} Q {rx+bend//2} {horizon+40-rh//2}, {rx+bend} {horizon+40-rh}" fill="none" stroke="{F950}" stroke-width="{r.uniform(1.2,2.6):.1f}" opacity=".85"/>')

# water
s.append(f'<rect y="{horizon+34}" width="{W}" height="{H-horizon-34}" fill="url(#hwater)"/>')
s.append(f'<rect x="{W*.66:.0f}" y="{horizon+34}" width="150" height="{H-horizon-34}" fill="url(#hshaft)"/>')
# concentric ripple rings centred where a duck would sit
cx0,cy0=W*0.30,H*0.86
for i in range(1,9):
    rr=i*88
    s.append(f'<ellipse cx="{cx0:.0f}" cy="{cy0:.0f}" rx="{rr}" ry="{rr*0.20:.0f}" fill="none" stroke="{GOLD}" stroke-width="1" opacity="{max(0.02,0.26-i*0.03):.2f}"/>')
# horizontal water strokes
for i in range(22):
    y=horizon+50+i*17
    s.append(f'<path d="M-30 {y} C {W*0.25:.0f} {y-6}, {W*0.5:.0f} {y+6}, {W*0.75:.0f} {y} S {W+30} {y-5}, {W+40} {y}" fill="none" stroke="{CREAM}" stroke-width="1" opacity="{max(0.015,0.09-i*0.004):.3f}"/>')
s.append('</svg>')
open(f"{OUT}/hero-wetland.svg","w",encoding="utf-8").write("\n".join(s))

# ---------- RINGS: reusable ripple field for dark CTA / page headers ----------
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">']
for i in range(1,16):
    rr=i*68
    s.append(f'<ellipse cx="800" cy="360" rx="{rr}" ry="{rr*0.42:.0f}" fill="none" stroke="{GOLD}" stroke-width="1" opacity="{max(0.02,0.30-i*0.019):.3f}"/>')
s.append('</svg>')
open(f"{OUT}/rings.svg","w",encoding="utf-8").write("\n".join(s))

# ---------- MAP: southeast footprint ----------
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 520" aria-hidden="true">']
s.append(f'<rect width="640" height="520" fill="none"/>')
# stylised sunbelt landmass
s.append(f'<path d="M70 150 L180 108 L300 92 L400 104 L470 132 L520 176 L470 232 L430 296 L372 344 L300 372 L232 344 L176 296 L124 240 Z" fill="{F800}" opacity=".28" stroke="{F600}" stroke-width="1.2"/>')
mkts=[("Charlotte, NC",352,150),("Greenville, SC",236,214),("Columbia, SC",344,268)]
for n,x,y in mkts:
    s.append(f'<circle cx="{x}" cy="{y}" r="20" fill="{GOLD}" opacity=".10"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{GOLD3}"/>')
    s.append(f'<text x="{x+13}" y="{y+4}" font-family="Figtree,sans-serif" font-size="11.5" font-weight="600" letter-spacing=".06em" fill="{CREAM}" opacity=".82">{n}</text>')
s.append('</svg>')
open(f"{OUT}/map-southeast.svg","w",encoding="utf-8").write("\n".join(s))

print(sorted(os.listdir(OUT)))
