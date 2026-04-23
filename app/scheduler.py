#!/usr/bin/env python3
"""
VARTAPRAVAH - TV Scheduler Engine
24×7 automated bulletin scheduling with promo loops and breaking news
"""

import logging
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


# ============================================================================
# BULLETIN SCHEDULE (Fixed Time Slots)
# ============================================================================

BULLETIN_SCHEDULE = [
    ("05:00", "सकाळ", "Morning"),
    ("12:00", "दुपार", "Afternoon"),
    ("17:00", "संध्याकाळ", "Evening"),
    ("20:00", "प्राइम टाइम", "Prime Time"),
    ("23:00", "रात्री", "Night"),
]

# Configuration
MAX_NEWS_PER_BULLETIN = 25
BREAKING_NEWS_LIMIT = 5
PROMO_INTERVAL = 300  # 5 minutes in seconds
LOOP_DELAY = 10  # Delay between loops (for testing, increase for production)

PROMO_VIDEO = "assets/promo.mp4"
DEFAULT_RTMP = os.getenv("YOUTUBE_RTMP_URL", "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY")


# ============================================================================
# NEWS QUEUE MANAGER
# ============================================================================

class NewsQueue:
    """Manages news articles and breaking news queue"""
    
    def __init__(self):
        self.main_news: List[Dict] = []
        self.breaking_news: List[Dict] = []
        self.processed_indices: set = set()
    
    def load_news(self, news_list: List[Dict]):
        """Load and split news into main and breaking"""
        total = len(news_list)
        
        if total > MAX_NEWS_PER_BULLETIN:
            logger.info(f"📊 News overflow: {total} articles")
            logger.info(f"   Main bulletin: {MAX_NEWS_PER_BULLETIN} articles")
            logger.info(f"   Breaking news: {total - MAX_NEWS_PER_BULLETIN} articles")
            
            self.main_news = news_list[:MAX_NEWS_PER_BULLETIN]
            self.breaking_news = news_list[MAX_NEWS_PER_BULLETIN:]
        else:
            self.main_news = news_list
            self.breaking_news = []
        
        self.processed_indices = set()
        logger.info(f"✅ Loaded {len(self.main_news)} main + {len(self.breaking_news)} breaking")
    
    def get_next_news(self) -> Optional[Dict]:
        """Get next unprocessed news article"""
        for i, article in enumerate(self.main_news):
            if i not in self.processed_indices:
                self.processed_indices.add(i)
                return article
        return None
    
    def has_unprocessed(self) -> bool:
        """Check if there are unprocessed articles"""
        return len(self.processed_indices) < len(self.main_news)
    
    def reset(self):
        """Reset processed indices for looping"""
        self.processed_indices = set()
    
    def get_breaking_news(self, limit: int = BREAKING_NEWS_LIMIT) -> List[Dict]:
        """Get breaking news articles"""
        return self.breaking_news[:limit]


# ============================================================================
# BULLETIN MANAGER
# ============================================================================

class BulletinManager:
    """Manages bulletin timing and switching"""
    
    def __init__(self):
        self.current_bulletin = None
        self.current_time_slot = None
    
    def get_current_bulletin(self) -> Tuple[str, str, str]:
        """
        Get current bulletin based on time
        Returns: (time_slot, marathi_name, english_name)
        """
        now = datetime.now().strftime("%H:%M")
        
        # Find current bulletin (most recent one that has passed)
        current = BULLETIN_SCHEDULE[0]  # Default to first
        
        for time_slot, marathi_name, english_name in BULLETIN_SCHEDULE:
            if now >= time_slot:
                current = (time_slot, marathi_name, english_name)
        
        return current
    
    def get_next_bulletin_time(self) -> datetime:
        """Get time until next bulletin"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Find next bulletin
        for time_slot, _, _ in BULLETIN_SCHEDULE:
            if current_time < time_slot:
                time_parts = time_slot.split(":")
                next_bulletin = now.replace(hour=int(time_parts[0]), minute=int(time_parts[1]), second=0)
                return next_bulletin
        
        # If we're past all bulletins today, next is tomorrow morning
        next_bulletin = (now + timedelta(days=1)).replace(hour=5, minute=0, second=0)
        return next_bulletin
    
    def seconds_until_next(self) -> int:
        """Seconds until next bulletin"""
        next_time = self.get_next_bulletin_time()
        now = datetime.now()
        delta = (next_time - now).total_seconds()
        return int(max(delta, 0))


# ============================================================================
# TV ENGINE
# ============================================================================

class TVEngine:
    """Main TV engine for 24×7 streaming"""
    
    def __init__(self, rtmp_url: str = DEFAULT_RTMP):
        self.rtmp_url = rtmp_url
        self.news_queue = NewsQueue()
        self.bulletin_manager = BulletinManager()
        self.is_running = False
        self.last_news_fetch = None
    
    def fetch_and_process_news(self):
        """Fetch news and process into queues"""
        try:
            from news_fetcher import NewsFetcher
            
            logger.info("📰 Fetching news from all sources...")
            fetcher = NewsFetcher()
            news_dict = fetcher.fetch_all_news(limit=15)
            
            # Flatten news from all categories
            all_news = []
            for category, articles in news_dict.items():
                for article in articles:
                    all_news.append({
                        'title': article.title,
                        'description': article.description or '',
                        'source': article.source,
                        'category': category
                    })
            
            self.news_queue.load_news(all_news)
            self.last_news_fetch = datetime.now()
            
            return True
        
        except Exception as e:
            logger.error(f"❌ News fetch failed: {str(e)}")
            return False
    
    def generate_script(self, news_article: Dict, bulletin_type: str) -> str:
        """Generate Marathi script for news article"""
        try:
            from script_generator import generate_marathi_script
            
            script = generate_marathi_script([news_article], bulletin_type)
            return script
        
        except Exception as e:
            logger.error(f"❌ Script generation failed: {str(e)}")
            return ""
    
    def generate_audio(self, script: str) -> Optional[str]:
        """Generate audio from script"""
        try:
            from tts_engine import generate_audio
            
            audio_path = generate_audio(script, output_path="output/story_audio.wav")
            return audio_path
        
        except Exception as e:
            logger.error(f"❌ Audio generation failed: {str(e)}")
            return None
    
    def generate_video(self, audio_path: str) -> Optional[str]:
        """Generate lip-sync video from audio"""
        try:
            from lipsync import run_lipsync
            
            video_path = run_lipsync(audio_path, output_video="output/story_video.mp4")
            return video_path
        
        except Exception as e:
            logger.error(f"❌ Video generation failed: {str(e)}")
            return None
    
    def stream_video(self, video_path: str, headline: str = ""):
        """Stream video to YouTube with overlays"""
        try:
            from streamer import stream_to_youtube
            from overlay import add_overlay
            
            # Step 4a: Add overlays
            logger.info("Step 4a/4b: Adding overlays...")
            overlay_output = "output/final_with_overlay.mp4"
            
            overlay_headline = headline or "वार्ताप्रवाह LIVE"
            if add_overlay(video_path, overlay_output, headline=overlay_headline):
                logger.info("✅ Overlay added")
                final_video = overlay_output
            else:
                logger.warning("⚠️ Overlay failed, streaming without overlay")
                final_video = video_path
            
            # Step 4b: Stream to YouTube
            logger.info("Step 4b/4b: Streaming to YouTube...")
            logger.info(f"📺 Streaming: {final_video}")
            success = stream_to_youtube(final_video, self.rtmp_url)
            
            return success
        
        except Exception as e:
            logger.error(f"❌ Streaming failed: {str(e)}")
            return False
    
    def play_promo(self):
        """Play promo video"""
        if not os.path.exists(PROMO_VIDEO):
            logger.warning(f"⚠️ Promo video not found: {PROMO_VIDEO}")
            return False
        
        try:
            logger.info("📢 Playing promo video...")
            # Use ffmpeg to stream promo
            cmd = f"ffmpeg -re -i {PROMO_VIDEO} -f null - 2>/dev/null"
            os.system(cmd)
            return True
        
        except Exception as e:
            logger.error(f"❌ Promo playback failed: {str(e)}")
            return False
    
    def process_story(self, news_article: Dict, bulletin_type: str):
        """Process and stream a single story"""
        logger.info(f"\n{'='*70}")
        logger.info(f"📖 Processing story: {news_article['title'][:60]}...")
        logger.info(f"    Category: {news_article.get('category', 'Unknown')}")
        logger.info(f"    Source: {news_article.get('source', 'Unknown')}")
        
        # Step 1: Generate script
        logger.info("Step 1/4: Generating Marathi script...")
        script = self.generate_script(news_article, bulletin_type)
        if not script:
            logger.error("❌ Script generation failed, skipping")
            return False
        
        # Step 2: Generate audio
        logger.info("Step 2/4: Converting to audio...")
        audio_path = self.generate_audio(script)
        if not audio_path:
            logger.error("❌ Audio generation failed, skipping")
            return False
        
        # Step 3: Generate video
        logger.info("Step 3/4: Creating lip-sync video...")
        video_path = self.generate_video(audio_path)
        if not video_path:
            logger.error("❌ Video generation failed, skipping")
            return False
        
        # Step 4: Stream with overlays
        logger.info("Step 4/4: Streaming to YouTube with overlays...")
        headline = news_article.get('title', '')[:60]  # Truncate to 60 chars for display
        success = self.stream_video(video_path, headline=headline)
        
        if success:
            logger.info(f"✅ Story streamed successfully")
        else:
            logger.error(f"❌ Streaming failed")
        
        return success
    
    def run_bulletin(self):
        """Run current bulletin"""
        time_slot, bulletin_marathi, bulletin_english = self.bulletin_manager.get_current_bulletin()
        
        logger.info("\n" + "=" * 70)
        logger.info(f"📺 STARTING BULLETIN: {bulletin_marathi} ({bulletin_english})")
        logger.info(f"🕒 Time Slot: {time_slot}")
        logger.info("=" * 70)
        
        # Fetch news
        if not self.fetch_and_process_news():
            logger.error("❌ Failed to fetch news, retrying...")
            time.sleep(5)
            return
        
        # Process all news with promos
        story_count = 0
        while self.news_queue.has_unprocessed():
            news = self.news_queue.get_next_news()
            if not news:
                break
            
            story_count += 1
            logger.info(f"\n📍 Story {story_count}/{len(self.news_queue.main_news)}")
            
            # Process story
            self.process_story(news, bulletin_marathi)
            
            # Play promo after each story (optional)
            if story_count % 5 == 0:
                logger.info("⏸️ Promo break...")
                self.play_promo()
        
        # Handle breaking news
        breaking = self.news_queue.get_breaking_news()
        if breaking:
            logger.info(f"\n🚨 BREAKING NEWS DETECTED: {len(breaking)} articles")
            for i, b_news in enumerate(breaking, 1):
                logger.info(f"\n🚨 Breaking News {i}/{len(breaking)}")
                self.process_story(b_news, "ब्रेकिंग न्यूज")
        
        logger.info(f"\n✅ Bulletin complete: {story_count} stories streamed")
    
    def run_loop(self):
        """Loop current bulletin until next time slot"""
        time_slot, bulletin_marathi, bulletin_english = self.bulletin_manager.get_current_bulletin()
        seconds_until_next = self.bulletin_manager.seconds_until_next()
        
        minutes_remaining = seconds_until_next // 60
        
        logger.info(f"\n🔁 Looping current bulletin ({bulletin_marathi})")
        logger.info(f"   Next bulletin in: {minutes_remaining} minutes")
        logger.info(f"   Repeating story cycle...")
        
        # Reset news queue for loop
        self.news_queue.reset()
        
        # Process news in loop
        story_count = 0
        while True:
            # Check if time for next bulletin
            current_time = datetime.now().strftime("%H:%M")
            next_bulletin_time = self.bulletin_manager.get_next_bulletin_time()
            
            if datetime.now() >= next_bulletin_time:
                logger.info(f"\n⏰ Time for next bulletin!")
                break
            
            news = self.news_queue.get_next_news()
            if not news:
                # Reset for next loop
                self.news_queue.reset()
                news = self.news_queue.get_next_news()
            
            if not news:
                logger.warning("⚠️ No news available, attempting to re-fetch in 10 seconds...")
                time.sleep(10)
                # Try to re-fetch if we have no news at all
                if not self.news_queue.main_news:
                    logger.info("🔄 Queue is empty, attempting emergency news fetch...")
                    if self.fetch_and_process_news():
                        logger.info("✅ Emergency fetch successful!")
                        continue
                    else:
                        logger.warning("❌ Emergency fetch failed, waiting 5 minutes before next try...")
                        time.sleep(300) 
                continue
            
            story_count += 1
            logger.info(f"\n📍 Repeat Cycle - Story {story_count}")
            
            self.process_story(news, bulletin_marathi)
            
            # Optional promo
            if story_count % 5 == 0:
                self.play_promo()
    
    def start(self):
        """Start 24×7 TV engine"""
        logger.info("\n" + "=" * 70)
        logger.info("🚀 VARTAPRAVAH 24×7 TV ENGINE STARTED")
        logger.info("=" * 70)
        logger.info(f"📺 Streaming to: {self.rtmp_url[:50]}...")
        logger.info(f"⏰ Bulletin schedule:")
        for time_slot, marathi, english in BULLETIN_SCHEDULE:
            logger.info(f"    {time_slot} → {marathi} ({english})")
        logger.info("=" * 70 + "\n")
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Run current bulletin
                self.run_bulletin()
                
                # Loop until next bulletin
                self.run_loop()
        
        except KeyboardInterrupt:
            logger.info("\n\n⏹️ Stopping TV engine...")
            self.is_running = False
        
        except Exception as e:
            logger.error(f"\n❌ Fatal error: {str(e)}")
            logger.error("Restarting in 30 seconds...")
            time.sleep(30)
            self.start()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def start_channel():
    """Start VARTAPRAVAH 24×7 channel"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    rtmp_url = os.getenv("YOUTUBE_RTMP_URL", DEFAULT_RTMP)
    engine = TVEngine(rtmp_url=rtmp_url)
    engine.start()


if __name__ == "__main__":
    start_channel()
