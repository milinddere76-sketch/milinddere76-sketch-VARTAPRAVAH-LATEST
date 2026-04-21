import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streaming state
streaming_state = {
    'is_streaming': False,
    'process': None,
    'video_path': None,
    'stream_key_status': False
}

# Initialize FastAPI app
app = FastAPI(
    title="VartaPravah - AI Video Encoder for Marathi YouTube",
    description="Production-ready AI video encoding system for 24/7 Marathi news broadcast",
    version="1.0.0"
)

# Configuration
YOUTUBE_STREAM_KEY = os.getenv('YOUTUBE_STREAM_KEY', 'your_stream_key_here')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_newsapi_key_here')
VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

# Create directories if they don't exist
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

logger.info("🎬 VartaPravah System Initialized")
logger.info(f"📁 Videos Directory: {VIDEOS_DIR}")
logger.info(f"📁 Temp Directory: {TEMP_DIR}")


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "status": "running",
        "name": "VartaPravah",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/status")
def status():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "VartaPravah AI Video Encoder",
        "youtube_stream_key_configured": YOUTUBE_STREAM_KEY != 'your_stream_key_here',
        "news_api_key_configured": NEWS_API_KEY != 'your_newsapi_key_here',
        "videos_dir": VIDEOS_DIR,
        "temp_dir": TEMP_DIR
    }

@app.get("/health")
def health():
    """Health check for Docker."""
    return {"status": "ok"}

@app.get("/docs")
def docs_redirect():
    """API documentation redirect."""
    return {
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


# ============================================================================
# TEST ENDPOINTS
# ============================================================================

@app.post("/test/echo")
def echo(message: str):
    """Echo test endpoint."""
    logger.info(f"Echo: {message}")
    return {
        "status": "success",
        "message": message,
        "service": "VartaPravah"
    }

@app.get("/test/config")
def test_config():
    """Test configuration endpoint."""
    return {
        "status": "success",
        "config": {
            "YOUTUBE_STREAM_KEY": "***" if YOUTUBE_STREAM_KEY != 'your_stream_key_here' else "NOT SET",
            "NEWS_API_KEY": "***" if NEWS_API_KEY != 'your_newsapi_key_here' else "NOT SET",
            "VIDEOS_DIR": VIDEOS_DIR,
            "TEMP_DIR": TEMP_DIR,
        }
    }

@app.get("/test/directories")
def test_directories():
    """Test directory creation."""
    return {
        "status": "success",
        "directories": {
            "videos_dir_exists": os.path.exists(VIDEOS_DIR),
            "temp_dir_exists": os.path.exists(TEMP_DIR),
            "videos_dir_path": VIDEOS_DIR,
            "temp_dir_path": TEMP_DIR,
        }
    }


# ============================================================================
# PLACEHOLDER ENDPOINTS (for future integration)
# ============================================================================

@app.get("/news/fetch")
def fetch_news():
    """Placeholder: Fetch news from multi-source aggregation."""
    return {
        "status": "placeholder",
        "message": "News fetcher endpoint - integrate with app.services.news_fetcher",
        "endpoint": "GET /news/fetch"
    }

@app.post("/bulletin/generate")
def generate_bulletin():
    """Placeholder: Generate news bulletin video."""
    return {
        "status": "placeholder",
        "message": "Bulletin generator endpoint - integrate with app.encoder.lipsync_engine",
        "endpoint": "POST /bulletin/generate"
    }

# ============================================================================
# STREAMING ENDPOINTS
# ============================================================================

def import_streaming_modules():
    """Lazy import streaming modules."""
    try:
        from app.encoder.ffmpeg_stream import FFmpegStreamer
        from app.encoder.placeholder_generator import PlaceholderGenerator
        return FFmpegStreamer, PlaceholderGenerator
    except ImportError as e:
        logger.warning(f"Could not import streaming modules: {e}")
        return None, None

@app.post("/fallback/create-placeholder")
def create_placeholder():
    """Create a placeholder/fallback video for streaming."""
    try:
        _, PlaceholderGenerator = import_streaming_modules()
        if PlaceholderGenerator is None:
            return {
                "status": "error",
                "message": "Streaming modules not available",
                "code": 500
            }
        
        logger.info("Creating placeholder video...")
        generator = PlaceholderGenerator()
        fallback_path = generator.create_fallback_video()
        
        return {
            "status": "success",
            "message": "Placeholder video created",
            "video_path": fallback_path,
            "duration": "60 seconds",
            "ready_to_stream": True
        }
    except Exception as e:
        logger.error(f"Error creating placeholder: {e}")
        return {
            "status": "error",
            "message": str(e),
            "code": 500
        }

@app.post("/stream/start")
def start_stream():
    """Start YouTube streaming with fallback video."""
    try:
        # Check if stream key is configured
        if YOUTUBE_STREAM_KEY == 'your_stream_key_here' or not YOUTUBE_STREAM_KEY:
            return {
                "status": "error",
                "message": "YouTube Stream Key not configured",
                "solution": "Set YOUTUBE_STREAM_KEY in .env file from YouTube Studio",
                "code": 400
            }
        
        # Check if already streaming
        if streaming_state['is_streaming']:
            return {
                "status": "already_streaming",
                "message": "Stream is already running",
                "video": streaming_state['video_path']
            }
        
        # Ensure fallback video exists
        fallback_path = os.path.join(VIDEOS_DIR, 'fallback.mp4')
        if not os.path.exists(fallback_path):
            logger.info("Fallback video not found, creating...")
            _, PlaceholderGenerator = import_streaming_modules()
            if PlaceholderGenerator:
                generator = PlaceholderGenerator()
                fallback_path = generator.create_fallback_video()
            else:
                return {
                    "status": "error",
                    "message": "Cannot create fallback video - streaming modules unavailable",
                    "code": 500
                }
        
        # Start streaming in background thread
        FFmpegStreamer, _ = import_streaming_modules()
        if FFmpegStreamer is None:
            return {
                "status": "error",
                "message": "FFmpegStreamer module not available",
                "code": 500
            }
        
        def stream_worker():
            try:
                logger.info(f"Starting stream with: {fallback_path}")
                streaming_state['video_path'] = fallback_path
                streaming_state['is_streaming'] = True
                
                streamer = FFmpegStreamer()
                # Stream video in loop
                streaming_state['process'] = streamer.stream_to_youtube(fallback_path)
                logger.info("Stream started successfully")
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                streaming_state['is_streaming'] = False
                streaming_state['process'] = None
        
        # Start in background thread
        thread = threading.Thread(target=stream_worker, daemon=True)
        thread.start()
        
        return {
            "status": "started",
            "message": "YouTube stream starting in background",
            "video": fallback_path,
            "stream_url": f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY[:10]}...",
            "next_check": "/stream/status"
        }
    except Exception as e:
        logger.error(f"Error starting stream: {e}")
        return {
            "status": "error",
            "message": str(e),
            "code": 500
        }

@app.post("/stream/stop")
def stop_stream():
    """Stop YouTube streaming."""
    try:
        if not streaming_state['is_streaming']:
            return {
                "status": "not_streaming",
                "message": "No active stream to stop"
            }
        
        if streaming_state['process']:
            streaming_state['process'].terminate()
            streaming_state['process'].wait(timeout=5)
        
        streaming_state['is_streaming'] = False
        streaming_state['process'] = None
        streaming_state['video_path'] = None
        logger.info("Stream stopped")
        
        return {
            "status": "stopped",
            "message": "YouTube stream stopped"
        }
    except Exception as e:
        logger.error(f"Error stopping stream: {e}")
        return {
            "status": "error",
            "message": str(e),
            "code": 500
        }

@app.get("/stream/status")
def stream_status():
    """Get current streaming status."""
    return {
        "status": "ok",
        "is_streaming": streaming_state['is_streaming'],
        "video_path": streaming_state['video_path'],
        "stream_key_configured": YOUTUBE_STREAM_KEY != 'your_stream_key_here' and bool(YOUTUBE_STREAM_KEY),
        "fallback_exists": os.path.exists(os.path.join(VIDEOS_DIR, 'fallback.mp4')),
        "available_videos": len([f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')]) if os.path.exists(VIDEOS_DIR) else 0
    }


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info("VartaPravah startup")
    logger.info(f"Videos Directory: {VIDEOS_DIR}")
    logger.info(f"Temp Directory: {TEMP_DIR}")
    
    # Check YouTube Stream Key
    if YOUTUBE_STREAM_KEY and YOUTUBE_STREAM_KEY != 'your_stream_key_here':
        streaming_state['stream_key_status'] = True
        logger.info("YouTube Stream Key configured")
    else:
        logger.warning("YouTube Stream Key NOT configured - streaming unavailable")
        logger.warning("To enable streaming, set YOUTUBE_STREAM_KEY in .env")
    
    # Create fallback video if it doesn't exist
    fallback_path = os.path.join(VIDEOS_DIR, 'fallback.mp4')
    if not os.path.exists(fallback_path):
        try:
            logger.info("Creating fallback video for failsafe streaming...")
            _, PlaceholderGenerator = import_streaming_modules()
            if PlaceholderGenerator:
                generator = PlaceholderGenerator()
                generator.create_fallback_video()
                logger.info("Fallback video created successfully")
            else:
                logger.warning("Could not create fallback video")
        except Exception as e:
            logger.warning(f"Failed to create fallback video: {e}")
    else:
        logger.info(f"Fallback video exists: {fallback_path}")
    
    logger.info("VartaPravah startup complete")
    logger.info("API Documentation: http://0.0.0.0:8000/docs")
    logger.info("Streaming Status: /stream/status")
    logger.info("Start Stream: POST /stream/start")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 VartaPravah shutting down")


# ============================================================================
# UVICORN STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )