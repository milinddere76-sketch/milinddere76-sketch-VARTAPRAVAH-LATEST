import os
import subprocess
import logging
from dotenv import load_dotenv
from pathlib import Path

# =========================
# Initialize TTS Model
# =========================
try:
    from TTS.api import TTS
except ImportError:
    TTS = None
    logging.warning("TTS not installed. Install with: pip install TTS")

load_dotenv()
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
WAV2LIP_PATH = os.getenv('WAV2LIP_PATH', '/app/Wav2Lip')

logger = logging.getLogger(__name__)

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Initialize Coqui TTS (lazy load)
_tts_model = None

def get_tts_model():
    """Lazy load TTS model to avoid startup delays."""
    global _tts_model
    if _tts_model is None and TTS is not None:
        try:
            logger.info("🎙️ Loading Coqui XTTS v2 model...")
            _tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
            logger.info("✅ Coqui TTS model loaded")
        except Exception as e:
            logger.warning(f"Failed to load TTS on GPU, trying CPU: {e}")
            try:
                _tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
                logger.info("✅ Coqui TTS model loaded (CPU)")
            except Exception as e:
                logger.error(f"Failed to load TTS: {e}")
                _tts_model = None
    return _tts_model


class LipSyncEngine:
    def __init__(self):
        self.wav2lip_dir = os.path.join(ASSETS_DIR, 'wav2lip')
        self.checkpoint_path = os.path.join(self.wav2lip_dir, 'checkpoints', 'wav2lip.pth')
        self.inference_script = os.path.join(self.wav2lip_dir, 'inference.py')
        self.ensure_wav2lip()
        self.tts_model = get_tts_model()

    def ensure_wav2lip(self):
        """Ensure Wav2Lip is available."""
        if not os.path.exists(self.wav2lip_dir):
            logger.info("Downloading Wav2Lip repository")
            try:
                subprocess.run(['git', 'clone', 'https://github.com/Rudrabha/Wav2Lip.git', self.wav2lip_dir], check=True)
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to clone Wav2Lip: {e}")
        if not os.path.exists(self.checkpoint_path):
            logger.info("Downloading Wav2Lip checkpoint")
            try:
                subprocess.run(['wget', '-O', self.checkpoint_path, 
                    'https://iiitaphyd-my.sharepoint.com/:f:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27BDNQHykbZpqdO3t3Bw?e=TBFBVW&download=1'], check=True)
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to download checkpoint: {e}")

    def generate_audio(self, text: str, output_path: str, language: str = "mr", speaker_wav: str = None) -> str:
        """Generate audio using Coqui TTS (Marathi support)."""
        logger.info(f"🎙️ Generating {language} voice from text...")
        
        if self.tts_model is None:
            logger.error("TTS model not available")
            raise RuntimeError("TTS model not initialized")
        
        try:
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                language=language,
                speaker_wav=speaker_wav  # Optional voice cloning
            )
            logger.info(f"✅ Audio generated: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Audio generation failed: {e}")
            raise

    def generate_lip_sync(self, face_image: str, audio_path: str, output_path: str) -> str:
        """Generate lip sync video using Wav2Lip."""
        logger.info(f"🗣️ Generating lip sync video...")
        
        if not os.path.exists(face_image):
            logger.error(f"Face image not found: {face_image}")
            raise FileNotFoundError(f"Face image not found: {face_image}")
        
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            cmd = [
                'python', self.inference_script,
                '--checkpoint_path', self.checkpoint_path,
                '--face', face_image,
                '--audio', audio_path,
                '--outfile', output_path
            ]
            subprocess.run(cmd, check=True, cwd=self.wav2lip_dir)
            logger.info(f"✅ Lip sync video generated: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Wav2Lip failed: {e}")
            # Fallback: create static video
            logger.info("📹 Fallback: Creating static video...")
            return self.create_static_video(face_image, audio_path, output_path)

    def create_static_video(self, image_path: str, audio_path: str, output_path: str) -> str:
        """Create static video from image and audio as fallback."""
        logger.info("Creating static video (fallback)...")
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', image_path,
            '-i', audio_path, '-c:v', 'libx264', '-c:a', 'aac',
            '-shortest', '-pix_fmt', 'yuv420p', output_path
        ]
        try:
            subprocess.run(cmd, check=True)
            logger.info(f"✅ Static video created: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create static video: {e}")
            raise

    def generate_anchor_video(self, text: str, anchor: str = "male", language: str = "mr") -> str:
        """Complete pipeline: Text → TTS → Wav2Lip → Video."""
        logger.info(f"🎬 Generating {anchor} anchor video...")
        
        # Verify anchor assets exist
        face_image = os.path.join(ASSETS_DIR, 'anchors', f"{anchor}.png")
        if not os.path.exists(face_image):
            raise FileNotFoundError(f"Anchor image not found: {face_image}")
        
        # Generate audio
        audio_path = os.path.join(TEMP_DIR, f"audio_{anchor}.wav")
        self.generate_audio(text, audio_path, language=language)
        
        # Generate lip sync video
        output_video = os.path.join(os.getenv('OUTPUT_DIR', 'app/videos'), f"{anchor}_anchor.mp4")
        os.makedirs(os.path.dirname(output_video), exist_ok=True)
        
        self.generate_lip_sync(face_image, audio_path, output_video)
        
        logger.info(f"✅ Complete: {output_video}")
        return output_video