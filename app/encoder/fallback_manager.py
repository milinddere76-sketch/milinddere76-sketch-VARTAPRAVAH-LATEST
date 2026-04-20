"""
VartaPravah Fallback Video Cache System
Ensures 24/7 streaming without downtime by managing fallback videos
"""

import os
import shutil
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class FallbackVideoManager:
    """
    Manages fallback videos to prevent stream crashes.
    
    Strategy:
    - Always keep /videos/final_news.mp4 as primary fallback
    - If new video not ready: stream old video (no downtime)
    - Automatic cache update when new video available
    """
    
    def __init__(self, videos_dir: str = "app/videos"):
        """
        Initialize fallback manager.
        
        Args:
            videos_dir: Path to videos directory
        """
        self.videos_dir = videos_dir
        self.fallback_path = os.path.join(videos_dir, "final_news.mp4")
        self.backup_path = os.path.join(videos_dir, "final_news_backup.mp4")
        self.temp_path = os.path.join(videos_dir, "final_news_temp.mp4")
        
        # Create videos directory if needed
        os.makedirs(videos_dir, exist_ok=True)
        
        # Statistics
        self.stats = {
            'fallback_uses': 0,
            'last_fallback_use': None,
            'cache_updates': 0,
            'last_cache_update': None,
            'stream_starts': 0,
            'stream_interruptions': 0
        }
        
        logger.info(f"Fallback Video Manager initialized")
        logger.info(f"Primary fallback: {self.fallback_path}")
        logger.info(f"Backup fallback: {self.backup_path}")
    
    def ensure_fallback_exists(self) -> bool:
        """
        Ensure fallback video exists.
        
        Returns:
            True if fallback ready, False if missing
        """
        if os.path.exists(self.fallback_path):
            size_mb = os.path.getsize(self.fallback_path) / (1024 * 1024)
            logger.info(f"Fallback video ready: {size_mb:.1f} MB")
            return True
        elif os.path.exists(self.backup_path):
            logger.warning("Primary fallback missing. Restoring from backup...")
            try:
                shutil.copy2(self.backup_path, self.fallback_path)
                logger.info("Backup restored successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to restore from backup: {e}")
                return False
        else:
            logger.error("No fallback video available!")
            return False
    
    def update_cache(self, new_video_path: str) -> bool:
        """
        Update fallback cache with new video.
        
        Args:
            new_video_path: Path to new video file
            
        Returns:
            True if successful, False if failed
        """
        if not os.path.exists(new_video_path):
            logger.error(f"New video not found: {new_video_path}")
            return False
        
        try:
            # Get new video size
            new_size = os.path.getsize(new_video_path) / (1024 * 1024)
            
            # Step 1: Backup current fallback if exists
            if os.path.exists(self.fallback_path):
                try:
                    shutil.copy2(self.fallback_path, self.backup_path)
                    logger.info("Current fallback backed up")
                except Exception as e:
                    logger.warning(f"Backup failed: {e}")
            
            # Step 2: Copy new video to temp first (atomic operation)
            shutil.copy2(new_video_path, self.temp_path)
            logger.info(f"Copied new video to temp ({new_size:.1f} MB)")
            
            # Step 3: Verify temp file is valid
            if not os.path.exists(self.temp_path):
                logger.error("Temp copy verification failed")
                return False
            
            temp_size = os.path.getsize(self.temp_path)
            if temp_size != os.path.getsize(new_video_path):
                logger.error("Temp copy size mismatch")
                os.remove(self.temp_path)
                return False
            
            # Step 4: Atomic move to fallback
            shutil.move(self.temp_path, self.fallback_path)
            logger.info(f"Cache updated successfully ({new_size:.1f} MB)")
            
            # Update stats
            self.stats['cache_updates'] += 1
            self.stats['last_cache_update'] = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            logger.error(f"Cache update failed: {e}")
            # Cleanup temp if exists
            if os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except:
                    pass
            return False
    
    def get_stream_video(self, new_video_path: Optional[str] = None) -> Optional[str]:
        """
        Get video to stream - new if ready, fallback if not.
        
        Strategy:
        - If new_video_path provided and exists: use it and update cache
        - Else: use fallback (ensures no downtime)
        
        Args:
            new_video_path: Path to new video if available
            
        Returns:
            Path to video to stream, or None if no video available
        """
        # Check if new video is ready
        if new_video_path and os.path.exists(new_video_path):
            try:
                # Verify new video is complete and not being written
                file_size = os.path.getsize(new_video_path)
                time.sleep(0.1)  # Small delay to ensure write complete
                file_size_verify = os.path.getsize(new_video_path)
                
                if file_size == file_size_verify and file_size > 0:
                    logger.info(f"New video ready: {new_video_path}")
                    # Update cache in background
                    self._async_cache_update(new_video_path)
                    return new_video_path
            except Exception as e:
                logger.warning(f"New video validation failed: {e}")
        
        # New video not ready - use fallback
        if self.ensure_fallback_exists():
            self.stats['fallback_uses'] += 1
            self.stats['last_fallback_use'] = datetime.now().isoformat()
            
            if new_video_path:
                logger.warning(
                    f"New video not ready. Streaming fallback instead. "
                    f"(Expected: {new_video_path})"
                )
            else:
                logger.info("No new video. Streaming fallback.")
            
            return self.fallback_path
        
        # No video available
        logger.error("No video available for streaming!")
        return None
    
    def _async_cache_update(self, new_video_path: str):
        """
        Update cache asynchronously (non-blocking).
        
        Should be called in a background thread.
        """
        try:
            logger.info("Updating cache in background...")
            if self.update_cache(new_video_path):
                logger.info("Cache update completed")
            else:
                logger.warning("Cache update failed, continuing with current fallback")
        except Exception as e:
            logger.error(f"Async cache update error: {e}")
    
    def verify_fallback_integrity(self) -> Dict:
        """
        Verify fallback video integrity.
        
        Returns:
            {
                'primary_exists': bool,
                'primary_size_mb': float,
                'backup_exists': bool,
                'backup_size_mb': float,
                'is_healthy': bool,
                'status': str
            }
        """
        result = {
            'primary_exists': os.path.exists(self.fallback_path),
            'primary_size_mb': 0,
            'backup_exists': os.path.exists(self.backup_path),
            'backup_size_mb': 0,
            'is_healthy': False,
            'status': 'unknown'
        }
        
        if result['primary_exists']:
            result['primary_size_mb'] = os.path.getsize(self.fallback_path) / (1024 * 1024)
        
        if result['backup_exists']:
            result['backup_size_mb'] = os.path.getsize(self.backup_path) / (1024 * 1024)
        
        # Health check
        if result['primary_exists'] and result['primary_size_mb'] > 0:
            result['is_healthy'] = True
            result['status'] = '✓ Primary fallback ready'
        elif result['backup_exists'] and result['backup_size_mb'] > 0:
            result['is_healthy'] = True
            result['status'] = '⚠ Primary missing, backup available'
        else:
            result['is_healthy'] = False
            result['status'] = '✗ No fallback available'
        
        return result
    
    def get_stats(self) -> Dict:
        """Get statistics on fallback usage."""
        return {
            'fallback_uses': self.stats['fallback_uses'],
            'last_fallback_use': self.stats['last_fallback_use'],
            'cache_updates': self.stats['cache_updates'],
            'last_cache_update': self.stats['last_cache_update'],
            'stream_starts': self.stats['stream_starts'],
            'stream_interruptions': self.stats['stream_interruptions']
        }
    
    def get_status(self) -> Dict:
        """Get complete status report."""
        integrity = self.verify_fallback_integrity()
        stats = self.get_stats()
        
        return {
            'status': 'healthy' if integrity['is_healthy'] else 'degraded',
            'fallback_ready': integrity['primary_exists'],
            'primary_video': {
                'exists': integrity['primary_exists'],
                'size_mb': integrity['primary_size_mb'],
                'path': self.fallback_path
            },
            'backup_video': {
                'exists': integrity['backup_exists'],
                'size_mb': integrity['backup_size_mb'],
                'path': self.backup_path
            },
            'message': integrity['status'],
            'statistics': stats
        }


class StreamWithFallback:
    """
    Stream wrapper that handles fallback automatically.
    
    Ensures stream never stops due to missing video.
    """
    
    def __init__(self, fallback_manager: FallbackVideoManager, streamer):
        """
        Initialize stream wrapper.
        
        Args:
            fallback_manager: FallbackVideoManager instance
            streamer: FFmpeg streamer instance
        """
        self.fallback_manager = fallback_manager
        self.streamer = streamer
        self.streaming = False
        self.current_video = None
    
    def start_stream(self, new_video_path: Optional[str] = None, 
                    stream_key: str = None) -> Dict:
        """
        Start streaming with automatic fallback handling.
        
        Args:
            new_video_path: Path to new video if available
            stream_key: YouTube RTMP stream key
            
        Returns:
            Status dict with streaming result
        """
        # Get video to stream (new or fallback)
        video_to_stream = self.fallback_manager.get_stream_video(new_video_path)
        
        if not video_to_stream:
            return {
                'status': 'error',
                'message': 'No video available for streaming',
                'using_fallback': False
            }
        
        # Determine if using fallback
        using_fallback = (video_to_stream == self.fallback_manager.fallback_path)
        
        try:
            # Start streaming
            if stream_key:
                self.streamer.stream_to_youtube(video_to_stream, stream_key)
            else:
                self.streamer.stream_to_youtube(video_to_stream)
            
            self.streaming = True
            self.current_video = video_to_stream
            
            return {
                'status': 'streaming',
                'video': video_to_stream,
                'using_fallback': using_fallback,
                'fallback_ready': self.fallback_manager.ensure_fallback_exists(),
                'message': 'Fallback' if using_fallback else 'New video'
            }
            
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'using_fallback': using_fallback
            }
    
    def stop_stream(self):
        """Stop streaming."""
        try:
            self.streamer.stop_stream()
            self.streaming = False
            return {'status': 'stopped'}
        except Exception as e:
            logger.error(f"Stop failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def ensure_always_streaming(self, new_video_path: Optional[str] = None):
        """
        Ensure stream is always running.
        
        If stream interrupted, automatically restart with fallback.
        """
        if not self.streaming:
            logger.warning("Stream interrupted! Restarting with fallback...")
            return self.start_stream(new_video_path)
        
        return {'status': 'streaming', 'message': 'Stream active'}
    
    def get_fallback_status(self) -> Dict:
        """Get fallback system status."""
        return self.fallback_manager.get_status()


def create_placeholder_video(output_path: str, duration: int = 10) -> bool:
    """
    Create a simple placeholder video for fallback.
    
    Args:
        output_path: Where to save video
        duration: Video duration in seconds
        
    Returns:
        True if successful
    """
    import subprocess
    
    try:
        logger.info(f"Creating placeholder video: {output_path}")
        
        # Create a simple color video with text
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=blue:s=1920x1080:d={duration}',
            '-f', 'lavfi',
            '-i', f'sine=f=1000:d={duration}',
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"Placeholder video created ({size_mb:.1f} MB)")
            return True
        else:
            logger.error(f"Placeholder creation failed: {result.stderr.decode()}")
            return False
            
    except Exception as e:
        logger.error(f"Placeholder video creation error: {e}")
        return False
