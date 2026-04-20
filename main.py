import os
import logging
import threading
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from encoder.anchor_engine import AnchorEngine
from encoder.lipsync_engine import LipSyncEngine
from encoder.graphics_engine import GraphicsEngine
from encoder.scene_builder import SceneBuilder

load_dotenv()
VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VartaPravah AI Video Encoder")

# Initialize components
tts = TTSEngine()
anchor = AnchorEngine()
lipsync = LipSyncEngine()
scene_builder = SceneBuilder()
ticker = TickerSystem()
streamer = FFmpegStreamer()
scheduler = NewsScheduler(generate_news)

# Global state
news_queue = []
video_list = []
streaming = False
monitor_thread = None

class NewsInput(BaseModel):
    headline: str
    content: str
    category: str
    breaking: bool = False

def generate_news(news_data=None, custom_path=None):
    """Generate news video with full broadcast pipeline."""
    global news_queue, video_list
    if not news_data:
        # Use queued news or default
        if news_queue:
            news_data = news_queue.pop(0)
        else:
            logger.info("No news to generate")
            return

    try:
        # Get anchor
        anchor_data = anchor.get_next_anchor()

        # Generate TTS
        audio_path = tts.generate_audio(news_data['content'])

        # Generate lip sync video
        lip_sync_video = os.path.join(TEMP_DIR, 'lipsync.mp4')
        lipsync.generate_lip_sync(anchor_data['image'], audio_path, lip_sync_video)

        # Update ticker
        ticker_text = ticker.get_ticker_text(news_data['content'], news_data['category'])
        ticker.update_ticker(ticker_text)

        # Build scene
        final_video = custom_path or os.path.join(VIDEOS_DIR, f"news_{int(time.time())}.mp4")
        scene_builder.build_scene(lip_sync_video, news_data['headline'], ticker_text, news_data.get('breaking', False), final_video)

        # Add to playlist if not custom
        if not custom_path:
            video_list.append(final_video)
        logger.info(f"Broadcast news video generated: {final_video}")

        # If streaming, update stream
        if streaming:
            streamer.stop_stream()
            streamer.stream_to_youtube(final_video)

    except Exception as e:
        logger.error(f"Error generating broadcast news: {e}")

@app.post("/generate-news")
def api_generate_news(news: NewsInput):
    """API to generate news video."""
    news_queue.append(news.dict())
    generate_news()
    return {"status": "News generation started"}

@app.post("/start-stream")
def start_stream():
    """Start YouTube streaming."""
    global streaming, monitor_thread
    if streaming:
        raise HTTPException(status_code=400, detail="Already streaming")

    if not video_list:
        # Generate a default video or use fallback
        generate_news()

    streamer.loop_stream(video_list)
    streaming = True

    # Start monitor thread
    monitor_thread = threading.Thread(target=streamer.monitor_and_restart, args=(video_list,))
    monitor_thread.start()

    return {"status": "Streaming started"}

@app.post("/stop-stream")
def stop_stream():
    """Stop streaming."""
    global streaming
    streamer.stop_stream()
    streaming = False
    if monitor_thread:
        monitor_thread.join()
    return {"status": "Streaming stopped"}

@app.get("/status")
def get_status():
    """Get system status."""
    return {
        "streaming": streaming,
        "videos_count": len(video_list),
        "news_queue": len(news_queue)
    }

@app.on_event("startup")
def startup_event():
    """Start scheduler on startup."""
    logger.info("VartaPravah Broadcast System Starting...")
    scheduler.start_scheduler()
    
    # Create fallback video if not exists
    fallback_path = os.path.join(VIDEOS_DIR, 'fallback.mp4')
    if not os.path.exists(fallback_path):
        logger.info("Creating fallback video for failsafe streaming")
        default_news = {
            'headline': 'वार्ताप्रवाहमध्ये आपले स्वागत आहे',
            'content': 'नवीन बातम्या येत आहेत, कृपया थांबा.',
            'category': 'सामान्य',
            'breaking': False
        }
        try:
            generate_news(default_news, fallback_path)
            logger.info(f"Fallback video created at {fallback_path}")
        except Exception as e:
            logger.warning(f"Could not create fallback video: {e}")
            logger.info("Streamer will use existing fallback video or wait for content")

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown."""
    scheduler.stop_scheduler()
    if streaming:
        streamer.stop_stream()