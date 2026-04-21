import os
import logging
from dotenv import load_dotenv

# Lazy load TTS to avoid startup delays
try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS = None
    TTS_AVAILABLE = False
    logging.warning("TTS not installed. Install with: pip install TTS")
except Exception as e:
    # Handle PyTorch DLL errors on Windows
    TTS = None
    TTS_AVAILABLE = False
    logging.warning(f"TTS initialization failed (likely PyTorch issue): {e}")
    logging.warning("On Windows, install: https://aka.ms/vs/17/release/vc_redist.x64.exe")

load_dotenv()
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

logger = logging.getLogger(__name__)

# Initialize Coqui TTS model (lazy load)
_tts_model = None

def get_tts_model(gpu=True):
    """Lazy load TTS model to avoid startup delays."""
    global _tts_model
    if _tts_model is None and TTS_AVAILABLE and TTS is not None:
        try:
            logger.info("Loading Coqui XTTS v2 model...")
            _tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=gpu)
            logger.info("Coqui TTS model loaded")
        except Exception as e:
            logger.warning(f"Failed to load TTS on GPU, trying CPU: {e}")
            try:
                _tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
                logger.info("Coqui TTS model loaded (CPU)")
            except Exception as e:
                logger.error(f"Failed to load TTS: {e}")
                _tts_model = None
    return _tts_model


class TTSEngine:
    def __init__(self, lang='mr', gpu=True):
        """
        Initialize TTS Engine for Marathi text-to-speech.
        
        Args:
            lang: Language code (mr for Marathi)
            gpu: Use GPU if available
        """
        self.lang = lang
        self.tts_model = get_tts_model(gpu=gpu)
        os.makedirs(TEMP_DIR, exist_ok=True)

    def generate_audio(self, text: str, filename: str = 'audio.wav', language: str = None):
        """Generate Marathi TTS audio from text using Coqui XTTS v2."""
        if self.tts_model is None:
            logger.error("TTS model not available")
            raise RuntimeError("TTS model not initialized")
        
        lang = language or self.lang
        filepath = os.path.join(TEMP_DIR, filename)
        
        try:
            logger.info(f"🎙️ Generating {lang} voice from text...")
            self.tts_model.tts_to_file(
                text=text,
                file_path=filepath,
                language=lang
            )
            logger.info(f"✅ TTS audio saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error generating TTS: {e}")
            raise

    def generate_dual_audio(self, text: str, anchor='male', language: str = None):
        """Generate audio with anchor-specific voice characteristics."""
        if self.tts_model is None:
            logger.error("TTS model not available")
            raise RuntimeError("TTS model not initialized")
        
        lang = language or self.lang
        filename = f"audio_{anchor}.wav"
        filepath = os.path.join(TEMP_DIR, filename)
        
        try:
            logger.info(f"🎙️ Generating {anchor} anchor voice...")
            self.tts_model.tts_to_file(
                text=text,
                file_path=filepath,
                language=lang
            )
            logger.info(f"✅ Dual TTS audio saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error generating dual TTS: {e}")
            raise