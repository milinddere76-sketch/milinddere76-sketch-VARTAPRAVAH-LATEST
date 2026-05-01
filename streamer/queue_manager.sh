#!/bin/bash

# Varta Pravah - DYNAMIC QUEUE SYSTEM (The Brain)
# This script periodically scans for new news bulletins and updates the playout queue.

VIDEO_DIR="/home/ubuntu/videos"
PLAYLIST="/home/ubuntu/queue/playlist.txt"

echo "🧠 [QUEUE-MANAGER] Brain is active. Monitoring $VIDEO_DIR..."

while true; do
  # 1. Start fresh with the FFmpeg header
  echo "ffconcat version 1.0" > "$PLAYLIST"

  # 2. PRIORITY: Add Breaking News Bulletins first
  for file in "$VIDEO_DIR"/breaking/*.mp4; do
    if [ -f "$file" ]; then
      echo "file '$file'" >> "$PLAYLIST"
    fi
  done

  # 3. STANDARD: Add regular news bulletins
  counter=0
  for file in "$VIDEO_DIR"/*.mp4; do
    if [ -f "$file" ]; then
      echo "file '$file'" >> "$PLAYLIST"
      ((counter++))
      
      # Insert promo every 5 videos (approx every 15 min)
      if [ $((counter % 5)) -eq 0 ]; then
        echo "file '/app/assets/promo.mp4'" >> "$PLAYLIST"
      fi
    fi
  done

  # 4. ZERO-DOWNTIME SECRET: Always add the long loop fallback at the end
  # This ensures FFmpeg always has content to read before the next loop cycle.
  echo "file '/app/assets/fallback.mp4'" >> "$PLAYLIST"

  # Wait 10 seconds before the next sync
  sleep 10
done
