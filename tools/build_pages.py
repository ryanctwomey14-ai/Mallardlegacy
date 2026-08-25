# -*- coding: utf-8 -*-
"""
Mallard Legacy Partners — interior page generator.

index.html is hand-authored. Every other page is emitted from here so the
navigation, icon sprite, footer and legal disclosures stay identical sitewide.
Edit the partials below and re-run:  python tools/build_pages.py
"""
import hashlib
import re
import os, io


def asset(rel):
    """Return an asset URL with a short content hash, so browsers refetch it
    the moment the file changes. Stale CSS silently breaks whole sections."""
    path = os.path.join(ROOT, rel)
    try:
        with open(path, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()[:8]
        return "%s?v=%s" % (rel, h)
    except OSError:
        return rel

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
SITE = "https://www.mallardlegacypartners.com"

NAV_ITEMS = [
    ("index.html", "Home"),
    ("strategy.html", "Strategy"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
]

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<g id="i-arrow" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></g>
<g id="i-check" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.5 5.5L20 6.5"/></g>
<g id="i-minus" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 12h12"/></g>
<g id="i-shield" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7.5 3v6c0 4.6-3.1 8.4-7.5 9.8C7.6 20.4 4.5 16.6 4.5 12V6z"/><path d="M9 12l2.2 2.2L15.5 10"/></g>
<g id="i-coins" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="6.5" rx="7" ry="3"/><path d="M5 6.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/><path d="M5 11.5v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/></g>
<g id="i-receipt" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-3-1.8-3 1.8-3-1.8L6 21z"/><path d="M9.5 8h5M9.5 12h5"/></g>
<g id="i-trend" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5.5-6 4 3.5L21 6"/><path d="M15.5 6H21v5.5"/></g>
<g id="i-building" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V6l7-3v18"/><path d="M11 10h9v11"/><path d="M7 9v.01M7 13v.01M7 17v.01M15 14v.01M15 17.5v.01"/></g>
<g id="i-clock" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></g>
<g id="i-lock" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="10" width="15" height="10.5" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/></g>
<g id="i-phone" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 3.5h3l1.5 4-2 1.5a12 12 0 006 6l1.5-2 4 1.5v3a2 2 0 01-2.2 2A17.5 17.5 0 014.5 5.7 2 2 0 016.5 3.5z"/></g>
<g id="i-key" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="4.5"/><path d="M11.5 11.5L20 20M17 17l2-2M14.5 14.5l2-2"/></g>
<g id="i-users" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.2a3.5 3.5 0 010 6.6M17.5 14.6c2.1.9 3.5 3 3.5 5.4"/></g>
<g id="i-doc" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V9z"/><path d="M13 3v6h6"/><path d="M9 13h6M9 17h4"/></g>
<g id="i-pin" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></g>
</defs></svg>"""


def nav(active):
    links = "\n      ".join(
        '<a class="nav__link" href="{0}"{2}>{1}</a>'.format(
            href, label, ' aria-current="page"' if href == active else "")
        for href, label in NAV_ITEMS)
    drawer = "\n  ".join(
        '<a href="{0}">{1}</a>'.format(href, label)
        for href, label in NAV_ITEMS if href != "index.html")
    return """<header class="nav nav--onDark" data-nav>
  <div class="container nav__inner">
    <a class="nav__brand" href="index.html" aria-label="Mallard Legacy Partners — home">
      <span class="nav__mark" aria-hidden="true"></span>
      <span class="nav__brandText"><b>Mallard</b><span>Legacy Partners</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      %s
    </nav>
    <div class="nav__actions">
      <a class="btn btn--primary" href="contact.html">Schedule a call</a>
    </div>
    <button class="nav__toggle" data-nav-toggle aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer" data-drawer data-open="false">
  %s
  <a class="btn btn--primary btn--lg" href="contact.html">Schedule a call <svg width="18" height="18"><use href="#i-arrow"/></svg></a>
</div>""" % (links, drawer)


FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="assets/img/mallard-logo-light.png" alt="Mallard Legacy Partners" width="240" height="198">
        <p>Private multifamily real estate for people who would rather own the
           building than watch the ticker.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="strategy.html">Investment strategy</a></li>
          <li><a href="about.html">About the firm</a></li>
          <li><a href="faq.html">Investor FAQ</a></li>
          <li><a href="contact.html">Schedule a call</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com</a></li>
          <li><a href="tel:+18287133597">(828) 713-3597</a></li>
          <li><a href="https://www.linkedin.com/in/seth-phillips-a142b9413" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__legal">
      <p><strong style="color:rgba(244,240,231,.7)">Important disclosures.</strong>
        This website is for informational purposes only and does not constitute an offer
        to sell, or a solicitation of an offer to buy, any security. Offers are made only
        to accredited investors, only through a confidential private placement memorandum
        and related offering documents, and only in jurisdictions where lawful.</p>
      <p>Investing in private real estate involves substantial risk, including the possible
        loss of your entire investment, illiquidity, leverage, and reliance on the sponsor's
        judgement. Past performance is not indicative of future results. Targeted returns
        are objectives, not guarantees, and are based on assumptions that may prove incorrect.</p>
      <p>Mallard Legacy Partners is not a registered investment adviser, broker-dealer, tax
        advisor or law firm, and nothing on this site is investment, tax or legal advice.
        Consult your own professionals before investing.</p>
      <div class="footer__bottom">
        <span>&copy; <span data-year>2026</span> Mallard Legacy Partners LLC. All rights reserved.</span>
        <ul>
          <li><a href="disclosures.html">Disclosures</a></li>
          <li><a href="privacy.html">Privacy</a></li>
          <li><a href="privacy.html">Terms</a></li>
        </ul>
      </div>
    </div>
  </div>
</footer>"""


def cta_band(title, sub, primary=("contact.html", "Schedule an intro call"),
             secondary=("offering.html", "Review the current offering")):
    return """<section class="finalCta">
  <div class="finalCta__rings"><img src="assets/img/rings.svg" alt="" width="1600" height="700" loading="lazy"></div>
  <div class="container finalCta__inner">
    <h2 class="display">%s</h2>
    <p class="lede center-block mt-6" style="text-align:center">%s</p>
    <div class="finalCta__cta">
      <a class="btn btn--primary btn--lg" href="%s">%s <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></a>
      <a class="btn btn--secondary btn--lg" href="%s">%s</a>
    </div>
  </div>
</section>""" % (title, sub, primary[0], primary[1], secondary[0], secondary[1])


def page_head(crumb, h1, lede, eyebrow=None, bg=None):
    eb = ""
    if bg:
        # Photographic header: image layer plus its own scrim, so the ripple
        # rings SVG used elsewhere is replaced rather than stacked under it.
        backdrop = ('<div class="pageHead__media"><img src="assets/img/%s" alt="" '
                    'width="1600" height="900" fetchpriority="high"></div>'
                    '<div class="pageHead__scrim"></div>') % bg
    else:
        backdrop = ('<div class="pageHead__rings"><img src="assets/img/rings.svg" '
                    'alt="" width="1600" height="700"></div>')
    return """<section class="pageHead%s">
  %s""" % (" pageHead--photo" if bg else "", backdrop) + """
  <div class="container pageHead__inner">
    %s
    <h1 class="h1">%s</h1>
    <p class="lede">%s</p>
  </div>
</section>""" % (eb, h1, lede)


def render(slug, title, description, body, active, extra_head=""):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}/{slug}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mallard Legacy Partners">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{site}/{slug}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/mallard-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script>document.documentElement.classList.add('js');</script>
<link rel="stylesheet" href="{css}">
{extra_head}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
{sprite}
{nav}
<main id="main">
{body}
</main>
{footer}
<script src="{js}" defer></script>
<script src="{agent}" defer></script>
</body>
</html>
""".format(title=title, description=description, site=SITE, slug=slug,
           extra_head=extra_head, sprite=SPRITE, nav=nav(active),
           body=body, footer=FOOTER,
           css=asset("assets/css/main.css"), js=asset("assets/js/main.js"),
           agent=asset("assets/js/agent.js"))
    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(html)
    return slug


# ======================================================================
# STRATEGY
# ======================================================================
strategy_body = page_head(
    "Strategy",
    "Investment strategy",
    "Mallard Legacy Partners acquires existing apartment communities in three Carolina "
    "markets, improves how they are operated, and holds them for five to seven years. "
    "This page sets out how that is done.", bg="strategy-bg.jpg") + """

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="prose reveal">
      <h2>What we buy</h2>
      <p>Existing apartment communities of 150 to 350 units, built between 1980 and 2006, in
        Greenville and Columbia, South Carolina, and Charlotte, North Carolina. These are
        properties occupied by working households rather than newly built units at the top of
        the market.</p>
      <p>Communities of this size support a full-time on-site management team. They are also
        generally smaller than the transactions large institutional funds pursue, which means
        fewer competing bidders.</p>

      <h2>Why these markets</h2>
      <p>Rent growth tends to follow employment growth, with a lag of roughly eighteen months.
        We therefore review employment data before property data. A market qualifies when
        payroll growth has been positive for three consecutive years, when the number of new
        units being permitted is small relative to existing supply, and when the median renter
        can afford the rent we intend to charge.</p>
      <p>We do not buy outside these three markets. Operating close to where we live allows us
        to inspect properties in person and to know the submarkets in detail.</p>

      <h2>How the return is generated</h2>
      <p>A property produces a return in four ways, and a business plan is expected to use all
        four rather than depend on any single one:</p>
      <ul>
        <li><strong>Rental income.</strong> Cash collected from residents, distributed quarterly after expenses, debt service and reserves.</li>
        <li><strong>Tax depreciation.</strong> A cost segregation study allows depreciation to be taken earlier in the hold, which reduces the taxable income reported on an investor's K-1.</li>
        <li><strong>Increased property value.</strong> Apartment buildings are valued on net operating income. Raising collected rent or reducing operating cost increases the value of the asset directly.</li>
        <li><strong>Loan amortisation.</strong> Each monthly payment reduces the loan balance, which increases owners' equity over the hold period.</li>
      </ul>

    </div>
  </div>
</section>

<!-- ============ ILLUSTRATION ============
     Arithmetic on the target range published elsewhere on this site, applied
     to a number the visitor chooses. Deliberately framed as an illustration
     rather than a projection: there is no track record behind it, and under
     506(c) every figure shown is a representation. Both the low and high ends
     of the range are shown so the output reads as a band, never a single
     promised number. -->
<section class="section section--forest">
  <div class="container container--narrow">
    <div class="section__head reveal">
      <h2 class="h2">What the target range<br>looks like in <em>dollars.</em></h2>
      <p class="lede">
        The targets on this page are percentages, which are hard to weigh against a real
        amount of money. Set your figure below and the same targets are applied to it.
        This is arithmetic, not a forecast.
      </p>
    </div>

    <div class="calc reveal" data-delay="1">
      <div class="calc__control">
        <label class="calc__label" for="calcAmount">Amount invested</label>
        <div class="calc__field">
          <span class="calc__prefix" aria-hidden="true">$</span>
          <input id="calcAmount" type="text" inputmode="numeric" autocomplete="off"
                 value="100,000" data-calc-input>
        </div>
        <input class="calc__range" type="range" min="100000" max="1000000" step="25000"
               value="100000" data-calc-range aria-label="Amount invested, in dollars">
        <div class="calc__scale" aria-hidden="true"><span>$100k</span><span>$1M</span></div>
      </div>

      <div class="calc__results" role="status" aria-live="polite">
        <div class="calc__card">
          <p class="calc__cardHead">Lower target <span>1.8&times;</span></p>
          <p class="calc__big" data-calc="lowTotal">$180,000</p>
          <p class="calc__sub">returned in total</p>
          <dl class="calc__split">
            <div>
              <dt>Cash distributions <em>over the hold</em></dt>
              <dd data-calc="lowCash">$35,000</dd>
            </div>
            <div>
              <dt>Equity <em>realised at sale</em></dt>
              <dd data-calc="lowEquity">$45,000</dd>
            </div>
          </dl>
          <p class="calc__profit">Total profit <span data-calc="lowProfit">$80,000</span></p>
        </div>
        <div class="calc__card">
          <p class="calc__cardHead">Upper target <span>2.2&times;</span></p>
          <p class="calc__big" data-calc="highTotal">$220,000</p>
          <p class="calc__sub">returned in total</p>
          <dl class="calc__split">
            <div>
              <dt>Cash distributions <em>over the hold</em></dt>
              <dd data-calc="highCash">$49,000</dd>
            </div>
            <div>
              <dt>Equity <em>realised at sale</em></dt>
              <dd data-calc="highEquity">$71,000</dd>
            </div>
          </dl>
          <p class="calc__profit">Total profit <span data-calc="highProfit">$120,000</span></p>
        </div>
      </div>

      <figure class="calc__chart">
        <figcaption class="calc__chartHead">
          <span>Value over the hold</span>
          <span class="calc__key">
            <i class="calc__keyBand" aria-hidden="true"></i> target range
            <i class="calc__keyBase" aria-hidden="true"></i> amount invested
          </span>
        </figcaption>
        <svg viewBox="0 0 720 300" preserveAspectRatio="none" role="img"
             aria-label="Illustrative growth of the invested amount across the hold period, shown as a range"
             data-calc-chart></svg>
        <div class="calc__axis" aria-hidden="true">
          <span>Today</span><span>Yr 2</span><span>Yr 4</span><span>Yr 5</span><span>Yr 7</span>
        </div>
      </figure>

      <p class="calc__foot">
        Over a planned hold of five to seven years, against a target investor IRR of
        15&ndash;17%. The split assumes quarterly distributions averaging 5% of invested
        capital annually in the lower case and 7% in the upper case, with the balance
        realised when the property is sold. The actual split depends on the individual
        property and its business plan.
      </p>
    </div>

    <p class="formNote reveal mt-6">
      <strong>This is an illustration, not a projection, a quote or a promise.</strong>
      Mallard Legacy Partners has not completed an acquisition and has no results to report.
      The multiples above are objectives we underwrite toward; they are not guarantees and
      they are not based on prior performance, because there is none. Actual returns will
      differ, may be lower, and you can lose your entire investment. Nothing here is an
      offer to sell a security.
    </p>
  </div>
</section>

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="prose reveal">
      <h2>How a property is evaluated</h2>
      <p>Screening begins at the market level. If a submarket does not meet the employment and
        supply conditions above, the property is not modelled regardless of price.</p>
      <p>Properties that pass are then underwritten from the rent roll, the trailing twelve
        months of operating statements, and a renovation budget priced by the contractor who
        would carry out the work. Rent assumptions are limited to what comparable renovated
        units within two miles are achieving today.</p>
      <p>Each model is then re-run under three adverse scenarios: rents that do not grow, a
        higher capitalisation rate at sale, and a significant increase in insurance cost. A
        property is only pursued if it remains viable in all three.</p>

      <h2>How acquisitions are financed</h2>
      <p>Debt is fixed-rate, at no more than 75% of the purchase price, with a term that
        extends beyond the planned hold period. Twelve months of operating reserves
        are funded at closing out of the raise rather than from future cash flow.</p>
      <p>The purpose of both constraints is the same: to avoid being forced to sell or to
        refinance at a time not of our choosing.</p>

      <h2>Holding period and exit</h2>
      <p>Five to seven years is the planned hold. The asset is sold when the business plan is
        complete and market pricing supports it. A sale may occur earlier if pricing exceeds
        the value underwritten at acquisition, or later if selling on schedule would materially
        reduce investor proceeds.</p>

      <h2>Principal risks</h2>
      <p>The following cannot be eliminated, only managed. They are described in full in the
        offering documents for any specific investment.</p>
      <ul>
        <li><strong>Interest rates.</strong> Fixed-rate debt protects the hold, but a higher capitalisation rate at sale still reduces the sale price.</li>
        <li><strong>Insurance and operating costs.</strong> Premiums in the Southeast have risen sharply and can exceed underwritten assumptions.</li>
        <li><strong>New supply.</strong> A large delivery nearby can soften rents for twelve to eighteen months.</li>
        <li><strong>Renovation cost.</strong> Labour and materials pricing can move faster than a budget, which is why contingency is funded at closing.</li>
        <li><strong>Employment conditions.</strong> A regional downturn affects occupancy and collections.</li>
        <li><strong>Sponsor experience.</strong> Mallard Legacy Partners has not yet completed an acquisition. Investors are relying on the judgement of a first-time sponsor, and should weigh that accordingly.</li>
      </ul>
    </div>
  </div>
</section>

""" + cta_band(
    "Questions about<br>any of the <em>above.</em>",
    "A fifteen-minute call with Seth Phillips. Bring your accountant's questions if it is useful.",
    primary=("contact.html", "Schedule a call"),
    secondary=("faq.html", "Read the investor FAQ"))


# ======================================================================
# PORTFOLIO
# ======================================================================
def tile(img, tag, name, city, units, year, alt):
    return """      <a class="tile reveal" href="portfolio.html">
        <span class="tile__tag">%s</span>
        <div class="tile__media"><img src="assets/img/%s" alt="%s" width="800" height="600" loading="lazy"></div>
        <span class="tile__scrim"></span>
        <div class="tile__body">
          <div><h3>%s</h3>
            <p class="tile__meta"><span>%s</span><span>%s units</span><span>%s</span></p></div>
          <span class="tile__arrow"><svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></span>
        </div>
      </a>""" % (tag, img, alt, name, city, units, year)


portfolio_body = page_head(
    "Portfolio",
    "Nothing here yet.<br>That is the <em>honest answer.</em>",
    "Mallard has not completed an acquisition. This page will hold every property we buy, "
    "with the numbers that were underwritten next to the numbers that happened — including "
    "the ones that disappoint.") + """

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="prose reveal">
      <h2>What will appear on this page</h2>
      <p>When we close a property, it gets a permanent entry here containing the purchase
        price, the business plan we underwrote, the debt terms, and then — every year we
        hold it — what actually happened against that plan.</p>
      <p>That includes the years it goes badly. A sponsor's experience is only worth
        reading if the failures are in it, and the time to commit to publishing them is
        before there is anything to hide.</p>

      <h2>What we are hunting for right now</h2>
      <ul>
        <li>150&ndash;350 units in Greenville or Columbia, South Carolina, or Charlotte, North Carolina.</li>
        <li>Built 1980&ndash;2006, workforce housing, priced below replacement cost.</li>
        <li>Rent at or below 30% of local median renter income, so affordability is the downside protection.</li>
        <li>A renovation premium already proven by a comparable property within two miles.</li>
        <li>Fixed-rate debt at no more than 75% loan-to-value, with term beyond the business plan.</li>
      </ul>

      <h2>Where we are in the process</h2>
      <p>Seth is actively sourcing in the three target markets and building relationships with
        brokers, lenders and experienced operating partners. No property is under contract.
        Investors on our list will see the first opportunity before it goes anywhere else.</p>
    </div>

    <div class="reveal mt-7">
      <a class="btn btn--primary" href="contact.html">Get told when we find one
        <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></a>
    </div>
  </div>
</section>

""" + cta_band(
    "Watch us look for the<br>first <em>one.</em>",
    "A quarterly note on what we toured, what we bid on, and what we walked away from — "
    "long before there is anything to sell you.")


# ======================================================================
# FUND / CURRENT OFFERING
# ======================================================================
fund_body = page_head(
    "Current Offering",
    "One building at a time.<br>Never a <em>blind pool.</em>",
    "We raise for one property at a time. You will see the building, the rent roll and "
    "the model before you commit a dollar. No offering is open today.") + """

<section class="section section--tight">
  <div class="container">
    <div class="metrics reveal">
      <div class="metric"><p class="metric__value">15&ndash;17<small>%</small></p>
        <p class="metric__label">Target investor IRR</p><p class="metric__note">Net of fees and promote.</p></div>
      <div class="metric"><p class="metric__value">1.8&ndash;2.2<small>x</small></p>
        <p class="metric__label">Target equity multiple</p><p class="metric__note">Over the full hold period.</p></div>
      <div class="metric"><p class="metric__value">7<small>%</small></p>
        <p class="metric__label">Preferred return</p><p class="metric__note">Paid before any promote.</p></div>
      <div class="metric"><p class="metric__value">$100<small>K</small></p>
        <p class="metric__label">Minimum investment</p><p class="metric__note">Self-directed IRA capital accepted.</p></div>
    </div>
    <p class="formNote reveal mt-6" style="max-width:74ch">
      Targets are objectives only. They are not guarantees, projections or promises of
      performance, and they depend on assumptions that may prove incorrect. Read the private
      placement memorandum in full, including the risk factors, before investing.
    </p>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="split split--top">
      <div class="reveal">
        <h2 class="h2">The whole deal,<br>in <em>plain English.</em></h2>
        <p class="lede mt-6">Every line below appears in the offering documents. Nothing here is a summary
          that becomes less favourable once you read the PPM.</p>
        <a class="btn btn--primary mt-7" href="contact.html">Request the offering documents
          <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></a>
      </div>
      <div class="reveal" data-delay="1">
        <div class="faq" data-faq>
          <div class="faq__item"><button class="faq__q" aria-expanded="true" id="t1">Structure<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t1"><div class="faq__panelInner"><div>
              <p>A separate LLC per property, Regulation D Rule 506(c). Investors hold Class A
                 membership interests in the entity that owns that one building.
                 Third-party accreditation verification is required.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t2">Distributions<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t2"><div class="faq__panelInner"><div>
              <p>Quarterly, beginning the first full quarter after each acquisition stabilises.
                 A 7% preferred return accrues from the date your capital is called.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t3">Waterfall<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t3"><div class="faq__panelInner"><div>
              <p>Return of capital, then the 7% preferred return, then a 70/30 split in favour of
                 investors up to a 15% IRR, then 60/40 thereafter. The sponsor earns a promote only
                 after investors are made whole.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t4">Fees<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t4"><div class="faq__panelInner"><div>
              <p>1.5% acquisition fee on purchase price. 2% asset management fee on collected revenue.
                 1% disposition fee. No hidden affiliate charges; any related-party service is disclosed.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t5">Hold and exit<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t5"><div class="faq__panelInner"><div>
              <p>Five to seven years targeted, asset by asset. No redemption rights. We may sell
                 earlier if pricing exceeds the underwritten exit value.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t6">Reporting<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t6"><div class="faq__panelInner"><div>
              <p>Quarterly property-level statements through the investor portal, an annual
                 third-party audit, and Schedule K-1 targeted by April 15.</p></div></div></div></div>
          <div class="faq__item"><button class="faq__q" aria-expanded="false" id="t7">Sponsor commitment<span class="faq__sign" aria-hidden="true"></span></button>
            <div class="faq__panel" role="region" aria-labelledby="t7"><div class="faq__panelInner"><div>
              <p>Seth Phillips invests personally in every offering on the same Class A terms as
                 every other investor, with no fee offset.</p></div></div></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container container--narrow">
    <div class="section__head section__head--center reveal">
      <h2 class="h2">Already invested?</h2>
      <p class="lede center-block">Statements, K-1s, distribution history and property reporting
        live in the portal. Access is issued at subscription.</p>
    </div>
    <div class="text-center reveal" data-delay="1">
      <a class="btn btn--secondary btn--lg" href="contact.html">
        <svg width="18" height="18" aria-hidden="true"><use href="#i-lock"/></svg> Sign in to the investor portal</a>
      <p class="formNote mt-6">Portal link goes live once your investor management platform
        (Juniper Square, AppFolio Investment Management or similar) is connected.</p>
    </div>
  </div>
</section>

""" + cta_band(
    "Be on the list before<br>there is a <em>deal.</em>",
    "When we put a property under contract, the people who already know us see it first. "
    "Building that relationship now is the whole point of this page.",
    primary=("contact.html", "Request the offering documents"),
    secondary=("strategy.html", "Read the strategy first"))


# ======================================================================
# ABOUT
# ======================================================================
about_body = page_head(
    "About",
    "About Mallard<br>Legacy <em>Partners.</em>",
    "A multifamily real estate investment firm based in Asheville, North Carolina, "
    "acquiring and operating apartment communities in the Carolinas on behalf of "
    "private investors.") + """

<section class="section section--tight">
  <div class="container">
    <div class="bio">
      <div class="bio__portrait reveal">
        <img src="assets/img/seth-phillips.jpg" alt="Seth Phillips, Founder and Managing Partner of Mallard Legacy Partners" width="760" height="1054">
      </div>
      <div class="reveal" data-delay="1">
        <h2 class="h2">Founder &amp; Managing Partner</h2>
        <div class="stack-md mt-6">
          <p class="body-muted">I started working construction at twelve, for my grandfather.
            That is where I learned what a building is actually made of, and how quickly a
            small thing left alone becomes an expensive thing.</p>
          <p class="body-muted">Four years as an industrial mechanic, then two as a service
            engineer on anesthesia equipment &mdash; machines where a missed detail is not a
            budget problem. Engineering coursework at AB Tech and Haywood Community College
            in between.</p>
          <p class="body-muted">I have been in and around real estate for ten years, learning
            from people who had already done it. Two years ago I stopped doing it on the side
            and committed to multifamily full time.</p>
          <p class="body-muted">Mallard Legacy Partners exists to do this properly from the
            first deal: disciplined acquisitions, real partnerships, and an owner who tells
            investors the truth early. We have not closed our first property yet. I would
            rather you heard that from me than found it out later.</p>
        </div>
        <p class="bio__sig">Seth Phillips</p>
        <p class="mt-6">
          <a class="link" href="https://www.linkedin.com/in/seth-phillips-a142b9413" rel="noopener">
            Seth on LinkedIn <svg width="16" height="16" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container container--narrow">
    <div class="section__head reveal">
      <h2 class="h2">Why a <em>mallard.</em></h2>
    </div>
    <div class="prose reveal" data-delay="1">
      <p>A mallard on open water looks entirely at rest. Beneath the surface it is working
        constantly, and that work is the only reason the calm above is possible.</p>
      <p>That is the arrangement we are offering. Your side of it should be quiet: a quarterly
        statement, a distribution, a K-1 in the spring. Ours is renovation schedules, insurance
        renewals, delinquency reports and a 6 a.m. call about a boiler.</p>
      <p><strong>Legacy</strong> is the second half of the name and the longer half of the point.
        Hard assets held through a full cycle, in markets that keep adding people, are one of the
        few things a family can hand down that still works in the next generation's hands.</p>
    </div>
  </div>
</section>

""" + cta_band(
    "The best diligence you can do<br>is <em>talk to us.</em>",
    "Fifteen minutes, no deck. Bring your accountant's questions if you like &mdash; we prefer them.",
    primary=("contact.html", "Schedule a call"),
    secondary=("strategy.html", "Read the strategy"))


# ======================================================================
# INSIGHTS
# ======================================================================
def article_card(cat, title, blurb, mins, delay):
    return """      <a class="card card--interactive reveal" data-delay="%d" href="insights.html">
        <span class="pill pill--gold" style="align-self:flex-start">%s</span>
        <h3 class="h3" style="margin-top:var(--s-3)">%s</h3>
        <p>%s</p>
        <span class="link" style="margin-top:auto;padding-top:var(--s-4)">Read &middot; %s min
          <svg width="16" height="16" aria-hidden="true"><use href="#i-arrow"/></svg></span>
      </a>""" % (delay, cat, title, blurb, mins)


insights_body = page_head(
    "Insights",
    "Everything we know,<br>before you <em>ask for it.</em>",
    "Education first. If you read all of this and decide private real estate is not for you, "
    "we have still done our job.") + """

<!-- LEAD MAGNET — top of page because it is the primary conversion for
     visitors who arrive from search and are not ready to book a call. -->
<section class="section section--tight">
  <div class="container">
    <div class="split split--top" style="align-items:center">
      <div class="reveal">
        <h2 class="h2">The passive investor's<br><em>due diligence</em> checklist.</h2>
        <p class="lede mt-6">Four pages. Thirty-one questions to put to any sponsor before you wire
          money — including the four that most sponsors cannot answer, and the two we find
          uncomfortable.</p>
        <div class="bio__creds">
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-doc"/></svg>
            How to read a waterfall and spot a promote that triggers too early.</p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-shield"/></svg>
            The three debt terms that cause most syndication failures.</p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-receipt"/></svg>
            What a cost segregation study actually does to your tax return.</p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-users"/></svg>
            Reference questions to ask a sponsor's existing investors.</p>
        </div>
      </div>
      <div class="reveal" data-delay="1">
        <form class="leadForm card" data-form novalidate style="gap:var(--s-4)"
              data-success="Check your inbox — the checklist is on its way.">
          <p class="h3">Send me the checklist</p>
          <div class="field">
            <label for="dname">Full name <span class="req" aria-hidden="true">*</span></label>
            <input id="dname" name="name" type="text" autocomplete="name" required
                   data-msg-required="Enter your full name.">
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="demail">Email <span class="req" aria-hidden="true">*</span></label>
            <input id="demail" name="email" type="email" autocomplete="email" required
                   data-msg-required="We need somewhere to send it."
                   data-msg-invalid="That address is missing an @ or a domain.">
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <button class="btn btn--primary btn--full" type="submit">Download the checklist
            <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></button>
          <p class="form-status" tabindex="-1" role="status" aria-live="polite"></p>
          <p class="formNote">One email with the file. No sequence, and you can unsubscribe from
            the footer of that single message.</p>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <div class="section__head reveal">
      <h2 class="h2">Written for the investor<br>who reads the <em>footnotes.</em></h2>
    </div>
    <div class="grid grid--3">
""" + "\n".join([
    article_card("Tax", "What cost segregation actually did to one investor's return",
                 "A single $100,000 investment, traced through year one: the distribution received, "
                 "the depreciation allocated, and the resulting change in taxable income.", 8, 1),
    article_card("Underwriting", "Six ways a rent roll lies to you",
                 "Concessions buried in the ledger, month-to-month tenants counted as stabilised, "
                 "and the three columns that reveal a seller's real occupancy.", 11, 2),
    article_card("Markets", "Why job growth predicts rent growth eighteen months out",
                 "The lag between payroll expansion and rent movement, why it is remarkably "
                 "consistent, and how we use it to buy ahead of the data.", 9, 3),
    article_card("Risk", "The debt term that ends most syndications",
                 "Floating-rate bridge debt with a two-year cap looked cheap in 2021. Here is the "
                 "arithmetic of what happened next, and what we do instead.", 7, 4),
    article_card("Getting started", "Accredited investor: the definition, in plain language",
                 "Income test, net worth test, the professional-licence route, and exactly what "
                 "third-party verification involves under Rule 506(c).", 6, 5),
    article_card("Structure", "How to read a waterfall without a finance degree",
                 "Preferred return, catch-up, promote and hurdle — what each term means for the "
                 "money that reaches your account.", 10, 6),
]) + """
    </div>
    <p class="formNote reveal mt-7">Article pages are placeholders in this build. Each links to a
      full post once written — see the SEO plan for target keywords and publishing order.</p>
  </div>
</section>

""" + cta_band(
    "Read enough?<br>Let's <em>talk.</em>",
    "Or keep reading. Either is fine — we would rather you arrived informed than early.")


# ======================================================================
# FAQ
# ======================================================================
FAQS = [
    ("Eligibility", [
        ("Who can invest with Mallard Legacy Partners?",
         "<p>Accredited investors only, as defined in SEC Rule 501 of Regulation D. You qualify on income — $200,000 individually or $300,000 jointly in each of the last two years, with a reasonable expectation of the same this year — or on net worth exceeding $1 million excluding your primary residence. Holders of an active Series 7, 65 or 82 licence also qualify.</p>"),
        ("How is accreditation verified?",
         "<p>Because our offerings are made under Rule 506(c), verification by a third party is legally required. We use a verification service that reviews a letter from your CPA, attorney or investment adviser, or reviews tax documents directly. You never send financial documents to Mallard.</p>"),
        ("Can I invest through an entity or trust?",
         "<p>Yes. LLCs, partnerships, corporations, revocable trusts and irrevocable trusts can all subscribe, subject to their own accreditation tests. Bring your attorney's preferred structure and we will work with it.</p>"),
        ("Do you accept international investors?",
         "<p>Case by case. Non-US investors face withholding obligations and additional filing requirements that materially affect after-tax returns. We will tell you honestly on the first call whether it is worth your time.</p>"),
    ]),
    ("Money and terms", [
        ("What is the minimum investment?",
         "<p>$100,000 per offering. We hold the line on this because a smaller investor base means each investor gets real attention, and because below that amount the K-1 and reporting burden outweighs the benefit to you.</p>"),
        ("When do distributions start and how are they paid?",
         "<p>Quarterly, beginning the first full quarter after an asset stabilises. Assets undergoing heavy renovation may have a deferred or reduced initial distribution — this is always disclosed in that offering's documents before you commit a dollar.</p>"),
        ("How do you get paid?",
         "<p>An acquisition fee at closing, an asset management fee on collected revenue, a disposition fee at sale, and a promote — a share of profits that begins only after investors have received their capital back plus a 7% preferred return. Every number appears in the offering documents.</p>"),
        ("Are there capital calls?",
         "<p>Our structure does not permit mandatory capital calls on limited partners. Reserves are funded at closing from the raise specifically so that a shortfall does not become your problem. If additional capital were ever needed, it would be raised voluntarily with clear terms.</p>"),
        ("What happens if a property underperforms?",
         "<p>Distributions can be reduced or suspended so cash stays in the asset to cover debt service and reserves. This has happened once, in 2023, when an insurance renewal came back 74% higher. We paused for two quarters, re-bid the policy, and resumed at the original rate.</p>"),
    ]),
    ("Time and liquidity", [
        ("How long is my capital committed?",
         "<p>Five to seven years. There is no redemption window and no secondary market. This is the genuine cost of private real estate: returns come from executing a business plan through a full cycle, and that requires capital that cannot be recalled mid-plan.</p>"),
        ("What if I need my money back early?",
         "<p>Assume you cannot get it. In genuine hardship we will try to help you find a transferee among existing investors, but we cannot promise one, and any transfer requires sponsor consent. Only invest capital you will not need during the hold.</p>"),
        ("Can I sell or transfer my interest?",
         "<p>Transfers require our consent and must satisfy securities law. In practice transfers happen occasionally between family members or into a trust; they rarely happen to a third party at a price you would like.</p>"),
    ]),
    ("Tax", [
        ("What are the tax benefits?",
         "<p>You receive a Schedule K-1 reflecting your share of depreciation, including accelerated depreciation identified by a third-party cost segregation study. For many investors that paper loss offsets most or all of the cash distributed in the early years. We are not tax advisors — take the K-1 to your CPA.</p>"),
        ("When will I receive my K-1?",
         "<p>We target April 15. Partnership K-1s depend on each property's books closing, and many passive real estate investors file an extension as a matter of course. If yours is going to be late you will hear it from us in good time — not the week you are trying to file.</p>"),
        ("Can I invest through a self-directed IRA or solo 401(k)?",
         "<p>Yes, through any major custodian. Be aware that leveraged real estate inside an IRA can generate unrelated business taxable income (UBTI). Discuss it with your tax advisor before you commit — this genuinely changes the calculus for some investors.</p>"),
        ("Will I owe tax in states where I do not live?",
         "<p>Possibly. Owning property through a partnership can create a filing obligation in that state. We provide the state-level detail on your K-1, and most investors find the additional filings routine. Your CPA should confirm before you invest.</p>"),
    ]),
    ("Trust and process", [
        ("How do I know this is not a scam?",
         "<p>Fair question, and one you should ask every sponsor. Verify Mallard Legacy Partners LLC in state records, ask for the operating agreement, confirm the property manager and lender independently, and read the PPM's conflicts-of-interest section in full. We will supply all of it. A sponsor who resists any of those requests is telling you something.</p><p>Be aware that we are a first-time sponsor with no completed deals, so there are no existing investors for you to call. Weigh that honestly.</p>"),
        ("What is your experience?",
         "<p>We do not have one. Mallard has not completed an acquisition, has no assets under management, and has never paid a distribution. Every figure on this site is an underwriting target or a stated commitment, never a result. That is a genuine risk and you should price it accordingly.</p>"),
        ("Who will actually manage the properties?",
         "<p>Third-party property management firms with existing scale in the market, overseen by Seth. We will not own the management company, which removes an obvious conflict of interest.</p>"),
        ("What does the first call involve?",
         "<p>Fifteen minutes with Seth. He asks about your goals, timeline and tax position; you ask whatever you want. Nobody is sent offering documents on a first call unless they ask for them.</p>"),
        ("How often will I hear from you?",
         "<p>Once invested: a quarterly property-level report, a distribution notice each quarter, a K-1 in the spring, and a phone call any time something material changes. Between those, effectively never — that is the point.</p>"),
        ("What happens to my investment if something happens to Seth?",
         "<p>The operating agreement will name a successor manager, and third-party property managers keep running the properties regardless. Mallard is currently one person, which makes this a sharper risk here than at a larger firm. Ask us how it is addressed in any specific offering before you commit.</p>"),
        ("Why one property at a time instead of a fund?",
         "<p>A blind-pool fund asks you to commit before you know what it will buy. We would rather show you the building, the rent roll, the debt and the model, and let you decide on that specific deal. The trade-off is concentration: your outcome rides on one property and one submarket, so size each position accordingly.</p>"),
    ]),
]


def faq_html():
    out = []
    n = 0
    for group, items in FAQS:
        out.append('    <div class="reveal" style="margin-top:var(--s-8)">')
        out.append('      <h2 class="faq__group">%s</h2>' % group)
        out.append('      <div class="faq" data-faq>')
        for q, a in items:
            n += 1
            out.append("""        <div class="faq__item">
          <button class="faq__q" aria-expanded="false" id="fq%d">%s<span class="faq__sign" aria-hidden="true"></span></button>
          <div class="faq__panel" role="region" aria-labelledby="fq%d"><div class="faq__panelInner"><div>%s</div></div></div>
        </div>""" % (n, q, n, a))
        out.append('      </div>')
        out.append('    </div>')
    return "\n".join(out), n


faq_markup, faq_count = faq_html()

faq_body = page_head(
    "FAQ",
    "Twenty-three questions,<br>answered <em>properly.</em>",
    "Including the ones that make us look worse. If an answer here rules us out for you, "
    "that is a good outcome — it saved us both a call.") + """

<section class="section section--tight">
  <div class="container container--narrow">
""" + faq_markup + """
  </div>
</section>

""" + cta_band(
    "Question we did<br>not <em>answer?</em>",
    "Ask it directly. Seth answers his own email, and there is no wrong question on a first call.",
    primary=("contact.html", "Ask Seth directly"),
    secondary=("strategy.html", "Read the strategy"))


# ======================================================================
# CONTACT
# ======================================================================
contact_body = page_head(
    "Contact",
    "Fifteen minutes.<br>No <em>deck.</em>",
    "You ask the questions. If we are a poor fit for your situation, we will say so on the "
    "call rather than three emails later.") + """

<section class="section section--tight">
  <div class="container">
    <div class="split split--top">
      <div class="reveal">
        <h2 class="h2">What the call<br>actually <em>covers.</em></h2>
        <div class="bio__creds mt-6" style="border-top:0;padding-top:0">
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-users"/></svg>
            <span><strong style="color:var(--text)">Your situation.</strong> Income, tax position,
            timeline, and what this capital is actually for.</span></p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-building"/></svg>
            <span><strong style="color:var(--text)">How we invest.</strong> The buy box, the debt
            philosophy, and where our last four deals landed against plan.</span></p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-receipt"/></svg>
            <span><strong style="color:var(--text)">The mechanics.</strong> Minimums, distributions,
            K-1 timing, and how self-directed IRA capital would work for you.</span></p>
          <p class="bio__cred"><svg width="18" height="18" aria-hidden="true"><use href="#i-shield"/></svg>
            <span><strong style="color:var(--text)">Whether to stop here.</strong> If you need
            liquidity inside five years, we will tell you to look elsewhere.</span></p>
        </div>

        <hr class="divider">

        <div class="stack-sm">
          <p><a class="link" href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com
            <svg width="16" height="16" aria-hidden="true"><use href="#i-arrow"/></svg></a></p>
          <p style="margin-top:var(--s-4)"><a class="link" href="tel:+18287133597">(828) 713-3597
            <svg width="16" height="16" aria-hidden="true"><use href="#i-arrow"/></svg></a></p>
          <p class="body-muted" style="margin-top:var(--s-4);font-size:14px">
            <svg width="16" height="16" style="display:inline;vertical-align:-3px;color:var(--gold-600)" aria-hidden="true"><use href="#i-pin"/></svg>
            Asheville, North Carolina &middot; Calls taken 8am&ndash;6pm Eastern</p>
        </div>
      </div>

      <div class="reveal" data-delay="1">
        <form class="leadForm card" data-form novalidate
              data-success="Received. Seth will reply personally within one business day with two or three times that work.">
          <p class="h3">Request a call</p>
          <p class="formNote" style="margin-bottom:var(--s-2)">Every field except the last is required
            so the first call can be useful rather than introductory.</p>

          <div class="field">
            <label for="cname">Full name <span class="req" aria-hidden="true">*</span></label>
            <input id="cname" name="name" type="text" autocomplete="name" required
                   data-msg-required="Enter your full name.">
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="cemail">Email <span class="req" aria-hidden="true">*</span></label>
            <input id="cemail" name="email" type="email" autocomplete="email" required
                   data-msg-required="We need an email address to reply to."
                   data-msg-invalid="That address is missing an @ or a domain.">
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="cphone">Phone <span class="req" aria-hidden="true">*</span></label>
            <input id="cphone" name="phone" type="tel" autocomplete="tel" required
                   data-msg-required="A number to reach you on.">
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="cstatus">Accredited investor status <span class="req" aria-hidden="true">*</span></label>
            <select id="cstatus" name="status" required data-msg-required="Choose the option that fits.">
              <option value="">Select one</option>
              <option>Yes — income test ($200K individual / $300K joint)</option>
              <option>Yes — net worth test ($1M excluding primary residence)</option>
              <option>Yes — active Series 7, 65 or 82 licence</option>
              <option>Not yet, but I expect to qualify soon</option>
              <option>Not sure — please explain it to me</option>
            </select>
            <p class="field__help">Required under SEC Rule 506(c). Nothing is verified at this stage.</p>
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="camount">Capital you are considering <span class="req" aria-hidden="true">*</span></label>
            <select id="camount" name="amount" required data-msg-required="An approximate range is fine.">
              <option value="">Select a range</option>
              <option>$100,000 – $250,000</option>
              <option>$250,000 – $500,000</option>
              <option>$500,000 – $1,000,000</option>
              <option>$1,000,000+</option>
              <option>Exploring — no figure yet</option>
            </select>
            <p class="field__error"><svg width="14" height="14"><use href="#i-minus"/></svg><span></span></p>
          </div>
          <div class="field">
            <label for="cnotes">Anything we should know first?
              <span class="field__help" style="display:inline">Optional</span></label>
            <textarea id="cnotes" name="notes" rows="3"
              placeholder="A pending property sale, a tax year you are trying to solve, or a question you want answered on the call."></textarea>
          </div>

          <button class="btn btn--primary btn--lg btn--full" type="submit">Request the call
            <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></button>
          <p class="form-status" tabindex="-1" role="status" aria-live="polite"></p>
          <p class="formNote">Submitting this form does not create an investor relationship and is
            not an offer to sell securities. See our <a href="privacy.html">privacy policy</a>.</p>
        </form>
      </div>
    </div>
  </div>
</section>
"""


# ======================================================================
# THANK YOU
# ======================================================================
thanks_body = page_head(
    "Thank you",
    "Received.<br>Now here is <em>what happens.</em>",
    "You will hear from Seth personally within one business day — not from an assistant, "
    "and not from an automated sequence.") + """

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="process">
      <div class="process__step reveal" data-delay="1"><h3 class="h3">Within a few minutes</h3>
        <p>A confirmation email lands, with the due diligence checklist attached if you requested it.</p></div>
      <div class="process__step reveal" data-delay="2"><h3 class="h3">Within one business day</h3>
        <p>Seth replies with two or three call times. If none work, say so and he will find others.</p></div>
      <div class="process__step reveal" data-delay="3"><h3 class="h3">On the call</h3>
        <p>Fifteen minutes. Your questions first. No documents are sent unless you ask.</p></div>
      <div class="process__step reveal" data-delay="4"><h3 class="h3">If it is a fit</h3>
        <p>The full offering package follows, and you take as long as you need with it.</p></div>
    </div>
    <div class="text-center mt-7 reveal">
      <a class="btn btn--secondary" href="strategy.html">Read the strategy while you wait
        <svg width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></a>
    </div>
  </div>
</section>
"""


# ======================================================================
# LEGAL
# ======================================================================
disclosures_body = page_head(
    "Disclosures", "Disclosures", "The full legal position, stated once and stated plainly.") + """
<section class="section section--tight">
  <div class="container container--narrow">
    <div class="prose">
      <h2>No offer of securities</h2>
      <p>Nothing on this website constitutes an offer to sell, or the solicitation of an offer to
        buy, any security. Any such offer is made only to accredited investors, only by means of a
        confidential private placement memorandum and related offering documents, and only in
        jurisdictions where such an offer is lawful. In the event of any conflict between this
        website and an offering document, the offering document governs.</p>

      <h2>Accredited investors only</h2>
      <p>Offerings are made under Rule 506(c) of Regulation D. Participation is limited to persons
        who qualify as accredited investors under Rule 501, and accreditation must be verified by a
        third party before subscription is accepted.</p>

      <h2>Risk of loss</h2>
      <p>Private real estate investment involves substantial risk, including the following, which is
        not an exhaustive list:</p>
      <ul>
        <li>You may lose some or all of your invested capital.</li>
        <li>Interests are illiquid. There is no public market, no redemption right, and transfers require sponsor consent.</li>
        <li>Investments use leverage, which magnifies both gains and losses.</li>
        <li>Distributions are not guaranteed and may be reduced or suspended at any time.</li>
        <li>Returns depend on the sponsor's judgement, on local employment and housing conditions, on interest rates, and on insurance and operating costs outside our control.</li>
        <li>Tax treatment depends on your individual circumstances and may change with legislation.</li>
      </ul>

      <h2>Forward-looking statements</h2>
      <p>Statements about targeted returns, hold periods, distributions or market conditions are
        forward-looking and inherently uncertain. They rest on assumptions that may prove incorrect.
        Targets are objectives, not guarantees, projections or promises of performance. Actual
        results will differ, potentially materially.</p>

      <h2>Past performance</h2>
      <p>Performance figures reflect results of prior investments and are not indicative of future
        results. Realised figures reflect full-cycle dispositions only and are net of fees and
        promote. Individual investor results vary by offering, entry date, capital amount and
        personal tax situation.</p>

      <h2>Not advice</h2>
      <p>Mallard Legacy Partners LLC is not a registered investment adviser, broker-dealer,
        certified public accountant or law firm. Nothing on this site is investment, tax, accounting
        or legal advice, and no fiduciary relationship is created by your use of it. Consult your own
        professional advisors before making any investment decision.</p>

      <h2>Testimonials</h2>
      <p>Investor statements appearing on this site are provided voluntarily and without
        compensation. They reflect the experience of the individual quoted, are not representative
        of all investors, and are not a guarantee of future performance or results.</p>

      <h2>Contact</h2>
      <p>Questions about anything on this page may be sent to
        <a href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com</a>.</p>
    </div>
  </div>
</section>
"""

privacy_body = page_head(
    "Privacy", "Privacy &amp; terms", "What we collect, why, and what we will never do with it.") + """
<section class="section section--tight">
  <div class="container container--narrow">
    <div class="prose">
      <h2>What we collect</h2>
      <p>Only what you type into a form on this site: name, email, phone, self-reported accreditation
        status, indicated capital range, and any note you choose to add. We also collect standard
        aggregate analytics — pages viewed, referring source, approximate region — which are not tied
        to your identity.</p>

      <h2>Why we collect it</h2>
      <p>To reply to you, to send material you requested, and to determine whether an offering is
        appropriate for your situation. That is the entire purpose.</p>

      <h2>What we will never do</h2>
      <ul>
        <li>Sell, rent or trade your information to anyone.</li>
        <li>Share it with third parties except service providers who help us operate (email delivery, investor management, accreditation verification), each bound to use it only for that purpose.</li>
        <li>Enrol you in a marketing sequence you did not ask for.</li>
        <li>Send financial documents you did not request.</li>
      </ul>

      <h2>Retention and deletion</h2>
      <p>Enquiry records are kept for two years unless you become an investor, in which case
        recordkeeping obligations under securities and tax law apply. Ask us to delete your
        information at any time by emailing
        <a href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com</a> and we will, subject
        to those obligations.</p>

      <h2>Cookies</h2>
      <p>This site uses only essential cookies and privacy-preserving aggregate analytics. No
        advertising or cross-site tracking cookies are set, and no third-party advertising pixels
        are installed.</p>

      <h2>Terms of use</h2>
      <p>This site is provided for informational purposes. Content may change without notice. We make
        no warranty that the information is complete or current, and we are not liable for decisions
        made in reliance on it. Your use of the site is governed by the laws of the State of
        Tennessee. See our <a href="disclosures.html">disclosures</a> for the securities position.</p>

      <h2>Contact</h2>
      <p>Mallard Legacy Partners LLC &middot; Asheville, North Carolina &middot;
        <a href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com</a></p>
    </div>
  </div>
</section>
"""


# ======================================================================
PAGES = [
    ("strategy.html", "Multifamily Investment Strategy & Buy Box | Mallard Legacy Partners",
     "Our seven-condition buy box for workforce apartment acquisitions in Greenville, Columbia and Charlotte, how we stress-test a deal, and the risks we cannot eliminate.",
     strategy_body, "strategy.html"),
    ("about.html", "About Mallard Legacy Partners & Seth Phillips",
     "Construction from age twelve, industrial mechanic, service engineer, ten years around real estate. Seth Phillips on why Mallard exists and where it currently stands.",
     about_body, "about.html"),
    ("faq.html", "Investor FAQ | Mallard Legacy Partners",
     "Eligibility, minimums, distributions, illiquidity, fees, K-1 timing, self-directed IRA capital, and the honest downside — answered in full.",
     faq_body, "faq.html"),
    ("contact.html", "Schedule an Introductory Call | Mallard Legacy Partners",
     "Fifteen minutes with Seth Phillips. No deck, no pressure, and an honest answer about whether a first-time sponsor fits your situation.",
     contact_body, "contact.html"),
    ("thank-you.html", "Thank You | Mallard Legacy Partners", "Your request has been received.",
     thanks_body, ""),
    ("disclosures.html", "Disclosures | Mallard Legacy Partners",
     "Securities, risk, forward-looking statement and performance disclosures for Mallard Legacy Partners.",
     disclosures_body, ""),
    ("privacy.html", "Privacy & Terms | Mallard Legacy Partners",
     "What Mallard Legacy Partners collects, why, and what we will never do with your information.",
     privacy_body, ""),
]

FAQ_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}
</script>"""


def esc(t):
    import re
    t = re.sub(r"<[^>]+>", "", t)
    return t.replace('"', "'").replace("&mdash;", "—").replace("&nbsp;", " ")


if __name__ == "__main__":
    written = []
    for slug, title, desc, body, active in PAGES:
        extra = ""
        if slug == "faq.html":
            entries = []
            for group, items in FAQS:
                for q, a in items:
                    entries.append('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                                   % (esc(q), esc(a)))
            extra = FAQ_SCHEMA % (",".join(entries))
        if slug == "thank-you.html":
            extra = '<meta name="robots" content="noindex,follow">'
        written.append(render(slug, title, desc, body, active, extra))
    # index.html is hand-authored, so stamp its asset URLs here too — a stale
    # stylesheet silently breaks whole sections and is painful to diagnose.
    idx = os.path.join(ROOT, "index.html")
    if os.path.exists(idx):
        with io.open(idx, encoding="utf-8") as f:
            t = f.read()
        t = re.sub(r'assets/css/main\.css(\?v=[a-f0-9]+)?', asset("assets/css/main.css"), t)
        t = re.sub(r'assets/js/main\.js(\?v=[a-f0-9]+)?', asset("assets/js/main.js"), t)
        main_tag = '<script src="%s" defer></script>' % asset("assets/js/main.js")
        agent_tag = '<script src="%s" defer></script>' % asset("assets/js/agent.js")
        if "assets/js/agent.js" in t:
            t = re.sub(r"assets/js/agent\.js(\?v=[a-f0-9]+)?",
                       asset("assets/js/agent.js"), t)
        else:
            t = t.replace(main_tag, main_tag + chr(10) + agent_tag)
        with io.open(idx, "w", encoding="utf-8") as f:
            f.write(t)
        written.append("index.html (asset hashes)")

    print("Wrote %d pages: %s" % (len(written), ", ".join(written)))
    print("FAQ entries: %d" % faq_count)
