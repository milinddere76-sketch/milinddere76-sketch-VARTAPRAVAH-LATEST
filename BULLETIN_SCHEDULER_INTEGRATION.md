"""
VartaPravah - AI Video Encoder with Bulletin-Based Scheduling
Integration for bulletin scheduler - updated main.py snippet
"""

from encoder.bulletin_scheduler import BulletinScheduler

# Updated generate_news function to support bulletin_type parameter
def generate_news(news_data=None, custom_path=None, bulletin_type=None):
    """
    Generate news video with full broadcast pipeline.
    
    Args:
        news_data: News content dict, or None to generate placeholder
        custom_path: Custom output path
        bulletin_type: Bulletin type (morning, afternoon, evening, prime_time, night)
    """
    global news_queue, video_list
    
    if not news_data:
        # Use queued news or generate bulletin-appropriate placeholder
        if news_queue:
            news_data = news_queue.pop(0)
        else:
            # Generate bulletin-specific placeholder
            if bulletin_type:
                bulletin_info = BulletinScheduler.get_bulletin_info(bulletin_type)
                news_data = {
                    'headline': f"🔴 {bulletin_info['name']}",
                    'content': f"नवीन बातम्या येत आहेत. कृपया आमच्याबरोबर रहा।",
                    'category': bulletin_type,
                    'breaking': bulletin_type == "prime_time"
                }
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

        # Update ticker with bulletin info if available
        ticker_text = ticker.get_ticker_text(news_data['content'], news_data['category'])
        ticker.update_ticker(ticker_text)

        # Build scene
        final_video = custom_path or os.path.join(VIDEOS_DIR, f"news_{bulletin_type or 'manual'}_{int(time.time())}.mp4")
        scene_builder.build_scene(
            lip_sync_video, 
            news_data['headline'], 
            ticker_text, 
            news_data.get('breaking', False), 
            final_video
        )

        # Add to playlist if not custom
        if not custom_path:
            video_list.append(final_video)
        
        log_msg = f"Generated {bulletin_type or 'manual'} news video: {final_video}"
        logger.info(log_msg)

        # If streaming, update stream
        if streaming:
            streamer.stop_stream()
            streamer.stream_to_youtube(final_video)

    except Exception as e:
        logger.error(f"Error generating broadcast news: {e}")


# Updated scheduler initialization to use bulletin scheduler
# In startup_event:
def init_bulletin_scheduler():
    """Initialize bulletin-based scheduler."""
    # Wrap generate_news for bulletin scheduler
    def bulletin_generate_func(bulletin_type):
        generate_news(bulletin_type=bulletin_type)
    
    bulletin_scheduler = BulletinScheduler(bulletin_generate_func)
    bulletin_scheduler.start_scheduler()
    return bulletin_scheduler


# New API endpoints for bulletin scheduling
@app.get("/bulletin/schedule")
def get_bulletin_schedule():
    """Get the bulletin schedule."""
    return {
        "schedule": BulletinScheduler.BULLETIN_SCHEDULE,
        "bulletin_info": BulletinScheduler.BULLETIN_INFO
    }

@app.get("/bulletin/status")
def get_bulletin_status():
    """Get current bulletin status and next bulletin time."""
    return bulletin_scheduler.get_schedule_status()

@app.post("/bulletin/generate/{bulletin_type}")
def generate_bulletin(bulletin_type: str):
    """Generate a specific bulletin type immediately."""
    if bulletin_type not in BulletinScheduler.BULLETIN_SCHEDULE.values():
        raise HTTPException(
            status_code=400,
            detail=f"Invalid bulletin type. Must be one of: {', '.join(BulletinScheduler.BULLETIN_INFO.keys())}"
        )
    
    try:
        bulletin_scheduler.generate_now(bulletin_type=bulletin_type)
        return {
            "status": "success",
            "message": f"Generating {bulletin_type} bulletin",
            "bulletin_info": BulletinScheduler.get_bulletin_info(bulletin_type)
        }
    except Exception as e:
        logger.error(f"Error generating bulletin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bulletin/queue")
def queue_bulletin_news(news: NewsInput):
    """Queue news for next bulletin generation."""
    news_queue.append(news.dict())
    return {
        "status": "queued",
        "queue_length": len(news_queue),
        "next_bulletin": bulletin_scheduler.get_next_bulletin_time()
    }


# Updated startup with bulletin scheduler
@app.on_event("startup")
def startup_event():
    """Start bulletin scheduler on startup."""
    global bulletin_scheduler
    
    logger.info("VartaPravah Bulletin Broadcasting System Starting...")
    
    # Initialize bulletin scheduler
    bulletin_scheduler = init_bulletin_scheduler()
    logger.info("Bulletin scheduler initialized")
    
    # Log schedule
    schedule_status = bulletin_scheduler.get_schedule_status()
    logger.info(f"Next bulletin: {schedule_status['next_bulletin_time']} ({schedule_status['next_bulletin_type']})")
    
    # Create fallback video if not exists
    fallback_path = os.path.join(VIDEOS_DIR, 'fallback.mp4')
    if not os.path.exists(fallback_path):
        logger.info("Creating fallback video for failsafe streaming")
        try:
            generate_news(bulletin_type="morning", custom_path=fallback_path)
            logger.info(f"Fallback video created at {fallback_path}")
        except Exception as e:
            logger.warning(f"Could not create fallback video: {e}")


# Updated shutdown
@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown."""
    bulletin_scheduler.stop_scheduler()
    if streaming:
        streamer.stop_stream()


# Global bulletin_scheduler (initialize in startup)
bulletin_scheduler = None
