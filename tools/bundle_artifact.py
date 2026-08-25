# -*- coding: utf-8 -*-
"""
Bundle the whole site into ONE self-contained HTML file for review.

Everything is inlined -- CSS, JS, images as data URIs -- and the eleven pages
become routes behind a hash router so navigation can be reviewed end to end
from a single link. This is a preview artifact only; /site stays the
deployable build.

    python tools/bundle_artifact.py <output.html>
"""
import base64, glob, json, mimetypes, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

PAGES = ["index", "strategy", "about", "faq",
         "contact", "thank-you", "disclosures", "privacy"]


def data_uri(relpath):
    path = os.path.join(SITE, relpath)
    mime = "image/svg+xml" if relpath.endswith(".svg") else \
        (mimetypes.guess_type(path)[0] or "application/octet-stream")
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


ASSETS = {}
for sub in ("img", "video"):
    for f in sorted(glob.glob(os.path.join(SITE, "assets", sub, "*"))):
        rel = "assets/%s/%s" % (sub, os.path.basename(f))
        ASSETS[rel] = data_uri(rel)


def read(p):
    with open(os.path.join(SITE, p), encoding="utf-8") as f:
        return f.read()


def inline_assets(html):
    html = re.sub(r'\s*data-video-webm="[^"]*"', "", html)
    for rel, uri in ASSETS.items():
        html = html.replace('"%s"' % rel, '"%s"' % uri)
    return html


def route_links(html):
    """x.html -> #/x , leaving mail/tel/external/in-page anchors alone."""
    return re.sub(r'(href)="([a-z0-9\-]+)\.html"', r'\1="#/\2"', html)


# ---- shared shell, lifted out of index.html ----
index_src = read("index.html")
sprite = re.search(r'(<svg width="0" height="0".*?</defs></svg>)', index_src, re.S).group(1)
nav = re.search(r'(<header class="nav.*?</header>)', index_src, re.S).group(1)
drawer = re.search(r'(<div class="drawer".*?</div>\s*\n)', index_src, re.S).group(1)
footer = re.search(r'(<footer class="footer">.*?</footer>)', index_src, re.S).group(1)

css = re.sub(r"@import url\([^)]*\);\s*", "", read("assets/css/main.css"))
# CSS references images as ../img/NAME; HTML uses assets/img/NAME. Inline both.
for _rel, _uri in ASSETS.items():
    css = css.replace('"../img/%s"' % os.path.basename(_rel), '"%s"' % _uri)
js = read("assets/js/main.js")
agent_js = read("assets/js/agent.js")
# The agent builds its own DOM in JS, so the HTML asset/link rewriting above
# never sees its image or its call-to-action. Patch both for the bundle.
agent_js = agent_js.replace('"assets/img/mallard-mark-light.png"',
                            '"%s"' % ASSETS["assets/img/mallard-mark-light.png"])
agent_js = agent_js.replace("var CALL_URL = 'contact.html';",
                            "var CALL_URL = '#/contact';")

# ---- each page's <main> becomes a route ----
routes, titles = [], {}
for name in PAGES:
    src = read("%s.html" % name)
    titles[name] = re.search(r"<title>(.*?)</title>", src, re.S).group(1).strip()
    body = re.search(r'<main id="main">(.*?)</main>', src, re.S).group(1)
    routes.append('<div class="route" data-route="%s"%s>%s</div>'
                  % (name, "" if name == "index" else " hidden", body))

shell = inline_assets(route_links("\n".join(routes)))
nav = inline_assets(route_links(nav))
drawer = inline_assets(route_links(drawer))
footer = inline_assets(route_links(footer))

titles_js = ",".join("%s:%s" % (json.dumps(k), json.dumps(v)) for k, v in titles.items())

# The bundled count-up answers the router's event as well as the observer,
# because a counter first shown by a route change never re-intersects.
js = js.replace(
    "counters.forEach(function (el) { cio.observe(el); });",
    "counters.forEach(function (el) {\n"
    "        cio.observe(el);\n"
    "        el.addEventListener('countup', function () { run(el); });\n"
    "      });")

ROUTER = """
/* ---- Review-bundle router -------------------------------------------
   The deployed site is eleven real HTML files. This single-file build
   swaps <div class="route"> blocks so navigation can be reviewed from
   one link. Nothing else about the pages changes. */
(function () {
  var TITLES = {%s};
  var routes = document.querySelectorAll('.route');
  var links  = document.querySelectorAll('.nav__link, .drawer a[href^="#/"]');

  function show(name, isInitial) {
    var found = false;
    routes.forEach(function (r) {
      var match = r.dataset.route === name;
      if (match) found = true;
      r.hidden = !match;
    });
    if (!found) { show('index', isInitial); return; }

    if (TITLES[name]) document.title = TITLES[name];
    links.forEach(function (a) {
      var t = (a.getAttribute('href') || '').replace('#/', '');
      if (t === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    if (!isInitial) {
      window.scrollTo({ top: 0, behavior: 'auto' });
      var navEl = document.querySelector('[data-nav]');
      if (navEl) navEl.classList.remove('nav--scrolled');
    }

    // Reveal what is already in view on the newly shown route -- those
    // elements were observed while display:none and never intersected.
    var active = document.querySelector('.route[data-route="' + name + '"]');
    if (!active) return;
    window.requestAnimationFrame(function () {
      active.querySelectorAll('.reveal, .ripple-rule').forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in');
      });
      active.querySelectorAll('[data-count]').forEach(function (el) {
        if (el.dataset.done) return;
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.dataset.done = '1';
          el.dispatchEvent(new CustomEvent('countup'));
        }
      });
    });
  }

  function current() { return location.hash.replace('#/', '') || 'index'; }
  window.addEventListener('hashchange', function () { show(current(), false); });
  show(current(), true);
})();
""" % titles_js

BANNER = """
<div class="reviewbar">
  <span class="reviewbar__dot" aria-hidden="true"></span>
  <span><strong>Review build.</strong> All eleven pages in one file &mdash;
  navigation works, figures are placeholders.</span>
</div>
"""

BANNER_CSS = """
.route[hidden]{display:none}
.reviewbar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:500;
  display:flex;align-items:center;gap:10px;max-width:calc(100% - 32px);
  padding:9px 16px;border-radius:999px;font-family:var(--font-ui);font-size:12.5px;
  line-height:1.4;color:#F4F0E7;background:rgba(7,29,23,.92);
  border:1px solid rgba(223,193,129,.34);box-shadow:0 8px 32px rgba(7,29,23,.34);
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.reviewbar strong{color:#DFC181;font-weight:600}
.reviewbar__dot{width:6px;height:6px;border-radius:50%;background:#C9A04B;flex:none}
@media print{.reviewbar{display:none}}
"""

HEAD = """<title>Mallard Legacy Partners</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Figtree:wght@400;500;600;700&display=swap">
<script>document.documentElement.classList.add('js');</script>
<style>
"""

# The Artifact wrapper owns <head>, so this file cannot declare its own
# <meta charset>. Emit pure ASCII instead and encoding can never be guessed
# wrong: HTML text becomes numeric entities, while script and style content
# -- where entities are NOT decoded -- gets \\u escapes or ASCII fallbacks.
def js_ascii(s):
    return "".join(c if ord(c) < 128 else "\\u%04x" % ord(c) for c in s)


def css_ascii(s):
    return s.encode("ascii", "replace").decode("ascii")


def html_ascii(s):
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")


PARTS = [
    ("html", HEAD),
    ("css", css),
    ("css", BANNER_CSS),
    ("html", '</style>\n\n<a class="skip-link" href="#main">Skip to main content</a>\n'),
    ("html", sprite),
    ("html", nav),
    ("html", drawer),
    ("html", '\n<main id="main">\n'),
    ("html", shell),
    ("html", "\n</main>\n"),
    ("html", footer),
    ("html", BANNER),
    ("html", "\n<script>\n"),
    ("js", js),
    ("js", agent_js),
    ("js", ROUTER),
    ("html", "\n</script>\n"),
]

OUT = "".join(
    html_ascii(p) if k == "html" else js_ascii(p) if k == "js" else css_ascii(p)
    for k, p in PARTS)

assert OUT.isascii(), "bundle still contains non-ASCII"

dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "mallard-review.html")
with open(dest, "w", encoding="ascii") as f:
    f.write(OUT)

print("wrote %s  (%.1f KB, ascii-safe)" % (dest, os.path.getsize(dest) / 1024))
print("routes: %s" % ", ".join(PAGES))
