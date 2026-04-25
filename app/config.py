import os
from dotenv import load_dotenv

load_dotenv()

# --- REDIS CONFIG ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
QUEUE_NAME = "news_queue"

# --- API KEYS ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY", "qcu7-xesd-m4sv-9zvv-e335")

# --- MODEL CONFIG ---
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# --- RESOURCE MANAGEMENT ---
MAX_WORKERS = 1 # VERY IMPORTANT: SadTalker is VRAM intensive. Limit to 1 job.

# --- PATHS ---
def get_assets_dir():
    # 1. Try absolute path (Standard Docker)
    if os.path.exists("/app/assets/promo.mp4"):
        return "/app/assets"
    
    # 2. Try nested path (Coolify specific)
    if os.path.exists("/app/app/assets/promo.mp4"):
        return "/app/app/assets"
    
    # 3. Local fallback
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets")

ASSETS_DIR = get_assets_dir()
print(f"📂 [CONFIG] Assets directory resolved to: {ASSETS_DIR}")
OUTPUT_DIR = "/app/output" if os.path.exists("/app") else os.path.join(os.path.dirname(ASSETS_DIR), "output")
