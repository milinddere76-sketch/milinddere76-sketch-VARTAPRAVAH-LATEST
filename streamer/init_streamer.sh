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
    echo "🔨 [INIT] Generating promo.mp4 from slides..."
    # Explicitly look for promo_1.png through promo_5.png
    ffmpeg -framerate 1/5 -start_number 1 -i /app/assets/promo_%d.png \
      -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
      -c:v libx264 -r 24 -pix_fmt yuv420p -y /app/assets/promo.mp4
    
    if [ $? -eq 0 ]; then
        echo "✅ [INIT] Promo generated successfully."
    else
        echo "⚠️ [WARN] Promo generation failed. Creating emergency placeholder..."
        ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=10 -vf "drawtext=text='VARTA PRAVAH NEWS':fontcolor=white:fontsize=50:x=(w-tw)/2:y=(h-th)/2" -c:v libx264 -y /app/assets/promo.mp4
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
