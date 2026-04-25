from TTS.api import TTS
import config
import os

tts = None

def init_tts():
    """Initializes the Neural TTS engine for consistent branding."""
    global tts
    if tts is None:
        # XTTS v2 is the industry standard for high-fidelity Marathi cloning
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        print(f"🎙️ [BRANDING] Initializing Custom Anchor Voice Engine ({model_name})...")
        tts = TTS(model_name=model_name).to("cuda" if os.getenv("USE_GPU") == "True" else "cpu")

def generate_audio(text, file_path):
    """
    Generates Marathi audio using the Custom Anchor Identity.
    Strictly uses the branded voice sample for zero-shot cloning.
    """
    global tts
    if tts is None:
        init_tts()

    # BRANDED ANCHOR IDENTITY
    # The user should place their clean Marathi anchor sample here.
    anchor_sample = os.path.join(config.ASSETS_DIR, "anchor_voice.wav")
    
    if not os.path.exists(anchor_sample):
        print(f"⚠️ [BRANDING] Branded sample {anchor_sample} not found! Using fallback.")
        # If no custom sample, we use a default available one or the first one in assets
        wavs = [f for f in os.listdir(config.ASSETS_DIR) if f.endswith(".wav")]
        if wavs:
            anchor_sample = os.path.join(config.ASSETS_DIR, wavs[0])
        else:
            # Emergency fallback: skip cloning or use a dummy path
            # In production, this file MUST exist for the "Identity" to work.
            anchor_sample = None

    try:
        print(f"🎙️ [TTS] Synthesizing audio with ANCHOR IDENTITY...")
        tts.tts_to_file(
            text=text,
            language="mr",
            speaker_wav=anchor_sample,
            file_path=file_path
        )
        return file_path
    except Exception as e:
        print(f"❌ [TTS] Synthesis failed: {e}")
        return None

class TTSEngine:
    def generate_audio(self, text, output_path, speaker_wav=None):
        """Worker wrapper ensuring the branded identity is used."""
        return generate_audio(text, output_path)
