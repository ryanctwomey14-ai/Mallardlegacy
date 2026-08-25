#!/bin/sh
# Re-encode both background videos from the originals in the project root.
# Grade is tuned so the footage stays VISIBLE under its scrim: an earlier pass
# crushed it to median luminance 0.014, which rendered as flat colour.
set -e
G="hue=h=-24:s=0.60,eq=brightness=-0.05:contrast=1.04:gamma=0.94,colorbalance=rs=-0.04:gs=0.05:bs=-0.09:rm=-0.05:gm=0.05:bm=-0.09:rh=-0.04:gh=0.03:bh=-0.07"

# The aerial source is darker than the hero source (asphalt, roofs, tree line),
# so it carries its own lift. Matching grades made it read as flat colour.
GC="hue=h=-24:s=0.62,eq=brightness=0.05:contrast=1.02:gamma=1.12,colorbalance=rs=-0.04:gs=0.05:bs=-0.09:rm=-0.05:gm=0.05:bm=-0.09:rh=-0.04:gh=0.03:bh=-0.07"

loop () { # $1=src $2=out $3=tail_start_frame $4=crf $5=grade
  ffmpeg -v error -i "$1" -filter_complex \
  "[0:v]${5},scale=1600:900,setsar=1[g];[g]split=3[a][b][c];\
   [a]trim=start_frame=0:end_frame=60,setpts=PTS-STARTPTS[head];\
   [b]trim=start_frame=$3:end_frame=$(($3+60)),setpts=PTS-STARTPTS[tail];\
   [tail][head]blend=all_expr='A*(1-(N/60))+B*(N/60)'[bl];\
   [c]trim=start_frame=60:end_frame=$3,setpts=PTS-STARTPTS[rest];\
   [bl][rest]concat=n=2:v=1:a=0[out]" \
  -map "[out]" -an -c:v libx264 -crf "$4" -preset medium -pix_fmt yuv420p -movflags +faststart -y "$2"
}

loop "Mallard Hero.mp4"          site/assets/video/mallard-hero.mp4    360 27 "$G"
loop "Investment Case Video.mp4" site/assets/video/investment-case.mp4 390 28 "$GC"

for f in mallard-hero investment-case; do
  ffmpeg -v error -i site/assets/video/$f.mp4 -an -c:v libvpx-vp9 -crf 40 -b:v 0 \
    -row-mt 1 -deadline realtime -cpu-used 5 -pix_fmt yuv420p -y site/assets/video/$f.webm
done

ffmpeg -v error -i site/assets/video/mallard-hero.mp4    -ss 2 -frames:v 1 -q:v 6 -y site/assets/img/hero-poster.jpg
ffmpeg -v error -i site/assets/video/investment-case.mp4 -ss 3 -frames:v 1 -q:v 6 -y site/assets/img/investment-case-poster.jpg
echo "ENCODE COMPLETE"
