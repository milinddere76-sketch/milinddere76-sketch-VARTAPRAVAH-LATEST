import logging
import os
from pathlib import Path
from TTS.api import TTS

logger = logging.getLogger(__name__)

# Initialize TTS model
try:
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    logger.info("✅ TTS model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load TTS model: {str(e)}")
    tts = None

def generate_audio(text: str, output_path: str = "output/audio.wav") -> str:
    """Generate speech audio from text using Coqui TTS.
    
    Args:
        text: Input text to convert to speech
        output_path: Path to save the WAV file
        
    Returns:
        Path to generated audio file
        
    Raises:
        ValueError: If TTS model not initialized or text is empty
        Exception: If audio generation fails
    """
    try:
        if not tts:
            raise ValueError("TTS model not initialized")
        
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎙️ Generating audio for: {text[:50]}...")
        tts.tts_to_file(text=text, file_path=output_path)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"✅ Audio generated successfully: {output_path} ({file_size} bytes)")
            return output_path
        else:
            raise Exception(f"Audio file not created at {output_path}")
            
    except Exception as e:
        logger.error(f"❌ Audio generation failed: {str(e)}")
        raise
