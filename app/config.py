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
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY", "5w92-9u7p-ucjh-b1bx-bszv")

# --- MODEL CONFIG ---
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# --- RESOURCE MANAGEMENT ---
MAX_WORKERS = 1 # VERY IMPORTANT: SadTalker is VRAM intensive. Limit to 1 job.

# --- PATHS ---
def get_assets_dir():
    # 1. Try relative to this config file (Works locally and in some Docker setups)
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "assets")
    if os.path.exists(os.path.join(path, "promo.mp4")):
        return path
    
    # 2. Try absolute Docker root (Works in Coolify/Standard Docker)
    docker_path = "/app/assets"
    if os.path.exists(os.path.join(docker_path, "promo.mp4")):
        return docker_path
    
    # Fallback to local
    return path

ASSETS_DIR = get_assets_dir()
OUTPUT_DIR = os.path.join(os.path.dirname(ASSETS_DIR), "output")
