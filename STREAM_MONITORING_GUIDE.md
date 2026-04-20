# VartaPravah Stream Monitoring Guide

## Overview

**stream-monitor** is an automated FFmpeg process monitoring script that provides continuous health checks for your YouTube RTMP stream. It complements the Docker watchdog service with FFmpeg-specific process monitoring.

---

## Features

✅ **Continuous Monitoring** - Checks FFmpeg process every 15 seconds  
✅ **Auto-Restart** - Automatically restarts streamer if process dies  
✅ **Detailed Logging** - All events logged to `logs/stream-monitor.log`  
✅ **Dual Protection** - Works alongside Docker watchdog for redundancy  
✅ **Lightweight** - Minimal resource usage  
✅ **Production Ready** - Safe for 24/7 operation  

---

## Installation

### Linux/Mac

```bash
# Make executable
chmod +x stream-monitor.sh

# Run in background
./stream-monitor.sh &

# Or with nohup to survive terminal close
nohup ./stream-monitor.sh &
```

### Windows

```bash
# Run directly
stream-monitor.bat

# Or create scheduled task (see below)
```

---

## Usage

### Run in Foreground (for testing)
```bash
./stream-monitor.sh    # Linux/Mac
stream-monitor.bat     # Windows
```

### Run in Background

**Linux/Mac:**
```bash
# Background with output to logs
./stream-monitor.sh > /dev/null 2>&1 &

# Or with nohup (survives terminal close)
nohup ./stream-monitor.sh &

# Or in a tmux/screen session
tmux new-session -d -s stream-monitor './stream-monitor.sh'
```

**Windows:**
```cmd
# Run as scheduled task
Task Scheduler > Create Task > stream-monitor.bat

# Or use START command
START "" stream-monitor.bat
```

### Stop Monitoring

**Linux/Mac:**
```bash
# Find process
ps aux | grep stream-monitor

# Kill it
kill <PID>
```

**Windows:**
```cmd
# Find process
tasklist | findstr stream-monitor

# Kill it
taskkill /PID <PID> /F
```

---

## How It Works

### Monitoring Process

1. **Check Interval**: Every 15 seconds
2. **Process Check**: Looks for `ffmpeg.*rtmp` process
3. **If Found**: Logs active stream and continues
4. **If Not Found**: 
   - Logs warning
   - Attempts restart: `docker restart vartapravah_stream`
   - Waits 5 seconds
   - Continues monitoring

### Logging

All events logged to: `logs/stream-monitor.log`

Example log entries:
```
[2026-04-20 14:23:45] Stream Monitor started
[2026-04-20 14:23:50] Stream active: 12345
[2026-04-20 14:24:05] Stream active: 12345
[2026-04-20 14:24:20] Stream active: 12345
[2026-04-20 14:35:15] WARNING: FFmpeg process not found - stream appears to have stopped
[2026-04-20 14:35:15] Attempting to restart vartapravah_stream service...
[2026-04-20 14:35:17] SUCCESS: Streamer service restarted
```

---

## Configuration

### Change Check Interval

Edit the script and modify `CHECK_INTERVAL`:

**Linux/Mac (stream-monitor.sh):**
```bash
CHECK_INTERVAL=15  # Change from 15 to desired seconds
```

**Windows (stream-monitor.bat):**
```batch
set CHECK_INTERVAL=15  # Change from 15 to desired seconds
```

### Change Restart Delay

**Linux/Mac (stream-monitor.sh):**
```bash
RESTART_DELAY=5  # Wait 5 seconds before restart
```

**Windows (stream-monitor.bat):**
```batch
set RESTART_DELAY=5  # Wait 5 seconds before restart
```

---

## Deployment Scenarios

### Scenario 1: Single Server (Always Running)

```bash
# Add to /etc/systemd/system/vartapravah-monitor.service
[Unit]
Description=VartaPravah Stream Monitor
After=docker-compose.service

[Service]
Type=simple
WorkingDirectory=/path/to/vartapravah
ExecStart=/path/to/vartapravah/stream-monitor.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable vartapravah-monitor.service
sudo systemctl start vartapravah-monitor.service
```

### Scenario 2: Development (Manual Start)

```bash
# Start when needed
./stream-monitor.sh &

# Stop with Ctrl+C or kill
```

### Scenario 3: High Availability

Run TWO instances for redundancy:
```bash
# Instance 1: Primary monitor
./stream-monitor.sh > logs/monitor1.log 2>&1 &

# Instance 2: Backup monitor
./stream-monitor.sh > logs/monitor2.log 2>&1 &
```

### Scenario 4: Windows Scheduled Task

1. Open Task Scheduler
2. Create Basic Task
3. Name: "VartaPravah Stream Monitor"
4. Trigger: "At startup"
5. Action: Start program `stream-monitor.bat`
6. Set to run with highest privileges
7. Check "Run whether user is logged in or not"

---

## Monitoring the Monitor

### Check if Running

**Linux/Mac:**
```bash
ps aux | grep stream-monitor
```

**Windows:**
```cmd
tasklist | findstr stream-monitor
```

### View Live Logs

```bash
# Linux/Mac
tail -f logs/stream-monitor.log

# Windows (in PowerShell)
Get-Content logs/stream-monitor.log -Tail 20 -Wait
```

### Verify with Docker

```bash
# Check if streamer service is running
docker-compose ps vartapravah_stream

# View streamer logs
docker-compose logs streamer
```

---

## Troubleshooting

### Script Won't Start

**Linux/Mac:**
```bash
# Make sure it's executable
chmod +x stream-monitor.sh

# Check bash is available
which bash

# Try explicit bash
bash stream-monitor.sh
```

**Windows:**
```cmd
# Check PowerShell execution policy
Get-ExecutionPolicy

# Try running as Administrator
```

### Process Check Failing

If monitor keeps restarting service:
1. Check Docker is running: `docker ps`
2. Check service name: `docker-compose ps`
3. Check streamer logs: `docker-compose logs streamer`
4. Verify YOUTUBE_STREAM_KEY: `grep YOUTUBE_STREAM_KEY .env`

### Logs Directory Missing

```bash
# Create logs directory
mkdir -p logs

# Restart monitor
./stream-monitor.sh
```

### High False Positives

If seeing too many restarts:
1. Increase CHECK_INTERVAL
2. Check YouTube Stream Key validity
3. Check network connectivity
4. Check FFmpeg bitrate vs available bandwidth

---

## Comparison: Monitor vs Watchdog

| Feature | stream-monitor | Docker watchdog |
|---------|---|---|
| Process Type | FFmpeg-specific | Docker container |
| Check Interval | 15 sec (configurable) | 30 sec |
| Restarts | Service | Container |
| Logs | logs/stream-monitor.log | docker logs |
| Startup | Manual or scheduled | Automatic with compose |
| Dependencies | Docker only | Docker |
| Overhead | Minimal | Minimal |

**Recommendation:** Use both for maximum reliability!

---

## Best Practices

1. ✅ **Run in Background** - Use nohup or systemd service
2. ✅ **Monitor the Monitor** - Check logs daily
3. ✅ **Set Appropriate Interval** - Balance between responsiveness and CPU
4. ✅ **Use with Watchdog** - Don't rely on monitor alone
5. ✅ **Rotate Logs** - Archive old logs monthly
6. ✅ **Test Recovery** - Manually kill FFmpeg to test restart
7. ✅ **Monitor Logs** - Watch for patterns of failures
8. ✅ **Keep Updated** - Update YouTube Stream Key regularly

---

## Advanced Usage

### Custom Log Analysis

```bash
# Count restarts
grep "Attempting to restart" logs/stream-monitor.log | wc -l

# Show all restarts with timestamps
grep "WARNING\|SUCCESS" logs/stream-monitor.log

# Find error patterns
grep "ERROR" logs/stream-monitor.log | sort | uniq -c
```

### Systemd Integration

Create `/etc/systemd/system/vartapravah-monitor.service`:

```ini
[Unit]
Description=VartaPravah FFmpeg Stream Monitor
Documentation=file:///path/to/STREAM_MONITORING_GUIDE.md
After=docker.service docker-compose.service
Wants=docker-compose.service

[Service]
Type=simple
User=vartapravah
WorkingDirectory=/home/vartapravah/vartapravah
ExecStart=/home/vartapravah/vartapravah/stream-monitor.sh
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal
Environment="PATH=/usr/local/bin:/usr/bin"

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vartapravah-monitor.service
sudo systemctl start vartapravah-monitor.service
sudo systemctl status vartapravah-monitor.service
```

### Docker Container Monitor

Alternatively, run monitor in a container:

```yaml
  stream-monitor:
    image: alpine:latest
    container_name: vartapravah_stream_monitor
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./logs:/logs
    entrypoint: /bin/sh
    command: -c "
      while true; do
        if ! docker ps | grep -q vartapravah_stream; then
          echo '[ERROR] Stream service down' >> /logs/monitor.log;
          docker restart vartapravah_stream;
        fi;
        sleep 15;
      done
    "
    networks:
      - vartapravah_network
```

---

## Support & Logs

For issues, check:
1. `logs/stream-monitor.log` - Monitor activity
2. `docker-compose logs streamer` - FFmpeg output
3. `docker-compose logs app` - API errors
4. `.env` - YOUTUBE_STREAM_KEY validity

---

## Performance Impact

- **CPU**: < 1% (mostly sleeping)
- **Memory**: < 10MB
- **Disk**: ~100 bytes per check
- **Network**: Minimal (Docker socket only)

**Safe for production 24/7 operation**

---

## Updates & Customization

The script is simple and can be customized:
- Change check intervals
- Add email/Slack notifications
- Integrate with monitoring systems
- Add custom restart logic
- Modify log format

Feel free to modify for your needs!

---

**Happy Streaming! 📡**