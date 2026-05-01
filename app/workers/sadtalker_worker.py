import redis
import json
import time
import os
import subprocess
import config
from services.tts_engine import init_tts, generate_audio
from services.sadtalker_engine import generate_ai_video
from services.video_engine import VideoEngine

# Dedicated SadTalker Worker Configuration
r = redis.Redis(host=config.REDIS_HOST, port=int(config.REDIS_PORT))
video_engine = VideoEngine()

os.makedirs(config.OUTPUT_DIR, exist_ok=True)

def upload_to_oracle(video_path, is_breaking=False):
    """
    Python Upload Hook (STEP 4)
    Automated transfer of news bulletins to the Oracle relay node.
    """
    if not config.ORACLE_IP:
        print("⚠️ [PIPELINE] ORACLE_IP not set. Skipping upload.")
        return False

    filename = os.path.basename(video_path)
    
    # Priority handling: Breaking news goes to its own subfolder
    subfolder = "breaking/" if is_breaking else ""
    remote_dest = f"{config.ORACLE_USER}@{config.ORACLE_IP}:{config.ORACLE_VIDEO_DIR}/{subfolder}"
    
    cmd = [
        "scp", "-i", config.ORACLE_KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        video_path,
        remote_dest
    ]
    
    print(f"📤 [PIPELINE] Uploading {filename} to Oracle ({'BREAKING' if is_breaking else 'NORMAL'})...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ [PIPELINE] Upload Successful: {filename}")
            return True
        else:
            print(f"❌ [PIPELINE] Upload Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"🚨 [PIPELINE] Upload Error: {e}")
        return False

def add_to_queue(video_filename, is_breaking=False):
    """
    Incorporate news into the dynamic playout queue (STEP 5).
    """
    if not config.ORACLE_IP:
        return False

    subfolder = "breaking/" if is_breaking else ""
    remote_file_path = f"/home/ubuntu/videos/{subfolder}{video_filename}"
    
    # Command to append the file to the playlist.txt
    cmd = [
        "ssh", "-i", config.ORACLE_KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        f"{config.ORACLE_USER}@{config.ORACLE_IP}",
        f"echo \"file '{remote_file_path}'\" >> /home/ubuntu/queue/playlist.txt"
    ]
    
    print(f"🧠 [PIPELINE] Adding {video_filename} to Oracle Queue...")
    try:
        subprocess.run(cmd, capture_output=True, text=True)
        return True
    except Exception as e:
        print(f"⚠️ [PIPELINE] Failed to update queue: {e}")
        return False

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
        generate_audio(script, audio_file, anchor_type=anchor_type)

        if not os.path.exists(audio_file):
            print("❌ [SADTALKER-WORKER] TTS Failed")
            continue

        # 2. SadTalker AI Face Generation
        face_image = os.path.join(config.ASSETS_DIR, f"anchor_{anchor_type}.jpg")
        result_dir = os.path.join(config.OUTPUT_DIR, f"sadtalker_{task_id}")
        os.makedirs(result_dir, exist_ok=True)

        print(f"🎭 [SADTALKER-WORKER] Synthesizing Expressive Face...")
        generate_ai_video(face_image, audio_file)

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
                
                # 5. AUTO-TRANSFER TO ORACLE (STEP 4)
                is_breaking = task.get("type") == "BREAKING"
                success = upload_to_oracle(final_path, is_breaking=is_breaking)
                
                if success:
                    # 6. INSTANT QUEUE INJECTION (STEP 5)
                    add_to_queue(final_video, is_breaking=is_breaking)

                    # 7. AUTO-CLEANUP (Hetzner)
                    print(f"🧹 [CLEANUP] Removing local file: {final_path}")
                    os.remove(final_path)
                    
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
