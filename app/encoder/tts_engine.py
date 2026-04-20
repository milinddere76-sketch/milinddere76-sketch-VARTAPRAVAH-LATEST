import os
import logging
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self, lang='mr'):
        self.lang = lang

    def generate_audio(self, text: str, filename: str = 'audio.mp3'):
        """Generate Marathi TTS audio from text."""
        try:
            tts = gTTS(text=text, lang=self.lang, slow=False)
            filepath = os.path.join(TEMP_DIR, filename)
            tts.save(filepath)
            logger.info(f"TTS audio saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating TTS: {e}")
            raise

    def generate_dual_audio(self, text: str, anchor='male'):
        """Generate audio with dual anchor voices."""
        # For simplicity, use different speeds or voices if available
        # gTTS doesn't have built-in voices, but we can simulate
        slow = anchor == 'female'  # Female slower
        filename = f"audio_{anchor}.mp3"
        try:
            tts = gTTS(text=text, lang=self.lang, slow=slow)
            filepath = os.path.join(TEMP_DIR, filename)
            tts.save(filepath)
            logger.info(f"Dual TTS audio saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating dual TTS: {e}")
            raise