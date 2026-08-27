#!/bin/sh
# Lighter encodes for phones. The desktop files are 1.8MB and 2.8MB, which is
# far too much to push over a cellular connection just for atmosphere. These
# are 960x540 at a higher CRF: same grade, roughly a quarter of the weight.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

for f in mallard-hero investment-case; do
  ffmpeg -v error -i "site/assets/video/$f.mp4" \
    -vf "scale=960:540" -an -c:v libx264 -crf 32 -preset medium \
    -pix_fmt yuv420p -movflags +faststart -y "site/assets/video/$f-mobile.mp4"
done

ls -la site/assets/video/*.mp4 | awk '{printf "%6.0f KB  %s\n", $5/1024, $9}'
echo "MOBILE ENCODE COMPLETE"
