#!/bin/bash

# Varta Pravah - DYNAMIC QUEUE SYSTEM (The Brain)
# This script periodically scans for new news bulletins and updates the playout queue.

VIDEO_DIR="/home/ubuntu/videos"
PLAYLIST="/home/ubuntu/queue/playlist.txt"

echo "🧠 [QUEUE-MANAGER] Brain is active. Monitoring $VIDEO_DIR..."

while true; do
  # 1. Start fresh with the FFmpeg header
  echo "ffconcat version 1.0" > "$PLAYLIST"

  # 2. INTRO: Always start with the Promo (Branding First)
  if [ -f "/app/app/assets/premium_promo.mp4" ]; then
    echo "file '/app/app/assets/premium_promo.mp4'" >> "$PLAYLIST"
  elif [ -f "/app/assets/promo.mp4" ]; then
    echo "file '/app/assets/promo.mp4'" >> "$PLAYLIST"
  fi

  # 3. PRIORITY: Add Breaking News Bulletins
  for file in "$VIDEO_DIR"/breaking/*.mp4; do
    if [ -f "$file" ]; then
      echo "file '$file'" >> "$PLAYLIST"
    fi
  done

  # 4. STANDARD: Add regular news bulletins
  counter=0
  has_news=false
  for file in "$VIDEO_DIR"/*.mp4; do
    if [ -f "$file" ]; then
      echo "file '$file'" >> "$PLAYLIST"
      has_news=true
      ((counter++))
      
      # Insert promo every 5 videos (approx every 15 min)
      if [ $((counter % 5)) -eq 0 ]; then
        if [ -f "/app/app/assets/premium_promo.mp4" ]; then
          echo "file '/app/app/assets/premium_promo.mp4'" >> "$PLAYLIST"
        else
          echo "file '/app/assets/promo.mp4'" >> "$PLAYLIST"
        fi
      fi
    fi
  done

  # 5. IDLE LOOP: If no news, add Promo + Fallback Loop
  if [ "$has_news" = false ]; then
     if [ -f "/app/app/assets/premium_promo.mp4" ]; then
       echo "file '/app/app/assets/premium_promo.mp4'" >> "$PLAYLIST"
     else
       echo "file '/app/assets/promo.mp4'" >> "$PLAYLIST"
     fi
  fi

  # 6. ZERO-DOWNTIME SECRET: Always add the long loop fallback at the end
  echo "file '/app/assets/fallback.mp4'" >> "$PLAYLIST"

  # Wait 10 seconds before the next sync
  sleep 10
done
