import logging
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from tts_engine import generate_audio
from lipsync import run_lipsync
from streamer import stream_to_youtube
from overlay import add_overlay
from news_fetcher import NewsFetcher, NewsArticle
from script_generator import ScriptGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="VARTAPRAVAH - AI News Avatar",
    description="Generate lip-synced AI news videos and stream to YouTube Live",
    version="1.0.0"
)

# Request/Response models
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to convert to speech")
    output_path: Optional[str] = Field(default="output/audio.wav", description="Path to save audio")

class TTSResponse(BaseModel):
    status: str
    audio_path: str
    timestamp: str
    message: str

class LipsyncRequest(BaseModel):
    audio_path: str = Field(..., description="Path to audio file")
    video_path: Optional[str] = Field(default="assets/anchor.mp4", description="Path to anchor video")
    output_video: Optional[str] = Field(default="output/lipsync.mp4", description="Path to save output")

class LipsyncResponse(BaseModel):
    status: str
    video_path: str
    timestamp: str
    message: str

class StreamRequest(BaseModel):
    video_path: str = Field(..., description="Path to video file")
    rtmp_url: str = Field(..., description="YouTube RTMP URL")
    headline: Optional[str] = Field(default="वार्ताप्रवाह LIVE", description="Lower-third headline text")
    add_overlay: Optional[bool] = Field(default=True, description="Add overlay (logo + headline)")

class StreamResponse(BaseModel):
    status: str
    timestamp: str
    message: str

class PipelineRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="News text")
    rtmp_url: Optional[str] = Field(default=None, description="YouTube RTMP (optional)")

class PipelineResponse(BaseModel):
    status: str
    audio_path: str
    video_path: str
    timestamp: str
    message: str

# News and Bulletin Models
class NewsRequest(BaseModel):
    limit: Optional[int] = Field(default=5, ge=1, le=10, description="Number of articles per category")
    categories: Optional[list] = Field(default=["India", "Maharashtra", "World"], description="News categories")

class BulletinRequest(BaseModel):
    max_bullets: Optional[int] = Field(default=5, ge=1, le=15, description="Max bullets in bulletin")
    rtmp_url: Optional[str] = Field(default=None, description="YouTube RTMP (optional)")
    use_google_translate: Optional[bool] = Field(default=False, description="Use Google Cloud Translation")

class BulletinResponse(BaseModel):
    status: str
    bulletin: dict
    narration_text: str
    timestamp: str
    message: str

# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the service is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# TTS Endpoint
@app.post("/tts", response_model=TTSResponse, tags=["Text-to-Speech"])
async def tts_endpoint(request: TTSRequest):
    """Convert text to speech audio"""
    try:
        logger.info(f"TTS request received: {request.text[:50]}...")
        audio_path = generate_audio(request.text, request.output_path)
        
        return TTSResponse(
            status="success",
            audio_path=audio_path,
            timestamp=datetime.now().isoformat(),
            message=f"✅ Audio generated successfully"
        )
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Lip-sync Endpoint
@app.post("/lipsync", response_model=LipsyncResponse, tags=["Lip-Sync"])
async def lipsync_endpoint(request: LipsyncRequest):
    """Generate lip-synced video from audio"""
    try:
        logger.info(f"Lip-sync request received for audio: {request.audio_path}")
        video_path = run_lipsync(request.audio_path, request.video_path, request.output_video)
        
        return LipsyncResponse(
            status="success",
            video_path=video_path,
            timestamp=datetime.now().isoformat(),
            message=f"✅ Lip-sync video generated successfully"
        )
    except Exception as e:
        logger.error(f"Lip-sync error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Stream Endpoint
@app.post("/stream", response_model=StreamResponse, tags=["Streaming"])
async def stream_endpoint(request: StreamRequest, background_tasks: BackgroundTasks):
    """Stream video to YouTube Live with optional overlays"""
    try:
        logger.info(f"Stream request received for: {request.video_path}")
        
        # Prepare video for streaming
        video_to_stream = request.video_path
        
        # Add overlays if requested
        if request.add_overlay:
            logger.info(f"Adding overlays with headline: {request.headline}")
            overlay_output = "output/streamed_with_overlay.mp4"
            if add_overlay(request.video_path, overlay_output, headline=request.headline):
                video_to_stream = overlay_output
                logger.info("✅ Overlays added successfully")
            else:
                logger.warning("⚠️ Overlay failed, streaming without overlay")
        
        # Run streaming in background
        background_tasks.add_task(stream_to_youtube, video_to_stream, request.rtmp_url)
        
        return StreamResponse(
            status="streaming",
            timestamp=datetime.now().isoformat(),
            message=f"✅ Streaming started in background"
        )
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Complete Pipeline Endpoint
@app.post("/pipeline", response_model=PipelineResponse, tags=["Pipeline"])
async def pipeline_endpoint(request: PipelineRequest):
    """Complete pipeline: TTS → Lip-sync → Stream (optional)"""
    try:
        logger.info(f"Pipeline request received: {request.text[:50]}...")
        
        # Step 1: Generate audio
        audio_path = generate_audio(request.text)
        logger.info(f"✅ Audio generated: {audio_path}")
        
        # Step 2: Generate lip-sync video
        video_path = run_lipsync(audio_path)
        logger.info(f"✅ Video lip-synced: {video_path}")
        
        # Step 3: Stream if RTMP provided
        if request.rtmp_url:
            stream_to_youtube(video_path, request.rtmp_url)
            logger.info(f"✅ Streaming started")
        
        return PipelineResponse(
            status="success",
            audio_path=audio_path,
            video_path=video_path,
            timestamp=datetime.now().isoformat(),
            message=f"✅ Complete pipeline executed successfully"
        )
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# News Fetcher Endpoints
@app.get("/news", tags=["News"])
async def fetch_news(limit: int = 5):
    """Fetch news from all categories (India, Maharashtra, World)"""
    try:
        logger.info(f"📰 News fetch request: {limit} articles per category")
        fetcher = NewsFetcher()
        news = fetcher.fetch_all_news(limit=limit)
        
        # Convert to dict format
        news_dict = {
            category: [article.dict() for article in articles]
            for category, articles in news.items()
        }
        
        total_articles = sum(len(v) for v in news_dict.values())
        
        return {
            "status": "success",
            "total_articles": total_articles,
            "categories": news_dict,
            "timestamp": datetime.now().isoformat(),
            "message": f"✅ Fetched {total_articles} news articles"
        }
    except Exception as e:
        logger.error(f"❌ News fetch error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Bulletin Generation Endpoint
@app.post("/bulletin", response_model=BulletinResponse, tags=["Bulletin"])
async def generate_bulletin(request: BulletinRequest):
    """Generate complete Marathi news bulletin"""
    try:
        logger.info(f"🧠 Bulletin generation request: {request.max_bullets} bullets")
        
        # Step 1: Fetch news
        fetcher = NewsFetcher()
        news = fetcher.fetch_all_news(limit=request.max_bullets)
        
        # Step 2: Generate Marathi script
        generator = ScriptGenerator(use_google_translate=request.use_google_translate)
        bulletin = generator.generate_bulletin_script(news, max_bullets=request.max_bullets)
        
        # Generate full narration for TTS
        narration = generator.generate_full_narration(bulletin)
        
        logger.info(f"✅ Bulletin generated: {bulletin['total_bullets']} bullets")
        
        return BulletinResponse(
            status="success",
            bulletin=bulletin,
            narration_text=narration,
            timestamp=datetime.now().isoformat(),
            message=f"✅ Bulletin generated with {bulletin['total_bullets']} bullets"
        )
    except Exception as e:
        logger.error(f"❌ Bulletin generation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Full Bulletin Pipeline Endpoint
@app.post("/bulletin-pipeline", tags=["Pipeline"])
async def bulletin_pipeline(request: BulletinRequest, background_tasks: BackgroundTasks):
    """
    Complete pipeline: Fetch News → Generate Marathi Script → TTS → Lip-sync → Stream
    This is the main "brain" of your channel!
    """
    try:
        logger.info(f"🧠💫 Starting complete bulletin pipeline...")
        
        # Step 1: Fetch news
        logger.info("Step 1/5: Fetching news...")
        fetcher = NewsFetcher()
        news = fetcher.fetch_all_news(limit=request.max_bullets)
        
        # Step 2: Generate Marathi script
        logger.info("Step 2/5: Generating Marathi script...")
        generator = ScriptGenerator(use_google_translate=request.use_google_translate)
        bulletin = generator.generate_bulletin_script(news, max_bullets=request.max_bullets)
        narration = generator.generate_full_narration(bulletin)
        
        # Step 3: Generate audio
        logger.info("Step 3/5: Converting to audio (TTS)...")
        audio_path = generate_audio(narration, output_path="output/bulletin_audio.wav")
        
        # Step 4: Generate lip-sync video
        logger.info("Step 4/5: Generating lip-sync video...")
        video_path = run_lipsync(audio_path, output_video="output/bulletin_video.mp4")
        
        # Step 5: Stream if RTMP provided (background task)
        if request.rtmp_url:
            logger.info("Step 5/5: Streaming to YouTube (background)...")
            background_tasks.add_task(stream_to_youtube, video_path, request.rtmp_url)
            streaming_status = "scheduled"
        else:
            logger.info("Step 5/5: (Skipped - no RTMP URL provided)")
            streaming_status = "skipped"
        
        logger.info(f"✅ Complete bulletin pipeline executed successfully!")
        
        return {
            "status": "success",
            "pipeline_steps": {
                "news_fetch": "✅ completed",
                "script_generation": "✅ completed",
                "tts": "✅ completed",
                "lipsync": "✅ completed",
                "streaming": f"✅ {streaming_status}"
            },
            "bulletin": bulletin,
            "narration_text": narration,
            "audio_path": audio_path,
            "video_path": video_path,
            "timestamp": datetime.now().isoformat(),
            "message": f"✅ Complete pipeline executed: {bulletin['total_bullets']} bullets → video → stream"
        }
    except Exception as e:
        logger.error(f"❌ Pipeline error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/info", tags=["Info"])
async def info():
    """Get service information"""
    return {
        "name": "VARTAPRAVAH",
        "description": "AI News Avatar Generator & YouTube Live Streamer - The Brain of Your Channel",
        "version": "1.0.0",
        "pipeline_flow": "APIs → Filter → Convert to Marathi → Generate Script → TTS → Lip-sync → YouTube Stream",
        "endpoints": {
            "health": "/health (GET)",
            "info": "/info (GET)",
            "tts": "/tts (POST)",
            "lipsync": "/lipsync (POST)",
            "stream": "/stream (POST)",
            "pipeline": "/pipeline (POST)",
            "news": "/news (GET)",
            "bulletin": "/bulletin (POST)",
            "bulletin-pipeline": "/bulletin-pipeline (POST) [🧠 MAIN BRAIN]",
            "docs": "/docs (Swagger UI)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
