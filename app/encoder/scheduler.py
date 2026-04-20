import os
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()
NEWS_INTERVAL = int(os.getenv('NEWS_INTERVAL', 5))

logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self, generate_func):
        self.generate_func = generate_func
        self.scheduler = BackgroundScheduler()

    def start_scheduler(self):
        """Start the scheduler to generate news periodically."""
        self.scheduler.add_job(self.generate_func, 'interval', minutes=NEWS_INTERVAL)
        self.scheduler.start()
        logger.info(f"Scheduler started, generating news every {NEWS_INTERVAL} minutes")

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    def generate_now(self):
        """Generate news immediately."""
        self.generate_func()