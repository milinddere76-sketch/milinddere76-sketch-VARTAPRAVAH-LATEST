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
  # AUDIO LOCK: Injecting silent audio track (Required for YouTube to go Live)
  ffmpeg -re -f concat -safe 0 -i "$PLAYLIST" \
    -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
    -vf "format=yuv420p,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k -maxrate 2500k -bufsize 5000k \
    -threads 0 -r 25 -g 50 -keyint_min 50 -x264-params "keyint=50" \
    -c:a aac -b:a 128k -ar 44100 -shortest -f flv -flvflags no_duration_filesize \
    "$YOUTUBE_RTMP_URL"

  echo "⚠️ [$(date)] Stream ended or crashed. Restarting in 2s..." >> "$LOG_FILE"
  sleep 2
done
