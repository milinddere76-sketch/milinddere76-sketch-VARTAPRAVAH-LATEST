"""
VartaPravah News Rules Engine Integration Guide
Code snippets for integrating news validation into main.py
"""

# ============================================================================
# INTEGRATION STEP 1: Import the News Rules Engine
# ============================================================================

from encoder.news_rules_engine import (
    validate_and_process_news,
    NewsGenerationRules,
    NewsValidator
)


# ============================================================================
# INTEGRATION STEP 2: Update the generate_news Function
# ============================================================================

def generate_news(news_data=None, custom_path=None, bulletin_type=None, news_list=None):
    """
    Generate news video with full broadcast pipeline and rule enforcement.
    
    Args:
        news_data: Single news item dict (legacy)
        custom_path: Custom output path
        bulletin_type: Bulletin type (morning, afternoon, evening, prime_time, night)
        news_list: List of news items to validate and process
    """
    global news_queue, video_list
    
    # Step 1: Prepare news list
    if news_list:
        # Validate and process list with rules
        report = validate_and_process_news(news_list)
        
        if not report['is_valid']:
            logger.error(f"News validation failed: {report['errors']}")
            return {
                'status': 'error',
                'message': 'News validation failed',
                'errors': report['errors'],
                'warnings': report['warnings']
            }
        
        # Use processed news
        processed_news_list = report['processed_news']
        is_breaking = report['is_breaking']
        volume_category = report['volume_category']
        
        logger.info(
            f"Processed {report['input_count']} news items → "
            f"{len(processed_news_list)} items ({volume_category})"
        )
    else:
        # Fallback to single item or queue
        if news_data:
            processed_news_list = [news_data]
            is_breaking = news_data.get('breaking', False)
            volume_category = 'single'
        elif news_queue:
            processed_news_list = [news_queue.pop(0)]
            is_breaking = False
            volume_category = 'queued'
        else:
            logger.info("No news to generate")
            return {'status': 'no_data', 'message': 'No news items available'}
    
    # Step 2: Generate video for each news item
    try:
        generated_videos = []
        
        for idx, news in enumerate(processed_news_list):
            logger.info(f"Processing news {idx+1}/{len(processed_news_list)}")
            
            # Get anchor
            anchor_data = anchor.get_next_anchor()
            
            # Generate TTS
            audio_path = tts.generate_audio(news['content'])
            
            # Generate lip sync video
            lip_sync_video = os.path.join(TEMP_DIR, f'lipsync_{idx}.mp4')
            lipsync.generate_lip_sync(anchor_data['image'], audio_path, lip_sync_video)
            
            # Update ticker with breaking news indicator if needed
            ticker_prefix = "🔴 तातडीची बातमी: " if is_breaking else ""
            ticker_text = ticker.get_ticker_text(
                news['content'], 
                news.get('category', 'सामान्य')
            )
            ticker.update_ticker(ticker_text)
            
            # Build scene
            final_video = custom_path or os.path.join(
                VIDEOS_DIR, 
                f"news_{bulletin_type}_{volume_category}_{int(time.time())}_{idx}.mp4"
            )
            scene_builder.build_scene(
                lip_sync_video,
                news['headline'],
                ticker_text,
                is_breaking or news.get('breaking', False),
                final_video
            )
            
            generated_videos.append(final_video)
            logger.info(f"Generated video {idx+1}: {final_video}")
        
        # Step 3: Add to playlist
        if not custom_path:
            video_list.extend(generated_videos)
        
        # Step 4: Update stream if running
        if streaming:
            streamer.stop_stream()
            # Concatenate all videos
            final_playlist = os.path.join(VIDEOS_DIR, f"playlist_{int(time.time())}.mp4")
            streamer.concat_videos(generated_videos, final_playlist)
            streamer.stream_to_youtube(final_playlist)
        
        return {
            'status': 'success',
            'message': f'Generated {len(generated_videos)} news videos',
            'bulletin_type': bulletin_type,
            'volume_category': volume_category,
            'is_breaking': is_breaking,
            'videos': generated_videos,
            'total_items': len(processed_news_list)
        }
        
    except Exception as e:
        logger.error(f"Error generating news: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


# ============================================================================
# INTEGRATION STEP 3: New API Endpoints
# ============================================================================

@app.get("/news/rules")
def get_news_rules():
    """Get current news generation rules."""
    return NewsGenerationRules.get_rule_summary()


@app.post("/news/validate")
def validate_news(request: Dict):
    """
    Validate news before generation.
    
    Request body:
    {
        "news_list": [
            {
                "headline": "बातमी",
                "content": "विस्तृत विवरण...",
                "category": "सामान्य"
            },
            ...
        ]
    }
    """
    try:
        news_list = request.get('news_list', [])
        report = validate_and_process_news(news_list)
        return report
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/bulletin/generate-with-rules")
def generate_bulletin_with_rules(request: Dict):
    """
    Generate bulletin with full rule enforcement.
    
    Request body:
    {
        "news_list": [...],
        "bulletin_type": "evening"
    }
    """
    try:
        news_list = request.get('news_list', [])
        bulletin_type = request.get('bulletin_type', 'manual')
        
        result = generate_news(
            news_list=news_list,
            bulletin_type=bulletin_type
        )
        
        if result['status'] != 'success':
            raise HTTPException(status_code=400, detail=result.get('message'))
        
        return {
            'status': 'success',
            'bulletin': bulletin_type,
            'news_count': result['total_items'],
            'volume_category': result['volume_category'],
            'is_breaking': result['is_breaking'],
            'videos_generated': len(result['videos']),
            'message': result['message']
        }
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/news/categorize/{count}")
def categorize_news_volume(count: int):
    """
    Get volume category for a given news count.
    
    Example: GET /news/categorize/15
    """
    info = NewsGenerationRules.categorize_news_volume(count)
    return info


# ============================================================================
# INTEGRATION STEP 4: Update Bulletin Scheduler Integration
# ============================================================================

# In bulletin_scheduler usage:

from encoder.bulletin_scheduler import BulletinScheduler

def init_bulletin_scheduler_with_rules():
    """Initialize bulletin scheduler with rule enforcement."""
    
    def generate_bulletin_func(bulletin_type):
        """Wrapper for bulletin generation with rules."""
        # Queue news from API or database
        queued_news = fetch_news_for_bulletin(bulletin_type)  # Implement as needed
        
        if queued_news:
            # Generate with full rule enforcement
            result = generate_news(
                news_list=queued_news,
                bulletin_type=bulletin_type
            )
            return result
        else:
            logger.warning(f"No news queued for {bulletin_type} bulletin")
    
    scheduler = BulletinScheduler(generate_bulletin_func)
    scheduler.start_scheduler()
    return scheduler


# ============================================================================
# INTEGRATION STEP 5: Add to Startup Event
# ============================================================================

bulletin_scheduler = None

@app.on_event("startup")
def startup_event():
    """Start bulletin scheduler with rule enforcement."""
    global bulletin_scheduler
    
    logger.info("VartaPravah System Starting with News Rules Engine...")
    
    # Log rules summary
    rules = NewsGenerationRules.get_rule_summary()
    logger.info(f"News Rules: {rules['valid_range']} items per bulletin")
    for rule in rules['rules']:
        logger.info(f"  - {rule}")
    
    # Initialize bulletin scheduler
    bulletin_scheduler = init_bulletin_scheduler_with_rules()
    logger.info("Bulletin scheduler started with rule enforcement")


# ============================================================================
# INTEGRATION STEP 6: Example Usage
# ============================================================================

"""
Example 1: Validate news before generation
============================================

POST /news/validate
{
    "news_list": [
        {
            "headline": "नई नीति घोषणा",
            "content": "सरकार ने नई नीति की घोषणा की है...",
            "category": "राजनीति"
        },
        {
            "headline": "बाजार में उछाल",
            "content": "शेयर बाजार में तेजी देखी गई...",
            "category": "अर्थव्यवस्था"
        },
        ... (need minimum 5 items)
    ]
}

Response:
{
    "is_valid": true,
    "input_count": 15,
    "volume_category": "extended",
    "is_breaking": false,
    "bulletin_format": "extended_bulletin",
    "processed_news": [...]
}


Example 2: Generate with 25 items (Breaking News)
==================================================

POST /bulletin/generate-with-rules
{
    "news_list": [...],  // 25 items
    "bulletin_type": "evening"
}

Response:
{
    "status": "success",
    "bulletin": "evening",
    "news_count": 25,
    "volume_category": "breaking",
    "is_breaking": true,
    "videos_generated": 25,
    "message": "Breaking news bulletin generated"
}


Example 3: Automatic Daily Bulletins
=====================================

The bulletin scheduler automatically checks for queued news at:
- 05:00 AM: Morning bulletin
- 12:00 PM: Afternoon bulletin  
- 05:00 PM: Evening bulletin
- 09:00 PM: Prime Time bulletin
- 12:00 AM: Night bulletin

Each bulletin enforces minimum 5 items and maximum 25 items rules.
If 25 items found, breaking news mode activates automatically.
"""