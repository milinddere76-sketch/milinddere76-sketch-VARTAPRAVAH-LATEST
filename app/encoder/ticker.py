import os
import logging
from dotenv import load_dotenv

load_dotenv()
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

logger = logging.getLogger(__name__)

class TickerSystem:
    def __init__(self):
        self.ticker_file = os.path.join(TEMP_DIR, 'ticker.txt')

    def update_ticker(self, text: str):
        """Update ticker text file."""
        try:
            with open(self.ticker_file, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"Ticker updated: {text}")
        except Exception as e:
            logger.error(f"Error updating ticker: {e}")
            raise

    def get_ticker_text(self, content: str, category: str):
        """Generate ticker text from news content."""
        # Shorten content for ticker
        ticker_text = f"{category}: {content[:200]}..."
        return ticker_text