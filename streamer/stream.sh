#!/bin/sh

while true
do
  echo "📡 Streaming to YouTube..."

  # Note: $YOUTUBE_RTMP_URL should be set in the .env or docker-compose
  ffmpeg -re -stream_loop -1 -i /app/videos/output.mp4 \
  -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k \
  -pix_fmt yuv420p -g 50 \
  -c:a aac -b:a 128k \
  -f flv "$YOUTUBE_RTMP_URL"

  echo "⚠️ Stream crashed. Restarting in 5 sec..."
  sleep 5
done
