#!/usr/bin/env python3
"""
VARTAPRAVAH - Complete Pipeline Demo
Shows the full flow: News → Marathi Script → TTS → Lip-sync → YouTube Stream
"""

import logging
import sys
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Execute the complete bulletin pipeline"""
    
    try:
        logger.info("=" * 70)
        logger.info("🧠 VARTAPRAVAH - COMPLETE BULLETIN PIPELINE")
        logger.info("=" * 70)
        
        # ==================================================
        # STEP 1: FETCH NEWS
        # ==================================================
        logger.info("\n📰 STEP 1: Fetching news from all sources...")
        logger.info("-" * 70)
        
        from news_fetcher import NewsFetcher
        
        fetcher = NewsFetcher()
        news_data = fetcher.fetch_all_news(limit=5)
        
        # Convert to simple format
        all_news = []
        for category, articles in news_data.items():
            for article in articles:
                all_news.append({
                    "title": article.title,
                    "description": article.description,
                    "source": article.source,
                    "category": category
                })
        
        logger.info(f"✅ Fetched {len(all_news)} news articles")
        for i, news in enumerate(all_news[:5], 1):
            logger.info(f"   {i}. {news['title'][:60]}... ({news['category']})")
        
        # ==================================================
        # STEP 2: GENERATE MARATHI SCRIPT
        # ==================================================
        logger.info("\n🧠 STEP 2: Generating Marathi script...")
        logger.info("-" * 70)
        
        from script_generator import generate_marathi_script
        
        # Choose bulletin type
        bulletin_type = "सकाळ"  # Morning - can be: मध्य, संध्या, प्राइम, रात्र
        script = generate_marathi_script(all_news[:5], bulletin_type)
        
        logger.info(f"✅ Generated Marathi script ({len(script)} characters)")
        logger.info("\n📄 SCRIPT PREVIEW:")
        logger.info("-" * 70)
        print(script[:500] + "...\n" if len(script) > 500 else script)
        
        # Save script to file
        script_file = "output/marathi_script.txt"
        os.makedirs("output", exist_ok=True)
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script)
        logger.info(f"✅ Script saved to: {script_file}")
        
        # ==================================================
        # STEP 3: CONVERT TO AUDIO (TTS)
        # ==================================================
        logger.info("\n🎤 STEP 3: Converting script to audio (TTS)...")
        logger.info("-" * 70)
        
        from tts_engine import generate_audio
        
        audio_path = "output/bulletin_audio.wav"
        audio_path = generate_audio(script, output_path=audio_path)
        logger.info(f"✅ Audio generated: {audio_path}")
        
        # ==================================================
        # STEP 4: CREATE LIP-SYNC VIDEO
        # ==================================================
        logger.info("\n👁️ STEP 4: Creating lip-synced video...")
        logger.info("-" * 70)
        
        from lipsync import run_lipsync
        
        video_path = "output/bulletin_video.mp4"
        video_path = run_lipsync(audio_path, output_video=video_path)
        logger.info(f"✅ Video created: {video_path}")
        
        # ==================================================
        # STEP 5: STREAM TO YOUTUBE (OPTIONAL)
        # ==================================================
        logger.info("\n📺 STEP 5: Stream to YouTube Live...")
        logger.info("-" * 70)
        
        # Get RTMP URL from environment or ask user
        rtmp_url = os.getenv("YOUTUBE_RTMP_URL", None)
        
        if rtmp_url:
            from streamer import stream_to_youtube
            
            logger.info(f"🌐 Streaming to: {rtmp_url[:50]}...")
            stream_to_youtube(video_path, rtmp_url)
            logger.info("✅ Streaming started!")
        else:
            logger.warning("⚠️ YouTube RTMP URL not configured")
            logger.warning("   Set YOUTUBE_RTMP_URL environment variable to enable streaming")
            logger.info("   To get RTMP URL:")
            logger.info("   1. Go to YouTube Studio > Go Live")
            logger.info("   2. Copy your RTMP URL")
            logger.info("   3. Set: export YOUTUBE_RTMP_URL='rtmp://...'")
        
        # ==================================================
        # COMPLETE
        # ==================================================
        logger.info("\n" + "=" * 70)
        logger.info("✅ COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
        logger.info("=" * 70)
        logger.info(f"📄 Script: {script_file}")
        logger.info(f"🎤 Audio:  {audio_path}")
        logger.info(f"📹 Video:  {video_path}")
        logger.info(f"⏱️  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 70 + "\n")
        
        return 0
    
    except Exception as e:
        logger.error(f"\n❌ Pipeline execution failed:")
        logger.error(f"   {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
