#!/bin/bash

# Varta Pravah - MASTER INITIALIZATION SCRIPT
echo "🚀 [INIT] Starting Varta Pravah Playout Node..."

# 1. Setup Environment
# SMARTER FUSION: Ensure the Stream Key is present exactly ONCE
STREAM_KEY=${YOUTUBE_STREAM_KEY:-"qcu7-xesd-m4sv-9zvv-e335"}
BASE_URL=${YOUTUBE_RTMP_URL:-"rtmp://a.rtmp.youtube.com/live2/"}

if [[ "$BASE_URL" == *"$STREAM_KEY"* ]]; then
    echo "✅ [INIT] Stream Key already present in URL."
    FINAL_RTMP_URL="$BASE_URL"
else
    echo "🔧 [INIT] Appending Stream Key to Base URL..."
    [[ "$BASE_URL" != */ ]] && BASE_URL="$BASE_URL/"
    FINAL_RTMP_URL="${BASE_URL}${STREAM_KEY}"
fi

# Export for playout.sh and envsubst
export YOUTUBE_RTMP_URL="$FINAL_RTMP_URL"

# VERIFICATION: Show masked URL to confirm fusion worked
MASKED_URL=$(echo "$YOUTUBE_RTMP_URL" | sed 's/live2\/.*/live2\/XXXXX/')
echo "🔗 [INIT] Target Broadcast URL: $MASKED_URL"

mkdir -p /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos/breaking /app/assets
chmod -R 777 /app/assets /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos

# 1b. AUTO-RESTORE: If images are missing from the volume mount, restore from internal backup
if [ -d "/app/backup_assets" ] && [ $(ls /app/assets/promo_*.png 2>/dev/null | wc -l) -eq 0 ]; then
    echo "📦 [INIT] Restoring branding assets from internal backup..."
    cp /app/backup_assets/*.png /app/assets/ 2>/dev/null || true
    cp /app/backup_assets/*.mp4 /app/assets/ 2>/dev/null || true
    chmod -R 777 /app/assets
fi

# 2. Configure Nginx (Inject Environment Variables)
envsubst '$YOUTUBE_RTMP_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx
echo "✅ [INIT] Nginx RTMP server online with injected configuration."

# 3. Generate Branded Promo (Self-Healing)
echo "🎬 [INIT] Verifying branding assets..."
ls -l /app/assets/

if [ ! -f "/app/assets/premium_promo.mp4" ] && [ ! -f "/app/assets/promo.mp4" ]; then
    echo "🔨 [INIT] Generating promo.mp4 from cinematic slides..."
    
    # Hunt for images in multiple potential locations
    SEARCH_PATH="/app/assets"
    [ ! -d "$SEARCH_PATH" ] && SEARCH_PATH="./assets"
    
    FILES_COUNT=$(ls $SEARCH_PATH/promo_*.png 2>/dev/null | wc -l)
    echo "📊 [INIT] Found $FILES_COUNT promo slides in $SEARCH_PATH."
    
    if [ "$FILES_COUNT" -gt 0 ]; then
        echo "🎨 [INIT] Rendering cinematic loop..."
        ffmpeg -framerate 1/5 -pattern_type glob -i "$SEARCH_PATH/promo_*.png" \
          -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
          -c:v libx264 -preset ultrafast -r 25 -pix_fmt yuv420p -y /app/assets/promo.mp4
    fi
    
    if [ -f "/app/assets/promo.mp4" ]; then
        echo "✅ [INIT] Promo generated successfully at /app/assets/promo.mp4"
    else
        echo "⚠️ [WARN] Promo generation failed. Creating emergency standby screen..."
        ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -vf "drawtext=text='VARTA PRAVAH NEWS standby...':fontcolor=white:fontsize=70:x=(w-tw)/2:y=(h-th)/2" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -y /app/assets/promo.mp4
    fi
fi

# 4. Sync Fallback
if [ ! -f "/app/assets/fallback.mp4" ]; then
    if [ -f "/app/assets/premium_promo.mp4" ]; then
        cp /app/assets/premium_promo.mp4 /app/assets/fallback.mp4
    else
        cp /app/assets/promo.mp4 /app/assets/fallback.mp4
    fi
fi

# 5. Launch the Brain (Queue Manager)
echo "🧠 [INIT] Starting the Brain (Queue Manager)..."
/app/queue_manager.sh &

# 6. Launch the Playout Engine
echo "📺 [INIT] Handing over to Playout Engine..."
/app/playout.sh
