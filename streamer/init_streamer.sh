#!/bin/bash

# Varta Pravah - MASTER INITIALIZATION SCRIPT
echo "🚀 [INIT] Starting Varta Pravah Playout Node..."

# 1. Setup Environment
export YOUTUBE_RTMP_URL=${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2/qcu7-xesd-m4sv-9zvv-e335}
mkdir -p /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos/breaking
chmod -R 777 /app/assets /home/ubuntu/queue /home/ubuntu/logs /home/ubuntu/videos

# 2. Configure Nginx (Inject Environment Variables)
envsubst '$YOUTUBE_RTMP_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx
echo "✅ [INIT] Nginx RTMP server online with injected configuration."

# 3. Generate Branded Promo (Self-Healing)
echo "🎬 [INIT] Verifying branding assets..."
ls -l /app/assets/

if [ ! -f "/app/assets/promo.mp4" ]; then
    echo "🔨 [INIT] Generating promo.mp4 from cinematic slides..."
    # Robust check for any png files starting with promo_
    FILES_COUNT=$(ls /app/assets/promo_*.png 2>/dev/null | wc -l)
    echo "📊 [INIT] Found $FILES_COUNT promo slides."
    
    if [ "$FILES_COUNT" -gt 0 ]; then
        # Force render with explicit scale and format
        ffmpeg -framerate 1/5 -pattern_type glob -i '/app/assets/promo_*.png' \
          -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
          -c:v libx264 -r 24 -pix_fmt yuv420p -y /app/assets/promo.mp4
    fi
    
    if [ -f "/app/assets/promo.mp4" ]; then
        echo "✅ [INIT] Promo generated successfully."
    else
        echo "⚠️ [WARN] Promo generation failed or images missing. Creating emergency placeholder..."
        ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -vf "drawtext=text='VARTA PRAVAH NEWS':fontcolor=white:fontsize=60:x=(w-tw)/2:y=(h-th)/2" -c:v libx264 -pix_fmt yuv420p -y /app/assets/promo.mp4
    fi
fi

# 4. Sync Fallback
if [ ! -f "/app/assets/fallback.mp4" ]; then
    cp /app/assets/promo.mp4 /app/assets/fallback.mp4
fi

# 5. Launch the Brain (Queue Manager)
echo "🧠 [INIT] Starting the Brain (Queue Manager)..."
/app/queue_manager.sh &

# 6. Launch the Playout Engine
echo "📺 [INIT] Handing over to Playout Engine..."
/app/playout.sh
