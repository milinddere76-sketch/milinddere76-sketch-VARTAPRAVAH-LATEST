#!/bin/bash

# Varta Pravah - MASTER INITIALIZATION SCRIPT
echo "🚀 [INIT] Starting Varta Pravah Playout Node..."

# 1. Setup Environment
export YOUTUBE_RTMP_URL=${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2/qcu7-xesd-m4sv-9zvv-e335}
mkdir -p /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos/breaking /app/app/assets
chmod -R 777 /app/app/assets /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos

# 1b. AUTO-RESTORE: If images are missing from the volume mount, restore from internal backup
if [ -d "/app/app/backup_assets" ] && [ $(ls /app/app/assets/promo_*.png 2>/dev/null | wc -l) -eq 0 ]; then
    echo "📦 [INIT] Restoring branding assets from internal backup..."
    cp /app/app/backup_assets/*.png /app/app/assets/ 2>/dev/null || true
    cp /app/app/backup_assets/*.mp4 /app/app/assets/ 2>/dev/null || true
    chmod -R 777 /app/app/assets
fi

# 2. Configure Nginx (Inject Environment Variables)
envsubst '$YOUTUBE_RTMP_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx
echo "✅ [INIT] Nginx RTMP server online with injected configuration."

# 3. Generate Branded Promo (Self-Healing)
echo "🎬 [INIT] Verifying branding assets..."
ls -l /app/app/assets/

if [ ! -f "/app/app/assets/premium_promo.mp4" ] && [ ! -f "/app/app/assets/promo.mp4" ]; then
    echo "🔨 [INIT] Generating promo.mp4 from cinematic slides..."
    
    # Hunt for images in multiple potential locations
    SEARCH_PATH="/app/app/assets"
    [ ! -d "$SEARCH_PATH" ] && SEARCH_PATH="./assets"
    
    FILES_COUNT=$(ls $SEARCH_PATH/promo_*.png 2>/dev/null | wc -l)
    echo "📊 [INIT] Found $FILES_COUNT promo slides in $SEARCH_PATH."
    
    if [ "$FILES_COUNT" -gt 0 ]; then
        echo "🎨 [INIT] Rendering cinematic loop..."
        ffmpeg -framerate 1/5 -pattern_type glob -i "$SEARCH_PATH/promo_*.png" \
          -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
          -c:v libx264 -preset ultrafast -r 24 -pix_fmt yuv420p -y /app/app/assets/promo.mp4
    fi
    
    if [ -f "/app/app/assets/promo.mp4" ]; then
        echo "✅ [INIT] Promo generated successfully at /app/app/assets/promo.mp4"
    else
        echo "⚠️ [WARN] Promo generation failed. Creating emergency standby screen..."
        ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -vf "drawtext=text='VARTA PRAVAH NEWS standby...':fontcolor=white:fontsize=70:x=(w-tw)/2:y=(h-th)/2" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -y /app/app/assets/promo.mp4
    fi
fi

# 4. Sync Fallback
if [ ! -f "/app/app/assets/fallback.mp4" ]; then
    if [ -f "/app/app/assets/premium_promo.mp4" ]; then
        cp /app/app/assets/premium_promo.mp4 /app/app/assets/fallback.mp4
    else
        cp /app/app/assets/promo.mp4 /app/app/assets/fallback.mp4
    fi
fi

# 5. Launch the Brain (Queue Manager)
echo "🧠 [INIT] Starting the Brain (Queue Manager)..."
/app/queue_manager.sh &

# 6. Launch the Playout Engine
echo "📺 [INIT] Handing over to Playout Engine..."
/app/playout.sh
