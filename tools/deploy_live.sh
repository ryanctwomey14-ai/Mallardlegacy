#!/bin/sh
# Publish site/ to gh-pages for the LIVE domain.
#
# The difference from tools/deploy_preview.sh is the whole point of having two
# scripts: the preview deploy blocks search engines (robots Disallow, noindex
# on every page) because it is an unapproved draft on a github.io URL. This one
# does NOT block them, and writes the CNAME file GitHub Pages needs to serve
# the custom domain.
#
# Run this only once the client has approved and the domain is pointed.
#
#   sh tools/deploy_live.sh
set -e

DOMAIN="www.mallardlegacypartners.com"

ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK="$ROOT/../.mlp-live"
BRANCH=_live

cd "$ROOT"
python tools/build_pages.py >/dev/null

git branch -D "$BRANCH" 2>/dev/null || true
[ -d "$WORK" ] && git worktree remove --force "$WORK" 2>/dev/null || true

git subtree split --prefix site -b "$BRANCH" >/dev/null
git worktree add -q "$WORK" "$BRANCH"

cd "$WORK"

# Skip Jekyll so underscore-prefixed paths are served verbatim.
touch .nojekyll

# Tell GitHub Pages which host to answer on. Without this it serves only the
# github.io URL and the custom domain returns a 404.
printf '%s\n' "$DOMAIN" > CNAME

# Sanity check: nothing here should be telling search engines to stay away.
# thank-you.html is noindex on purpose (a post-conversion page), and robots.txt
# legitimately disallows that one path — so both checks are exact, not loose.
BLOCKED=$(grep -l 'noindex' *.html 2>/dev/null | grep -v '^thank-you.html$' || true)
if [ -n "$BLOCKED" ]; then
  echo "ERROR: noindex found on pages that should be indexed:" >&2
  echo "$BLOCKED" >&2
  exit 1
fi
if grep -qx 'Disallow: /' robots.txt 2>/dev/null; then
  echo "ERROR: robots.txt blocks the whole site. Refusing to deploy." >&2
  exit 1
fi

git add -A
git commit -q -m "Deploy live site to $DOMAIN" || true
git push -q --force origin "$BRANCH":gh-pages

cd "$ROOT"
git worktree remove --force "$WORK" 2>/dev/null || true
git branch -D "$BRANCH" >/dev/null 2>&1 || true

echo "Deployed to gh-pages for $DOMAIN"
echo "Remember: GitHub repo Settings > Pages > Custom domain must read $DOMAIN"
