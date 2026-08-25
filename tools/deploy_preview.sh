#!/bin/sh
# Publish site/ to the gh-pages branch for client review.
#
# The deployed copy is deliberately NOT indexable. This is an unapproved draft
# on a github.io URL: if Google crawls it, the draft competes with the real
# domain later and puts terms the sponsor has not signed off into search
# results. Production robots.txt and meta tags in site/ are left untouched —
# only the deployed copy is altered.
#
#   sh tools/deploy_preview.sh
set -e

ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK="$ROOT/../.mlp-preview"
BRANCH=_preview

cd "$ROOT"
python tools/build_pages.py >/dev/null

git branch -D "$BRANCH" 2>/dev/null || true
[ -d "$WORK" ] && git worktree remove --force "$WORK" 2>/dev/null || true

git subtree split --prefix site -b "$BRANCH" >/dev/null
git worktree add -q "$WORK" "$BRANCH"

cd "$WORK"

# Skip Jekyll so underscore-prefixed paths are served verbatim.
touch .nojekyll

cat > robots.txt <<'EOF'
# Client review draft — not for indexing.
User-agent: *
Disallow: /
EOF

rm -f sitemap.xml

# robots.txt stops crawling; the meta tag stops indexing of anything already
# discovered through a shared link. Both are needed.
python - <<'PY'
import glob, io, re
for p in glob.glob("*.html"):
    t = io.open(p, encoding="utf-8").read()
    t = re.sub(r'<meta name="robots" content="[^"]*">',
               '<meta name="robots" content="noindex,nofollow">', t)
    if 'name="robots"' not in t:
        t = t.replace("<title>", '<meta name="robots" content="noindex,nofollow">\n<title>', 1)
    io.open(p, "w", encoding="utf-8").write(t)
print("noindex applied to %d pages" % len(glob.glob("*.html")))
PY

git add -A
git commit -q -m "Deploy client review draft (noindex)" || true
git push -q --force origin "$BRANCH":gh-pages

cd "$ROOT"
git worktree remove --force "$WORK"
git branch -D "$BRANCH" >/dev/null 2>&1 || true

echo "Deployed to gh-pages."
