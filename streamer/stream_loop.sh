#!/bin/bash

# Varta Pravah - Oracle Auto-Stream Script
# This script loops through all mp4 files in the videos directory.
# Note: Using '-stream_loop -1' inside the loop will cause FFmpeg to loop 
# the FIRST file infinitely. If you want to rotate through multiple news bulletins, 
# you should remove the '-stream_loop -1' flag.

VIDEO_DIR="/home/ubuntu/videos"

while true
do
  for file in $VIDEO_DIR/*.mp4
  do
    echo "🌐 [STREAM] Playing: $file"
    ffmpeg -re -stream_loop -1 -i "$file" \
      -c:v libx264 -preset veryfast -b:v 2500k \
      -c:a aac -b:a 128k \
      -f flv rtmp://localhost/live/stream
  done
done
