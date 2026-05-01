from TTS.api import TTS
from gtts import gTTS
import config
import os

tts_model = None

def init_tts():
    """Initializes the Neural TTS engine."""
    global tts_model
    if tts_model is None:
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        print(f"🎙️ [TTS] Initializing XTTS v2 Engine...")
        try:
            tts_model = TTS(model_name=model_name).to("cuda" if os.getenv("USE_GPU") == "True" else "cpu")
        except Exception as e:
            print(f"⚠️ [TTS] Failed to load XTTS: {e}")

def generate_audio(text, file_path, anchor_type="female"):
    """
    Generates Marathi audio with Anchor Identity and gTTS fallback.
    """
    global tts_model
    
    # Select voice sample based on anchor type
    # Expecting anchor_male.wav or anchor_female.wav in assets
    voice_sample = os.path.join(config.ASSETS_DIR, f"anchor_{anchor_type}.wav")
    
    if not os.path.exists(voice_sample):
        # Fallback to generic anchor_voice.wav if specific one is missing
        voice_sample = os.path.join(config.ASSETS_DIR, "anchor_voice.wav")

    # Attempt XTTS (Pro Quality)
    if tts_model:
        try:
            print(f"🎙️ [XTTS] Synthesizing {anchor_type.upper()} voice...")
            tts_model.tts_to_file(
                text=text,
                language="mr",
                speaker_wav=voice_sample if os.path.exists(voice_sample) else None,
                file_path=file_path
            )
            return file_path
        except Exception as e:
            print(f"⚠️ [XTTS] Failed: {e}. Falling back to gTTS.")

    # Fallback: gTTS (Lightweight/Reliable)
    try:
        print(f"🎙️ [gTTS] Using emergency fallback for Marathi speech...")
        tts = gTTS(text=text, lang='mr')
        tts.save(file_path)
        return file_path
    except Exception as e:
        print(f"❌ [TTS] All synthesis methods failed: {e}")
        return None

class TTSEngine:
    def generate_audio(self, text, output_path, anchor_type="female"):
        return generate_audio(text, output_path, anchor_type)
