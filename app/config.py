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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "app", "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
