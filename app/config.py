import os
from dotenv import load_dotenv

load_dotenv()

# --- REDIS CONFIG ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
QUEUE_NAME = "news_queue"

# --- POSTGRES CONFIG ---
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "vartapravah")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# --- API KEYS ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY", "qcu7-xesd-m4sv-9zvv-e335")

# --- MODEL CONFIG ---
TTS_MODEL = os.getenv("TTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")

# --- RESOURCE MANAGEMENT ---
MAX_WORKERS = 1  # SadTalker is VRAM intensive

# --- PATHS ---
def get_assets_dir():
    """Get assets directory with proper fallbacks."""
    # 1. Try absolute path (Standard Docker)
    path1 = "/app/assets"
    if os.path.exists(path1):
        return path1
    
    # 2. Try nested path (Coolify)
    path2 = "/app/app/assets"
    if os.path.exists(path2):
        return path2
    
    # 3. Local dev path
    base = os.path.dirname(os.path.abspath(__file__))
    path3 = os.path.join(base, "assets")
    if os.path.exists(path3):
        return path3
    
    # 4. Create and return default
    os.makedirs(path1, exist_ok=True)
    return path1

def get_output_dir():
    """Get output directory with proper fallbacks."""
    path1 = "/app/output"
    path2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    
    if os.path.exists(path1):
        return path1
    
    os.makedirs(path1, exist_ok=True)
    return path1

ASSETS_DIR = get_assets_dir()
OUTPUT_DIR = get_output_dir()
print(f"📂 [CONFIG] Assets: {ASSETS_DIR}")
print(f"📂 [CONFIG] Output: {OUTPUT_DIR}")
