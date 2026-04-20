import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.post("/stream/start")
def start_stream():
    """Placeholder: Start YouTube streaming."""
    return {
        "status": "placeholder",
        "message": "Stream controller endpoint - integrate with app.encoder.ffmpeg_stream",
        "endpoint": "POST /stream/start"
    }

@app.get("/stream/status")
def stream_status():
    """Placeholder: Get stream status."""
    return {
        "status": "placeholder",
        "streaming": False,
        "message": "Stream status endpoint - integrate with app.encoder.ffmpeg_stream"
    }


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info("✅ VartaPravah startup complete")
    logger.info("📚 API Documentation available at: /docs")
    logger.info("🎬 Ready for broadcast generation")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 VartaPravah shutting down")