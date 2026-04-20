"""
Bulletin-based news scheduling system for VartaPravah.
Generates news bulletins at specific times throughout the day.
"""

import time
import logging
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)


class BulletinScheduler:
    """Schedule news generation based on fixed bulletin times."""
    
    # Bulletin schedule: time (HH:MM) -> bulletin type
    BULLETIN_SCHEDULE = {
        "05:00": "morning",
        "12:00": "afternoon",
        "17:00": "evening",
        "21:00": "prime_time",
        "00:00": "night"
    }
    
    # Bulletin metadata
    BULLETIN_INFO = {
        "morning": {
            "name": "Morning Bulletin",
            "description": "Early morning news (5:00 AM)",
            "duration": 10,
            "tone": "informative"
        },
        "afternoon": {
            "name": "Afternoon Bulletin",
            "description": "Midday news update (12:00 PM)",
            "duration": 8,
            "tone": "balanced"
        },
        "evening": {
            "name": "Evening Bulletin",
            "description": "Evening news (5:00 PM)",
            "duration": 12,
            "tone": "comprehensive"
        },
        "prime_time": {
            "name": "Prime Time News",
            "description": "Prime time bulletin (9:00 PM)",
            "duration": 15,
            "tone": "in-depth"
        },
        "night": {
            "name": "Night Bulletin",
            "description": "Late night news (12:00 AM)",
            "duration": 7,
            "tone": "brief"
        }
    }
    
    def __init__(self, generate_func):
        """
        Initialize bulletin scheduler.
        
        Args:
            generate_func: Callable that generates news. 
                          Should accept bulletin_type parameter.
        """
        self.generate_func = generate_func
        self.running = False
        self.scheduler_thread = None
        self.last_run = None
    
    @staticmethod
    def get_current_bulletin_type():
        """Get bulletin type based on current time."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        elif 21 <= hour < 24:
            return "prime_time"
        else:  # 0-4
            return "night"
    
    @staticmethod
    def get_next_bulletin_time():
        """Get next scheduled bulletin time."""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        times = sorted(BulletinScheduler.BULLETIN_SCHEDULE.keys())
        
        # Find next time in today's schedule
        for scheduled_time in times:
            if current_time < scheduled_time:
                return scheduled_time
        
        # If past all times, next is first time tomorrow
        return times[0]
    
    def start_scheduler(self):
        """Start the bulletin scheduler in background thread."""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Bulletin scheduler started")
        self._log_schedule()
    
    def stop_scheduler(self):
        """Stop the bulletin scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Bulletin scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop."""
        logger.info("Bulletin scheduler thread started")
        
        while self.running:
            now = datetime.now().strftime("%H:%M")
            
            # Check if it's time to generate a bulletin
            if now in self.BULLETIN_SCHEDULE:
                bulletin_type = self.BULLETIN_SCHEDULE[now]
                
                # Avoid running multiple times in same minute
                if self.last_run != now:
                    try:
                        logger.info(f"Generating {bulletin_type} bulletin at {now}")
                        self.generate_func(bulletin_type=bulletin_type)
                        self.last_run = now
                    except Exception as e:
                        logger.error(f"Error generating bulletin: {e}")
            
            # Check every 30 seconds
            time.sleep(30)
    
    def generate_now(self, bulletin_type=None):
        """
        Generate news immediately.
        
        Args:
            bulletin_type: Specific bulletin type, or auto-detect if None
        """
        if bulletin_type is None:
            bulletin_type = self.get_current_bulletin_type()
        
        try:
            logger.info(f"Generating {bulletin_type} bulletin immediately")
            self.generate_func(bulletin_type=bulletin_type)
        except Exception as e:
            logger.error(f"Error generating bulletin: {e}")
    
    def _log_schedule(self):
        """Log the bulletin schedule."""
        logger.info("=" * 50)
        logger.info("BULLETIN SCHEDULE")
        logger.info("=" * 50)
        for time_str, bulletin_type in sorted(self.BULLETIN_SCHEDULE.items()):
            info = self.BULLETIN_INFO[bulletin_type]
            logger.info(f"{time_str} - {info['name']}: {info['description']}")
        logger.info("=" * 50)
    
    @staticmethod
    def get_bulletin_info(bulletin_type):
        """Get metadata for a bulletin type."""
        return BulletinScheduler.BULLETIN_INFO.get(
            bulletin_type,
            {"name": "Unknown", "description": "", "duration": 10, "tone": "standard"}
        )
    
    def get_schedule_status(self):
        """Get current schedule status."""
        now = datetime.now()
        current_type = self.get_current_bulletin_type()
        next_time = self.get_next_bulletin_time()
        
        return {
            "current_time": now.strftime("%H:%M"),
            "current_bulletin_type": current_type,
            "current_bulletin_info": self.get_bulletin_info(current_type),
            "next_bulletin_time": next_time,
            "next_bulletin_type": self.BULLETIN_SCHEDULE[next_time],
            "next_bulletin_info": self.get_bulletin_info(self.BULLETIN_SCHEDULE[next_time]),
            "scheduler_running": self.running
        }
