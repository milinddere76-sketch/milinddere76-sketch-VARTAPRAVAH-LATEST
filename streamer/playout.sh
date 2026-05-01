#!/bin/bash

# Varta Pravah - NO STOP STREAM (PRO Architecture)
# This script uses the FFmpeg concat demuxer to play a dynamic playlist.

PLAYLIST="/home/ubuntu/queue/playlist.txt"
LOG_FILE="/home/ubuntu/logs/playout.log"

echo "🚀 [PRO-PLAYOUT] Starting continuous broadcast engine..."

# Wait for the Brain to create the first playlist
while [ ! -f "$PLAYLIST" ]; do
  echo "⏳ [WAIT] Waiting for Queue Manager to generate the first playlist..."
  sleep 2
done

while true; do

  # Use environment variable if present, otherwise default to the provided key
  TARGET_URL=${YOUTUBE_RTMP_URL:-rtmp://a.rtmp.youtube.com/live2/qcu7-xesd-m4sv-9zvv-e335}
  
  ffmpeg -re -f concat -safe 0 -i "$PLAYLIST" \
    -c:v libx264 -preset veryfast -b:v 2500k \
    -pix_fmt yuv420p -g 50 \
    -c:a aac -b:a 128k \
    -f flv "$TARGET_URL"

  echo "⚠️ [$(date)] Stream ended or crashed. Restarting in 2s..." >> "$LOG_FILE"
  sleep 2
done
