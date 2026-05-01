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
  echo "📺 [PLAYOUT] Starting live broadcast to Oracle relay..."
  ffmpeg -re -f concat -safe 0 -i "$PLAYLIST" \
    -c:v libx264 -preset ultrafast -tune zerolatency -c:a aac -b:a 128k -f flv \
    "rtmp://localhost:1935/live/stream"

  echo "⚠️ [$(date)] Stream ended or crashed. Restarting in 2s..." >> "$LOG_FILE"
  sleep 2
done
