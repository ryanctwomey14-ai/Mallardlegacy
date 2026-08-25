# Mallard Legacy Partners — Web Strategy & Conversion Architecture

**Revision 2** — rebuilt against the client intake form.
Shareable version: <https://claude.ai/code/artifact/3a750be8-a97a-4f3f-9cba-7e28902dd979>

Revision 1 was written before the intake arrived and assumed an established sponsor with a
track record. That was wrong in the most important way possible, and everything below replaces it.

---

## 1. Ground truth

Everything here comes from the intake form. Anything not on this list does not appear on the
site as a claim.

| | |
|---|---|
| **Entity** | Mallard Legacy Partners LLC |
| **Exemption** | Reg D **506(c)** — public advertising permitted, third-party accreditation verification required |
| **Track record** | **None.** No AUM, no units, no exits, no distributions ever paid |
| **Current deal** | **None under contract.** Actively sourcing; seeking an experienced partner for deal one |
| **Target markets** | Greenville SC, Columbia SC, Charlotte NC |
| **Minimum** | $100,000 |
| **Hold period** | 5–7 years |
| **Principal** | Seth Phillips, Founder & Managing Partner. Sole team member |
| **Background** | Construction from age 12; industrial mechanic (4 yrs); anesthesia service engineer (2 yrs); ~10 yrs around real estate, last 2 in multifamily; engineering coursework at AB Tech & Haywood CC |
| **Domain** | mallardlegacypartners.com |
| **Phone** | (828) 713-3597 |
| **CRM** | Peak Operator (GoHighLevel) |
| **Calendar** | Not set up — contact form is the only booking path |
| **Blank on intake** | Preferred return, equity split, fees, formation date, counsel, target close |

> ⚠️ **The governing constraint.** Under 506(c) this site is *general solicitation*. Every number
> on it is a representation to prospective investors. A placeholder that would be harmless on a
> restaurant site is a misstatement of material fact here.
>
> The first build carried invented performance figures as scaffolding. All of it has been removed.
> The rule going forward: **if it did not come from the intake form or from Seth, it does not go
> on the page as fact.**

---

## 2. The real problem

This is not a conversion problem. It is a credibility problem.

A sponsor with eleven deals sells *returns*. A sponsor with zero deals sells *himself*, and the
buyer knows it.

| Dimension | Established sponsor | Mallard today |
|---|---|---|
| Primary conversion | Subscribe to the open deal | **Join the investor list.** There is nothing to subscribe to |
| Proof carried by | Realised IRR, exits, references | Named constraints, personal capital, the operator's history |
| Best-fit investor | Cold high earner from search | Someone who already knows Seth, or one degree away |
| Success in 90 days | Capital committed | A list of qualified people who take the call when deal one lands |
| Biggest risk | Losing to a better-priced deal | Reading as a beginner *hiding* it, rather than a beginner *naming* it |

Every sponsor with a track record started without one. The ones who raised successfully did it by
being conspicuously honest about the gap, not by papering over it. That is the whole strategy.

---

## 3. Ideal customer — in the order they will actually say yes

The classic ICP (over-taxed physician, $3M in equities) is the right *long-term* target and the
wrong *first* target: that investor screens on track record and screens Mallard out.

1. **The proximate network.** People who know Seth personally or one degree away — contractors,
   engineers, plant managers, local business owners across western NC and upstate SC. They
   underwrite the *person*, the only thing available to underwrite. Almost all of deal one's
   equity comes from here.
2. **The experienced operating partner.** Not an investor — a co-GP or mentor sponsor for deal
   one. The intake names this explicitly as what Seth is working on. **The site must convert this
   audience too.**
3. **The access-over-pedigree investor.** Accredited but shut out of institutional minimums, and
   comfortable trading first-timer risk for a real relationship and early access. Reachable
   through local networks and podcasts, not Google.
4. **The classic high earner.** Genuinely the long-term ICP — but realistically deal two or three,
   once there is something to point at.

> **Structural tension worth raising with Seth.** A **$100,000 minimum plus no track record is the
> hardest combination in private real estate.** The people most willing to back a first-time
> sponsor are the ones closest to him, and they typically write $25K–$50K. A $50K minimum would
> roughly double the reachable pool for deal one, at the cost of more K-1s. Built at $100K as
> instructed — this is a recommendation to revisit, not a change made.

---

## 4. Objections — one dominates everything

| Objection | Retired by | Where |
|---|---|---|
| **"You've never done this."** | Stated by us before the visitor can raise it — in the metrics slot, the bio, and as its own FAQ answered "We do not have one" | Home ×3 · About · FAQ |
| "So why would I go first?" | Named constraints instead of results: 3 markets, 150–350 units, 75% max leverage, 12 months reserves | Home — Commitments |
| "Are you learning on my money?" | Explicit commitment not to do deal one alone | About — Commitments |
| "What do you actually know?" | Engineering and mechanical history, framed as buildings-as-systems rather than finance pedigree | Home · About |
| "I can't lock up $100K for 7 years" | Stated bluntly; visitor told to invest less or wait | Home · FAQ |
| "How do you get paid?" | Structure explained before any document request ⚠️ *terms still unset* | Offering |
| "What if something happens to Seth?" | Answered directly, including that a one-person firm makes this sharper | FAQ |
| "Can I check you out?" | A four-part diligence checklist aimed at ourselves | Home — Diligence |

---

## 5. Site map

```
/                  Full argument, honesty-first
├── /strategy      Buy box, underwriting, risk table — the substitute for a track record
├── /portfolio     "Nothing here yet." What we hunt, and what will appear
├── /offering      How an offering is structured (renamed from /fund — no fund, no blind pool)
├── /about         Seth's real history + four operating commitments
├── /insights      Due diligence checklist + education
├── /faq           23 questions in five groups
├── /contact       Primary conversion
├── /thank-you     Expectation setting (noindex)
├── /disclosures   Securities, risk, forward-looking, performance
└── /privacy       Privacy + terms
```

**Recommended next:** once Seth confirms, `/offering` should become an **investor-list
registration page** rather than a terms page. With no deal, "join the list" is the only honest
primary action — and the one that matters most right now.

---

## 6. Homepage, section by section

Two slots differ from a normal sponsor site, and they are the two that matter: **Commitments**
replaces the track record, **Diligence** replaces the testimonials.

| # | Section | Job | Why it converts |
|---|---|---|---|
| 01 | Hero | Name the three return mechanics | "Rent pays you. Depreciation shelters you. Tenants retire the loan." Says how money is made before asking for anything. Stat card labelled *What we underwrite to* — targets, not results |
| 02 | Credibility strip | Answer "is this real?" | Cut from seven items to five. Audited financials and sponsor co-investment removed — both implied an operating history that doesn't exist |
| 03 | Problem | Resonance before persuasion | Tax, concentration, time, access |
| 04 | Pain → Gain | Reframe agreement into a product | Forest panel draws the eye first, so the promise reads before the pain |
| 05 | Benefits | Four outcomes a brokerage account can't deliver | Written as things the investor experiences, not things we provide |
| 06 | **Commitments** *(rewritten)* | Occupy the proof slot honestly | "We haven't bought a building yet. Here is what we won't compromise on." 3 markets / 150–350 units / 75% leverage / 12 months reserves. Naming the gap in the exact slot where proof belongs converts better than evasive silence |
| 07 | Strategy | Answer "why should this work?" | Falsifiable buy box; animated Carolinas map pins the three real markets |
| 08 | Process | Reduce perceived effort | Four steps from "book a call" to "invested" |
| 09 | Comparison | Win the choice actually being made | Four-way vs REITs, own rentals, index funds. **Loses the liquidity row on purpose** |
| 10 | **Authority** *(rewritten)* | Sell the operator | "New firm. Not a new operator." Closes by stating the first acquisition hasn't happened — in the same place a chart would go |
| 11 | **Diligence** *(replaced testimonials)* | Hand the skeptic the weapon | No investors means no quotes. Four things to check on us, including "there are no existing investors for you to call" |
| 12 | FAQ | Retire the last objections | Opens "Have you done this before?", closes "What is the honest downside?" |
| 13 | Two paths | Capture the not-yet-ready | Call, or the checklist. Most visitors are early right now |
| 14 | Final CTA | Close | Three reassurances under the button |

---

## 7. Trust architecture — rebuilt from scratch

The top three signals in revision 1 (published failures, verifiable history, realised returns)
do not exist. What replaces them is weaker individually — but disclosure does work no established
sponsor can copy, because they have results to hide behind.

| Weight | Element | Placement |
|---|---|---|
| ●●●●● | Naming the absence of a track record, unprompted, in the proof slot | Home · About · FAQ |
| ●●●●● | Seth's own capital in every deal, identical terms | Home · About · Offering |
| ●●●●● | Commitment not to do deal one alone | About |
| ●●●●○ | A narrow, falsifiable buy box published in full | Home · Strategy |
| ●●●●○ | The diligence checklist aimed at ourselves | Home · Insights |
| ●●●●○ | An honest comparison table we lose a row in | Home |
| ●●●○○ | "Bad news travels first" as a stated policy | About |
| ●●●○○ | Reserves, leverage cap, debt-term discipline, stated numerically | Home · Strategy |
| ●●○○○ | Third-party management and accreditation verification | Strip · FAQ |
| ●●○○○ | Plain-English disclosures | Footer |

**What would move the needle most:** naming the experienced partner for deal one, publicly. That
would outrank everything except Seth's own capital — clearly attributed to them, never implied as
Mallard's.

---

## 8. CTA architecture

**Primary:** Schedule an intro call. **Secondary:** Download the due diligence checklist.
Nothing else is styled as a button.

| Location | CTA | Destination |
|---|---|---|
| Header, every page | Schedule a call | `/contact` |
| Hero, primary | Schedule an intro call | `/contact` |
| Hero, secondary | See how we invest *(was "See the track record")* | `/strategy` |
| After Pain → Gain | Read the full investment thesis | `/strategy` |
| After Commitments | See the full buy box | `/strategy` |
| After Strategy | See how we underwrite a deal | `/strategy` |
| After Process | Start with step one | `/contact` |
| After Diligence | Take the full 31-question checklist | `/insights` |
| Two-paths form | Send me the checklist | Form |
| Final CTA | Schedule an intro call | `/contact` |

**Form design:** five questions (a longer form lowers volume and raises quality — correct at a
$100K minimum); capital ranges start at $100,000; validation on **blur**, never keystroke;
accreditation required with "Not sure — please explain it to me" selectable.

> ⚠️ Forms currently simulate submission client-side. They need to POST into **Peak Operator
> (GoHighLevel)**. There is no calendar link yet, so "Schedule a call" is a form plus a manual
> reply — set that up before sending traffic.

---

## 9. SEO

Canonicals, Open Graph, JSON-LD and the sitemap all point at **mallardlegacypartners.com**, with
`areaServed` set to the Carolinas and FAQ schema rewritten so no structured-data claim
contradicts the page.

| Page | Primary target |
|---|---|
| Home | multifamily real estate investing |
| Strategy | multifamily investment criteria |
| Portfolio | *no commercial intent until there are assets* |
| Offering | multifamily investment opportunity Carolinas |
| Insights | real estate sponsor due diligence checklist |
| FAQ | multifamily syndication FAQ |
| About | multifamily sponsor Asheville |

**Content roadmap, in publishing order:**

1. Cost segregation for passive investors: what it does to a $100K investment
2. Accredited investor definition, in plain language *(highest-volume entry term)*
3. How to read a waterfall: preferred return, catch-up, promote, hurdle
4. Self-directed IRA real estate: the UBTI question nobody answers
5. **How to vet a first-time sponsor** *(owns the exact objection; almost nobody writes it)*
6. Six ways a rent roll lies to you
7. Market pages: Greenville, Columbia, Charlotte *(local intent, low competition)*

> **Set expectations.** Organic search will not produce deal one's capital. Ranking takes six to
> twelve months, and cold arrivals screen hardest on track record. **Podcasts, local networks and
> CPA relationships are the channels that matter now.**

---

## 10. Design direction

Every colour sampled from the supplied logo: forest `#164338`, gold `#B78C34`, indigo `#353087`,
taupe `#ABA098`, over cream. Small-text gold darkened to `#7E5D20` so 11px type clears 4.5:1.

**Typography.** Cormorant Garamond 300 for display, tight leading and negative tracking — the
light weight at scale is the point. Figtree for UI, body and tabular data. Eyebrows in Figtree
600, 11px, 0.2em tracking — the only uppercase on the site.

**The mallard idea.** Calm above the waterline, working constantly below it. It survives as the
organising idea and drives the ripple motif, but it is no longer the headline — a sponsor with no
track record cannot afford to be poetic before being clear.

**Logo handling.** The supplied artwork is flat colour on an opaque white rectangle, so no CSS
filter can make it work on a dark ground. Four transparent assets were extracted instead — full
lockup and emblem-only, each in brand colour and cream. The nav uses a single element with the
image swapped by CSS, making a duplicate mark structurally impossible.

**Motion.** Hero lines rise on 1000ms `cubic-bezier(.23,1,.32,1)`, 90ms stagger, once per load.
Scroll reveals 760ms, 70ms stagger, fired once. Map pins drop with slight overshoot, 150ms apart.
Hover 160–220ms, gated behind `(hover:hover) and (pointer:fine)`. `prefers-reduced-motion` removes
every transform; entrance states are scoped behind a `.js` class so the page renders complete
without JavaScript.

---

## 11. Measurement — measure the list, not the raise

There is nothing to subscribe to, so subscription metrics are meaningless. The question is: *when
deal one lands, how many qualified people take the call?*

| Metric | Target | Read it as |
|---|---|---|
| Checklist downloads | 6–12% | The main number right now |
| Intro calls booked / month | 8–15 | Is the honesty positioning earning conversations? |
| Accredited & $100K+ on form | >50% | Is the site pre-qualifying? |
| Call → "call me when you have one" | >40% | The real conversion today |
| Scroll depth past Commitments | >55% | Does naming the gap hold people, or lose them? |
| "Have you done this before?" opens | track it | The most diagnostic number on the site |

Instrument every FAQ accordion as a GoHighLevel event. If people open *"Have you done this
before?"* and then leave, the honesty is landing as disqualification — and the answer needs to
work harder, not move down the page.

---

## 12. Open items

| Item | Status | Risk if shipped as-is |
|---|---|---|
| Preferred return | **Blank on intake** | Offering page shows 7% — drafted, not chosen |
| Equity split | **Blank on intake** | Shows 70/30 to a 15% IRR then 60/40 |
| Fee schedule | **Blank on intake** | 1.5% / 2% / 1% are conventional drafts |
| Target IRR & multiple | Client-supplied | 15–17% and 1.8–2.2x are forward-looking from a sponsor with no deals. Hero-card disclaimer removed at client request; footer disclosures carry the load alone |
| Securities counsel | **None named** | Nothing on a 506(c) site should go live unreviewed |
| Calendar link | Not set up | "Schedule a call" is a form plus manual reply |
| Form endpoint | Simulated | Submissions go nowhere until wired to GoHighLevel |
| Investor portal | Not needed yet | Header link is a placeholder |
| Headshot | Pending | Intake referenced a file that wasn't attached |
| Photography | Blocked | Requires a real building |

> ⚠️ **Before the domain resolves.** Have securities counsel review the live site end to end.
> 506(c) permits the advertising this site does, but it makes every figure on it a representation
> — and three of the deal terms currently displayed were drafted by an agency, not decided by the
> sponsor.
