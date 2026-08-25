# Mallard Legacy Partners — website

Static site. No build step, no dependencies, no framework. Open `site/index.html` or serve
the `site/` directory and it works.

The reasoning behind every structural decision is in [`STRATEGY.md`](STRATEGY.md).

---

## Run it locally

```bash
python -m http.server 4488 --directory site
```

Then open <http://localhost:4488>.

---

## Structure

```
site/
├── index.html            Homepage — hand-authored, commented section by section
├── strategy.html         Thesis, 7-point buy box, underwriting, risk table
├── about.html            Seth, operating commitments, the name
├── faq.html              24 questions in 5 groups
├── contact.html          Primary conversion page
├── thank-you.html        Post-conversion (noindex)
├── disclosures.html      Securities, risk, performance
├── privacy.html          Privacy + terms
├── robots.txt
├── sitemap.xml
└── assets/
    ├── css/main.css      Whole design system, ~700 lines, token-driven
    ├── js/main.js        ~200 lines, vanilla, no dependencies
    └── img/              Logo, headshot, generated SVG artwork

tools/
├── build_pages.py        Regenerates every page except index.html
├── gen_logo.py           Builds transparent logo + emblem variants from the source PNG
├── gen_map.py            Builds the Carolinas market map (inline SVG snippet)
├── gen_art.py            Regenerates the SVG artwork from the brand palette
└── bundle_artifact.py    Bundles all 11 pages into one shareable file
```

### Editing navigation or the footer

They live in `tools/build_pages.py`. Change them there, then:

```bash
python tools/build_pages.py
```

`index.html` is hand-authored and is **not** regenerated — apply header/footer changes to it
manually. This is deliberate: the homepage carries per-section commentary that a generator
would flatten.

---

## Before launch — required

### 1. Confirm the securities exemption ⚠️

The site is built for **Reg D 506(c)**: it advertises the offering publicly and states that
third-party accreditation verification is required.

**If Mallard is running 506(b) instead**, general solicitation is prohibited. You must gate
`offering.html` behind registration and remove the offering terms from public view. Have securities
counsel sign off before the domain resolves.

### 2. Remaining unknowns from the intake form

The fabricated track record has been removed entirely. What is still open:

| Item | Status |
|---|---|
| Preferred return | **Blank on intake.** Offering page currently shows 7% — my draft, not Seth's decision. Needs his number or removal. |
| Equity split | **Blank on intake** (form showed the "Ex. 70/30" prompt). Same caveat. |
| Fees | Acquisition 1.5% / asset mgmt 2% / disposition 1% are conventional drafts, not supplied. |
| Target close date | Not set. |
| Calendar link | Not set up — contact form is the only booking path today. |
| Formation / counsel | Blank. |
| Headshot | Intake referenced a new file that wasn't attached; current image is the original supplied headshot. |

Confirmed and applied: entity `Mallard Legacy Partners LLC`, Reg D **506(c)**, minimum
**$100,000**, hold **5–7 years**, target markets **Greenville SC, Columbia SC, Charlotte NC**,
phone **(828) 713-3597**, domain **mallardlegacypartners.com**, Seth's real biography.

⚠️ **Target IRR (15–17%) and equity multiple (1.8–2.2x) are forward-looking targets for a
sponsor with no completed deals.** They are labelled as underwriting targets on the page, but
the hero-card disclaimer was removed at the client's request. Confirm with counsel that the
remaining footer disclosures are sufficient for 506(c).

### 3. Wire up the forms

`assets/js/main.js` §7 simulates submission with a `setTimeout`. Replace it with a real
endpoint — Juniper Square, HubSpot, Formspark, or a serverless function:

```js
const res = await fetch('https://your-endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(Object.fromEntries(new FormData(form)))
});
```

On success, either show the inline status (current behaviour) or redirect to `thank-you.html`
so the conversion is trackable as a pageview.

### 4. Connect the investor portal

`offering.html` and the header "Investor login" both point at a placeholder. Repoint them at your
investor management platform once it is live.

### 5. Set the real domain

`https://www.mallardlegacy.com` is hard-coded in canonical tags, Open Graph URLs, JSON-LD and
`sitemap.xml`. Update `SITE` in `tools/build_pages.py`, rerun it, and fix `index.html` by hand.

### 6. Add an OG image

`index.html` references `assets/img/og-home.jpg`, which does not exist yet. 1200×630.

---

## Ask Mallard — investor assistant

`site/assets/js/agent.js`. A duck in the bottom right that expands into a chat panel,
loaded on every page.

**It is not wired to an LLM, deliberately.** This site advertises a Reg D 506(c) offering,
so anything the widget says is a representation to a prospective investor. A free-form model
can invent a return figure, imply a guarantee, or give tax advice in Seth's voice — none of
which Mallard can stand behind, least of all with no completed deals. Answers therefore come
from a fixed knowledge base written from the site's own FAQ, strategy and terms.

Every reply is two bubbles: the answer, then a separate soft nudge with a "Book the call"
link. Splitting them matters — a sales line welded onto the end of a sentence reads as pushy.
The closing lines are varied per topic so it does not repeat itself.

Anything it cannot match confidently hands off to Seth rather than guessing. Intent matching
is keyword scoring with a confidence floor, tested at 41 phrasings (currently 100%). Keywords
are normalised the same way queries are, because a keyword containing punctuation (`k-1`)
could otherwise never match a query that has had punctuation stripped.

**To connect a real model later:** set `window.MALLARD_AGENT_ENDPOINT` to a URL taking
`{ message, history }` and returning `{ reply }`. The API key must live on the server — never
in this file. The knowledge base becomes the system prompt or retrieval context, and the same
guardrails have to be enforced server-side: no invented figures, no guarantees, no tax or
investment advice, always disclose the absent track record.

Note for the bundler: the widget builds its own DOM in JS, so `tools/bundle_artifact.py`
patches its image reference and `CALL_URL` separately — the HTML rewriting never sees them.

## Return illustration calculator

Strategy page, sitting directly after "How the return is generated". Applies the published
multiples (1.8x / 2.2x) to an amount the visitor sets, and draws the band between them across
the seven-year outer hold.

Each target card breaks the return into **cash distributions over the hold** and **equity
realised at sale**, because those are two different things with different risk and different
timing, and a single blended figure hides that.

The split uses assumed distributions of 5% (lower) and 7% (upper) of invested capital per
year across the hold, with the remainder of the multiple realised at sale. `CASH_LOW` and
`CASH_HIGH` in the JS hold those rates, and the footnote states them. **They are assumptions,
not the deal's preferred return** — which is still unset. Replace both when Seth sets terms.

Behaviour lives in `assets/js/main.js` section 7b. Three details are deliberate:

- **It draws a range, never one line.** A single curve reads as a forecast. There is no track
  record behind these numbers, so the output has to look like a band.
- **Input is not clamped while typing.** Forcing the value to the $100,000 minimum on every
  keystroke makes the field impossible to edit. It clamps on blur instead.
- **It never extrapolates.** Only the two multiples stated elsewhere on the site are used. If
  those change, update `LOW` and `HIGH` in the JS and the two `calc__cardHead` labels in
  `tools/build_pages.py` together.

The chart is hand-built SVG — no charting library. Axis labels rescale with the amount, the
dashed baseline marks the sum invested, and the vertical dotted line marks the earliest exit
at year five.

⚠️ Under 506(c) this is the highest-exposure element on the site: dollar figures attached to a
sponsor with no completed deals. The disclaimer directly beneath does the work — it states
plainly that this is an illustration rather than a projection, that no prior performance sits
behind the numbers, and that total loss is possible. **Do not remove or soften it, and have
counsel review this section specifically.**

## Asset cache busting

`main.css` and `main.js` are referenced with a short content hash (`main.css?v=4a04b4c4`),
regenerated by `tools/build_pages.py` on every build — including in the hand-authored
`index.html`, which the build stamps in place.

This exists because stale CSS broke review repeatedly during the build: a cached stylesheet
renders whole sections as unstyled markup or drops a background out of position, and it looks
exactly like a code bug. If you edit CSS or JS by hand, **re-run `python tools/build_pages.py`**
so the hashes update.

## Strategy page header image

`site/assets/img/strategy-bg.jpg` is graded from `Strategy Background.png` in the project
root (rain rings on a pond — the site's ripple motif as a photograph). Regenerate with the
snippet in `tools/` or re-run the grading inline: desaturate to 0.62, brightness 1.45,
contrast 1.05, then blend 20% toward forest `#164338`.

Same trap as the videos, in the opposite direction. A first pass graded it to median
luminance 0.043 and the scrim then buried it — text measured a comfortable 13:1 while the
photograph was invisible. **Judging it by mean brightness was the wrong test**: ripples read
through local texture, not overall lightness. Measured on texture instead (standard
deviation of the composited open area), the usable grade was three stops lighter.

Current state: cream heading 8.2:1, gold eyebrow 5.4:1, open-side texture sd 17.5.

## Video backgrounds

Two graded, looping, silent MP4s in `site/assets/video/`, rebuilt from the originals in the
project root:

```bash
sh tools/encode_video.sh
```

| File | Section | Source |
|---|---|---|
| `mallard-hero.mp4` | Hero | `Mallard Hero.mp4` |
| `investment-case.mp4` | "Four returns from one apartment building" | `Investment Case Video.mp4` |

Each is scaled to 1600x900, stripped of audio, and given a 2-second crossfade so the loop has
no visible cut. **The two use different grades on purpose** — the aerial source is much darker
(asphalt, roofs, tree line) and needs a lift the hero source does not.

**Grading and scrim are tuned together, by measurement.** Get it wrong in either direction and
the section breaks:

- Too light and cream text fails contrast. Ungraded, the hero footage sits at luminance 0.24
  under the headline where 0.155 is the AA limit.
- Too dark and the video is invisible. An earlier pass crushed the aerial to median luminance
  0.014 and put an 0.88 scrim over it; the composite differed from the flat background by 3
  greys out of 255. It was playing perfectly and looked like a solid colour.

Current measured state: text bands **9.8:1** (hero) and **6.7:1** (investment case) against
cream, with the footage reading clearly in the open areas of both. The scrims are directional —
heavy across the text, light across the rest — rather than uniform. If you re-grade, re-measure
both numbers, not just contrast.

MP4 only; a VP9 encode came out larger than the H.264 and bought nothing.

Loading is gated in `assets/js/main.js`: sources attach only above 900px and only when
`prefers-reduced-motion` is unset, so phones never download them. A poster sits underneath, so
no-JS, blocked autoplay, a 404 or an unsupported codec all fall back to a still.

⚠️ The investment-case footage shows an apartment community **Mallard does not own**. The
caption stating this was removed at the client's request, so nothing on the page now
distinguishes the footage from a Mallard asset. Raise this with securities counsel before
launch, and do not reuse the footage anywhere that implies ownership.

## Photography

The site ships with brand-duotone architectural SVGs rather than stock photography — coherent
today, and designed so real photos drop in without a redesign. Priority order:

1. **Hero** (`assets/img/hero-wetland.svg`) — replace with a wide dusk exterior of a real
   community. Keep the dark overlay; the headline needs it.
2. **Property tiles** (`prop-*.svg`) — one 4:3 exterior per community.
3. **Case study** — before/after interior pair.

Swap the `src` and keep the `width`/`height` attributes so layout shift stays at zero.

---

## Shareable review build

To produce a single self-contained HTML file containing all eleven pages
(inlined CSS, JS and images, with the navigation driven by a hash router):

```bash
python tools/bundle_artifact.py mallard-review.html
```

Useful for sending to a client for review without deploying. It is a preview
only — `site/` remains the deployable build.

## Regenerating the artwork

```bash
python tools/gen_art.py
```

Rewrites the SVG elevations, the hero, the ripple field and the market map from the brand
palette. Only needed if you change colours or want different building compositions.

---

## Accessibility

Verified in-browser across all eleven pages:

- Every text/background pair meets WCAG AA (4.5:1 body, 3:1 large). The `--text-faint` and
  small-gold tokens are darkened specifically to clear it — don't lighten them back.
- Single `h1` per page, sequential headings, skip link, visible focus rings.
- All interactive targets ≥44px.
- Accordions and the drawer are real buttons with `aria-expanded`; Escape closes the drawer.
- Forms use real labels, `aria-live` status, blur-time validation, focus moved to the first
  invalid field.
- `prefers-reduced-motion` drops every transform.
- No horizontal scroll at any width; the comparison table scrolls inside its own container.
- With JavaScript disabled the page renders complete — entrance states are scoped behind `.js`.

---

## Browser support

Modern evergreen browsers. Uses `overflow: clip` (with an `overflow: hidden` fallback),
CSS custom properties, `grid-template-rows` transitions, `aspect-ratio` and
`IntersectionObserver`. No polyfills required for anything from 2023 onward.
