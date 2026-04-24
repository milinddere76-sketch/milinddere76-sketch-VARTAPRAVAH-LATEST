import redis
import json
import time
import os
from app import config
from app.services.tts_engine import init_tts, generate_audio
from app.services.lip_sync import generate_ai_anchor
from app.services.video_engine import VideoEngine

# Dedicated SadTalker Worker Configuration
r = redis.Redis(host=config.REDIS_HOST, port=int(config.REDIS_PORT))
video_engine = VideoEngine()

os.makedirs(config.OUTPUT_DIR, exist_ok=True)

print("🎭 [SADTALKER-WORKER] Dedicated AI Face Engine starting...")
init_tts()

while True:
    # Listening for high-fidelity synthesis tasks
    data = r.blpop(config.QUEUE_NAME, timeout=5)

    if not data:
        time.sleep(1)
        continue

    try:
        task = json.loads(data[1])
        task_id = task["id"]
        script = task["script"]
        anchor_type = task.get("anchor_type", "female")
        
        print(f"🎙️ [SADTALKER-WORKER] Processing Task {task_id} for {anchor_type.upper()}...")

        # 1. Neural TTS Synthesis
        audio_file = os.path.join(config.OUTPUT_DIR, f"audio_{task_id}.mp3")
        generate_audio(script, audio_file)

        if not os.path.exists(audio_file):
            print("❌ [SADTALKER-WORKER] TTS Failed")
            continue

        # 2. SadTalker AI Face Generation
        face_image = os.path.join(config.ASSETS_DIR, f"anchor_{anchor_type}.jpg")
        result_dir = os.path.join(config.OUTPUT_DIR, f"sadtalker_{task_id}")
        os.makedirs(result_dir, exist_ok=True)

        print(f"🎭 [SADTALKER-WORKER] Synthesizing Expressive Face...")
        generate_ai_anchor(face_image, audio_file, result_dir)

        # 3. Find the rendered .mp4
        sadtalker_video = None
        for root, dirs, files in os.walk(result_dir):
            for file in files:
                if file.endswith(".mp4"):
                    sadtalker_video = os.path.join(root, file)
                    break
        
        if sadtalker_video:
            # 4. Final Video Composition (Ticker + Overlays)
            final_video = f"final_bulletin_{task_id}.mp4"
            final_path = video_engine.generate_video(sadtalker_video, script, final_video)
            
            if final_path and os.path.exists(final_path):
                print(f"✅ [SADTALKER-WORKER] Bulletin Completed: {final_path}")
                r.rpush("ready_videos", final_path)
                r.incr("stats_videos_generated")
            else:
                print("❌ [SADTALKER-WORKER] Composition Failed")
                r.incr("stats_errors_count")
        else:
            print("❌ [SADTALKER-WORKER] SadTalker Synthesis Failed")
            r.incr("stats_errors_count")

    except Exception as e:
        print("🚨 [SADTALKER-WORKER] Critical Error:", e)
        r.incr("stats_errors_count")
        time.sleep(2)
