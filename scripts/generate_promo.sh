#!/bin/bash

# Varta Pravah Premium Promo Generator
# Stitches 4K-Style Slides into a cinematic loop

OUTPUT="/app/assets/premium_promo.mp4"
ASSETS="/app/assets"

echo "🎬 [PROMO] Generating Premium Cinematic Loop..."

# Using FFmpeg to create a 30-second slideshow from the 5 premium slides
# Each slide shows for 6 seconds with a subtle crossfade
ffmpeg -y -loop 1 -t 6 -i $ASSETS/promo_1.png \
-loop 1 -t 6 -i $ASSETS/promo_2.png \
-loop 1 -t 6 -i $ASSETS/promo_3.png \
-loop 1 -t 6 -i $ASSETS/promo_4.png \
-loop 1 -t 6 -i $ASSETS/promo_5.png \
-filter_complex \
"[0:v]fade=t=in:st=0:d=1,fade=t=out:st=5:d=1[v0]; \
 [1:v]fade=t=in:st=0:d=1,fade=t=out:st=5:d=1[v1]; \
 [2:v]fade=t=in:st=0:d=1,fade=t=out:st=5:d=1[v2]; \
 [3:v]fade=t=in:st=0:d=1,fade=t=out:st=5:d=1[v3]; \
 [4:v]fade=t=in:st=0:d=1,fade=t=out:st=5:d=1[v4]; \
 [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p $OUTPUT

echo "✅ [PROMO] Premium Promo generated at $OUTPUT"
