import redis
import json
import time
import os
from app.services.tts_engine import init_tts, generate_audio
from app.services.sadtalker_engine import generate_ai_video

# Worker Initialization
r = redis.Redis(host="redis", port=6379)
init_tts()

# --- AUTO ANCHOR LOGIC ---
anchors = [
    "/app/assets/anchor_male.jpg",
    "/app/assets/anchor_female.jpg"
]
current = 0

def get_anchor():
    """Alternates between male and female identities for each bulletin."""
    global current
    anchor = anchors[current]
    current = 1 - current
    return anchor

print("🚀 [WORKER] VARTAPRAVAH AI Worker active. Monitoring news_queue...")

while True:
    # 1. Fetch News Task
    data = r.blpop("news_queue", timeout=5)

    if not data:
        time.sleep(1)
        continue

    try:
        # 2. Parse Task
        news = json.loads(data[1])
        audio_path = "/app/output/audio.mp3"

        print(f"🎙️ [WORKER] Processing News Cycle...")

        # 🔊 TTS: Generate Marathi Audio
        generate_audio(news["script"], audio_path)

        # 👤 Select anchor identity
        face_path = get_anchor()

        # 🎭 SadTalker: Synthesize Talking Face
        # This calls the GPU Node via the SadTalker Service Wrapper
        video_path = generate_ai_video(face_path, audio_path)

        print(f"✅ AI Anchor Video Ready: {video_path}")
        
        # In a full flow, we would push to 'ready_videos' for the streamer
        # r.rpush("ready_videos", video_path)

    except Exception as e:
        print(f"❌ Worker error: {e}")
        time.sleep(2)
