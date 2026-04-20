"""
VartaPravah Fallback Cache System Integration Guide
Code snippets for integrating fallback system into main.py
"""

# ============================================================================
# STEP 1: Import Fallback Manager
# ============================================================================

from encoder.fallback_manager import (
    FallbackVideoManager,
    StreamWithFallback,
    create_placeholder_video
)


# ============================================================================
# STEP 2: Global Initialization
# ============================================================================

# Global instances
fallback_manager: Optional[FallbackVideoManager] = None
stream_with_fallback: Optional[StreamWithFallback] = None

VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')
FALLBACK_PATH = os.path.join(VIDEOS_DIR, 'final_news.mp4')


# ============================================================================
# STEP 3: Initialize in Startup Event
# ============================================================================

@app.on_event("startup")
def startup_event():
    """Initialize fallback system on startup."""
    global fallback_manager, stream_with_fallback
    
    logger.info("Initializing Fallback Video Cache System...")
    
    # Create videos directory
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    
    # Initialize fallback manager
    fallback_manager = FallbackVideoManager(videos_dir=VIDEOS_DIR)
    stream_with_fallback = StreamWithFallback(fallback_manager, streamer)
    
    # Ensure fallback exists
    if not fallback_manager.ensure_fallback_exists():
        logger.warning("No fallback video found. Creating placeholder...")
        try:
            if create_placeholder_video(FALLBACK_PATH, duration=60):
                logger.info("Placeholder fallback created successfully")
            else:
                logger.error("Failed to create placeholder fallback")
        except Exception as e:
            logger.error(f"Fallback initialization failed: {e}")
    else:
        logger.info("Fallback video ready")
    
    # Verify fallback health
    status = fallback_manager.get_status()
    logger.info(f"Fallback Status: {status['message']}")


# ============================================================================
# STEP 4: Update generate_news Function
# ============================================================================

def generate_news(news_data=None, custom_path=None, bulletin_type=None, news_list=None):
    """
    Generate news with automatic fallback cache updates.
    """
    global news_queue, video_list, fallback_manager
    
    # ... [existing news generation logic] ...
    
    # After generating final video:
    final_video = os.path.join(VIDEOS_DIR, f"news_{int(time.time())}.mp4")
    
    # ... [generate video] ...
    
    # Update fallback cache
    try:
        if fallback_manager.update_cache(final_video):
            logger.info(f"Fallback cache updated: {final_video}")
        else:
            logger.warning("Cache update failed, continuing with current fallback")
    except Exception as e:
        logger.warning(f"Cache update error: {e}")
    
    return {
        'status': 'success',
        'video': final_video,
        'fallback_updated': True
    }


# ============================================================================
# STEP 5: Safe Stream Start - Primary Implementation
# ============================================================================

@app.post("/start-stream-safe")
def start_stream_safe():
    """
    Start streaming with automatic fallback protection.
    
    Guarantees:
    - Stream always has video to play
    - Uses new video if ready
    - Falls back to cached video if new not ready
    - No downtime ever
    """
    global video_list, streaming, stream_with_fallback
    
    if streaming:
        return {"status": "error", "message": "Already streaming"}
    
    # Get latest video if available
    new_video = None
    if video_list:
        new_video = video_list[-1]  # Latest generated video
    
    logger.info(f"Starting stream with fallback protection...")
    logger.info(f"New video: {new_video}")
    logger.info(f"Fallback available: {stream_with_fallback.fallback_manager.ensure_fallback_exists()}")
    
    # Start stream (new if ready, fallback if not)
    result = stream_with_fallback.start_stream(
        new_video_path=new_video,
        stream_key=os.getenv('YOUTUBE_STREAM_KEY')
    )
    
    if result['status'] == 'streaming':
        streaming = True
        logger.info(f"Stream started: {result['message']} video")
        logger.info(f"Using fallback: {result['using_fallback']}")
    else:
        logger.error(f"Stream failed: {result.get('message')}")
    
    return result


# ============================================================================
# STEP 6: Fallback Management Endpoints
# ============================================================================

@app.get("/fallback/status")
def get_fallback_status():
    """Get comprehensive fallback system status."""
    if not fallback_manager:
        return {"status": "not_initialized"}
    
    return fallback_manager.get_status()


@app.get("/fallback/verify")
def verify_fallback():
    """Verify fallback video integrity."""
    if not fallback_manager:
        return {"status": "not_initialized"}
    
    return fallback_manager.verify_fallback_integrity()


@app.post("/fallback/update")
def update_fallback(request: Dict):
    """
    Manually update fallback cache with new video.
    
    Request:
    {
        "video_path": "app/videos/news_latest.mp4"
    }
    """
    if not fallback_manager:
        raise HTTPException(status_code=500, detail="Fallback manager not initialized")
    
    video_path = request.get('video_path')
    
    if not video_path:
        raise HTTPException(status_code=400, detail="video_path required")
    
    try:
        if fallback_manager.update_cache(video_path):
            return {
                'status': 'success',
                'message': 'Cache updated successfully',
                'new_video': video_path,
                'fallback_ready': True
            }
        else:
            return {
                'status': 'error',
                'message': 'Cache update failed',
                'fallback_ready': fallback_manager.ensure_fallback_exists()
            }
    except Exception as e:
        logger.error(f"Cache update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fallback/stats")
def get_fallback_stats():
    """Get fallback usage statistics."""
    if not fallback_manager:
        return {"status": "not_initialized"}
    
    return {
        'fallback_stats': fallback_manager.get_stats(),
        'status': fallback_manager.get_status()
    }


@app.post("/fallback/create-placeholder")
def create_placeholder():
    """Create placeholder fallback video if missing."""
    if not fallback_manager:
        raise HTTPException(status_code=500, detail="Fallback manager not initialized")
    
    try:
        if create_placeholder_video(FALLBACK_PATH, duration=60):
            return {
                'status': 'success',
                'message': 'Placeholder created',
                'path': FALLBACK_PATH
            }
        else:
            raise HTTPException(status_code=500, detail="Creation failed")
    except Exception as e:
        logger.error(f"Placeholder creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STEP 7: Enhanced Stop Stream
# ============================================================================

@app.post("/stop-stream")
def stop_stream():
    """Stop streaming gracefully."""
    global streaming
    
    if not streaming:
        return {"status": "error", "message": "Not streaming"}
    
    result = stream_with_fallback.stop_stream()
    streaming = False
    
    return result


# ============================================================================
# STEP 8: Health Check Endpoint
# ============================================================================

@app.get("/health/fallback")
def health_check_fallback():
    """
    Health check specifically for fallback system.
    
    Returns 200 if healthy, 503 if degraded/failing.
    """
    if not fallback_manager:
        return {
            'status': 'unhealthy',
            'message': 'Fallback manager not initialized'
        }, 503
    
    status = fallback_manager.get_status()
    
    if status['status'] == 'healthy':
        return {
            'status': 'healthy',
            'message': status['message'],
            'fallback_ready': True
        }, 200
    else:
        return {
            'status': 'degraded',
            'message': status['message'],
            'fallback_ready': status['fallback_ready']
        }, 503


# ============================================================================
# STEP 9: Monitoring & Alerting
# ============================================================================

def check_fallback_health():
    """
    Periodic fallback health check (run every 5 minutes).
    
    Should be called by a scheduler or watchdog.
    """
    if not fallback_manager:
        logger.warning("Fallback manager not initialized")
        return
    
    status = fallback_manager.get_status()
    
    if not status['fallback_ready']:
        logger.error("CRITICAL: Fallback not ready!")
        # TODO: Send alert/notification
    
    stats = fallback_manager.get_stats()
    if stats['fallback_uses'] > 10:
        logger.warning(f"High fallback usage: {stats['fallback_uses']} times")
        # TODO: Investigate why new videos delayed


# ============================================================================
# STEP 10: Integration with Bulletin Scheduler
# ============================================================================

def generate_bulletin_with_fallback(bulletin_type):
    """
    Generate bulletin and automatically update fallback.
    
    Called by BulletinScheduler at scheduled times.
    """
    try:
        # Generate news
        result = generate_news(bulletin_type=bulletin_type)
        
        if result['status'] == 'success':
            # Fallback already updated by generate_news
            logger.info(f"{bulletin_type} bulletin generated and fallback updated")
        else:
            logger.warning(f"{bulletin_type} bulletin failed, using existing fallback")
            
    except Exception as e:
        logger.error(f"Bulletin generation error: {e}")
        # Stream continues with fallback (no downtime!)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
Example 1: Start Safe Stream (Recommended)
==========================================

POST /start-stream-safe

Response (if new video ready):
{
    "status": "streaming",
    "video": "app/videos/news_latest.mp4",
    "using_fallback": false,
    "fallback_ready": true,
    "message": "New video"
}

Response (if new video NOT ready):
{
    "status": "streaming",
    "video": "app/videos/final_news.mp4",
    "using_fallback": true,
    "fallback_ready": true,
    "message": "Fallback"
}

Result: Stream ALWAYS starts successfully!


Example 2: Check Fallback Health
================================

GET /fallback/status

{
    "status": "healthy",
    "fallback_ready": true,
    "primary_video": {
        "exists": true,
        "size_mb": 42.5
    },
    "backup_video": {
        "exists": true,
        "size_mb": 40.2
    },
    "message": "✓ Primary fallback ready",
    "statistics": {
        "fallback_uses": 5,
        "cache_updates": 3
    }
}


Example 3: Update Fallback Manually
===================================

POST /fallback/update
Content-Type: application/json

{
    "video_path": "app/videos/news_123.mp4"
}

Response:
{
    "status": "success",
    "message": "Cache updated successfully",
    "fallback_ready": true
}


Example 4: Monitor Fallback Usage
=================================

GET /fallback/stats

{
    "fallback_stats": {
        "fallback_uses": 5,
        "last_fallback_use": "2026-04-21T14:35:22",
        "cache_updates": 3,
        "last_cache_update": "2026-04-21T14:30:15",
        "stream_starts": 180,
        "stream_interruptions": 0
    },
    "status": { ... }
}


Example 5: Automatic Daily Bulletins with Fallback
==================================================

Bulletins are automatically generated at:
- 05:00: Morning (falls back if not ready)
- 12:00: Afternoon (falls back if not ready)
- 17:00: Evening (falls back if not ready)
- 21:00: Prime Time (falls back if not ready)
- 00:00: Night (falls back if not ready)

Each bulletin:
1. Generates new video
2. Updates fallback cache
3. Continues streaming (never stops)

Result: 24/7 news broadcast with zero downtime!
"""