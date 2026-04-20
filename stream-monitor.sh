#!/bin/bash

# VartaPravah Stream Monitor
# Continuously monitors FFmpeg process and restarts streamer if needed
# Usage: ./stream-monitor.sh

LOG_FILE="logs/stream-monitor.log"
CHECK_INTERVAL=15
RESTART_DELAY=5

# Ensure logs directory exists
mkdir -p logs

log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

log_message "Stream Monitor started"

while true; do
  if ! pgrep -f "ffmpeg.*rtmp" > /dev/null 2>&1; then
    log_message "WARNING: FFmpeg process not found - stream appears to have stopped"
    log_message "Attempting to restart vartapravah_stream service..."
    
    # Restart the streamer service
    docker restart vartapravah_stream >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
      log_message "SUCCESS: Streamer service restarted"
    else
      log_message "ERROR: Failed to restart streamer service"
    fi
    
    sleep $RESTART_DELAY
  else
    # Stream is running, check connection quality (optional)
    PROCESS_INFO=$(ps aux | grep "ffmpeg.*rtmp" | grep -v grep)
    log_message "Stream active: $(echo $PROCESS_INFO | awk '{print $2}')"
  fi

  sleep $CHECK_INTERVAL
done