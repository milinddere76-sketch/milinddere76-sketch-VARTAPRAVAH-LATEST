import os
import time
from app import config

def generate_loop_video(image_path, output_path, duration=10):
    """
    Converts an AI Face Image into a high-quality Loop Video.
    Provides the temporal base for Wav2Lip.
    """
    # User's dynamic zoompan command for realistic subtle movement
    cmd = (
        f"ffmpeg -y -loop 1 -i {image_path} -t {duration} "
        "-vf \"zoompan=z='min(zoom+0.0005,1.1)':d=250:s=1280x720,scale=1280:720\" "
        f"-c:v libx264 -pix_fmt yuv420p {output_path}"
    )
    os.system(cmd)
    return output_path

def generate_lipsync(face_video, audio, output):
    """
    Wav2Lip synthesis using the Looped Video.
    """
    cmd = f"""
    python /app/Wav2Lip/inference.py \
    --checkpoint_path /app/Wav2Lip/checkpoints/wav2lip.pth \
    --face {face_video} \
    --audio {audio} \
    --outfile {output}
    """
    print(f"🧬 [LIP-SYNC] Syncing audio to Loop Video...")
    os.system(cmd)
    return output

class LipSyncEngine:
    def __init__(self):
        self.output_dir = config.OUTPUT_DIR
        self.assets_dir = config.ASSETS_DIR

    def generate_lipsync(self, audio_path, anchor_type="female"):
        """
        Hybrid Workflow: Image -> Loop -> Wav2Lip
        """
        ts = int(time.time())
        
        # 1. Start with AI Face Image
        face_image = os.path.join(self.assets_dir, f"anchor_{anchor_type}.jpg")
        if not os.path.exists(face_image):
            face_image = os.path.join(self.assets_dir, "studio.jpg")

        # 2. Create Loop Video (Temporal Base)
        loop_video = os.path.join(self.output_dir, f"loop_{ts}.mp4")
        generate_loop_video(face_image, loop_video)

        # 3. Apply Wav2Lip
        final_output = os.path.join(self.output_dir, f"talking_anchor_{ts}.mp4")
        generate_lipsync(loop_video, audio_path, final_output)
        
        if os.path.exists(final_output):
            return final_output
        else:
            # Fallback
            return loop_video
