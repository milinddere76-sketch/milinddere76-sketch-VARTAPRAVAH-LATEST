import os
import subprocess
import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Streaming configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
STREAM_TIMEOUT = 300  # 5 minutes


def stream_to_youtube(video_path: str, rtmp_url: str, max_retries: int = MAX_RETRIES) -> bool:
    """
    Stream video to YouTube Live using FFmpeg with auto-recovery.
    
    Features:
    - Automatic retry on failure (up to max_retries)
    - Network resilience with reconnect flags
    - Handles streaming interruptions gracefully
    
    Args:
        video_path: Path to input video file
        rtmp_url: YouTube RTMP URL with stream key
        max_retries: Maximum number of retry attempts
        
    Returns:
        True if streaming succeeded, False otherwise
        
    Raises:
        FileNotFoundError: If video file doesn't exist
        ValueError: If RTMP URL is invalid
    """
    # Validate input
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if not rtmp_url or not rtmp_url.startswith("rtmp"):
        raise ValueError(f"Invalid RTMP URL: {rtmp_url}")
    
    attempt = 0
    
    while attempt < max_retries:
        attempt += 1
        
        try:
            logger.info(f"📡 Starting YouTube Live stream (Attempt {attempt}/{max_retries})")
            logger.info(f"📡 Video: {video_path}")
            logger.info(f"📡 RTMP endpoint: {rtmp_url.split('/')[-1][:20]}...")
            
            # FFmpeg command with network resilience
            cmd = [
                "ffmpeg",
                "-re",
                "-reconnect", "1",              # Enable reconnection
                "-reconnect_streamed", "1",     # Reconnect for stream
                "-reconnect_delay_max", "5",    # Max 5 sec between reconnects
                "-i", video_path,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-maxrate", "3000k",
                "-bufsize", "6000k",
                "-pix_fmt", "yuv420p",
                "-g", "50",                     # Keyframe interval
                "-c:a", "aac",
                "-b:a", "128k",
                "-f", "flv",
                rtmp_url
            ]
            
            # Run streaming
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=STREAM_TIMEOUT
            )
            
            if result.returncode == 0:
                logger.info("✅ Stream completed successfully")
                return True
            else:
                stderr = result.stderr[-500:] if result.stderr else "Unknown error"
                logger.warning(f"⚠️ Stream ended (code {result.returncode}): {stderr}")
                
                if attempt < max_retries:
                    logger.info(f"⏳ Waiting {RETRY_DELAY}s before retry...")
                    time.sleep(RETRY_DELAY)
                    
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ Stream timeout (exceeded {STREAM_TIMEOUT}s)")
            
            if attempt < max_retries:
                logger.info(f"⏳ Waiting {RETRY_DELAY}s before retry...")
                time.sleep(RETRY_DELAY)
                
        except Exception as e:
            logger.error(f"❌ Stream error: {str(e)}")
            
            if attempt < max_retries:
                logger.info(f"⏳ Waiting {RETRY_DELAY}s before retry...")
                time.sleep(RETRY_DELAY)
    
    logger.error(f"❌ Streaming failed after {max_retries} attempts")
    return False


def stream_with_loop(
    video_path: str,
    rtmp_url: str,
    loop_count: int = -1
) -> bool:
    """
    Stream video in loop mode for continuous playback.
    
    Args:
        video_path: Path to input video file
        rtmp_url: YouTube RTMP URL with stream key
        loop_count: Number of loops (-1 for infinite)
        
    Returns:
        True if streaming succeeded
    """
    try:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        logger.info(f"📡 Starting loop stream (count: {loop_count if loop_count > 0 else 'infinite'})")
        
        cmd = [
            "ffmpeg",
            "-re",
            "-reconnect", "1",
            "-reconnect_streamed", "1",
            "-reconnect_delay_max", "5",
            "-stream_loop", str(loop_count),
            "-i", video_path,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-maxrate", "3000k",
            "-bufsize", "6000k",
            "-pix_fmt", "yuv420p",
            "-g", "50",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "flv",
            rtmp_url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=STREAM_TIMEOUT
        )
        
        if result.returncode == 0:
            logger.info("✅ Loop stream completed")
            return True
        else:
            logger.error(f"❌ Loop stream failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Loop stream error: {str(e)}")
        return False
