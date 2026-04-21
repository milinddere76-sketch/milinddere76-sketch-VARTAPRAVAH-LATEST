import os
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def run_lipsync(audio_path: str, video_path: str = "assets/anchor.mp4", output_video: str = "output/lipsync.mp4") -> str:
    """Generate lip-synced video using Wav2Lip.
    
    Args:
        audio_path: Path to input audio file
        video_path: Path to anchor video file
        output_video: Path to save output video
        
    Returns:
        Path to generated video file
        
    Raises:
        FileNotFoundError: If input files don't exist
        Exception: If lip-sync generation fails
    """
    try:
        # Validate input files
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Anchor video not found: {video_path}")
        
        # Create output directory
        Path(output_video).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎬 Starting lip-sync with audio: {audio_path}")
        
        cmd = [
            "python", "Wav2Lip/inference.py",
            "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip.pth",
            "--face", video_path,
            "--audio", audio_path,
            "--outfile", output_video
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        
        if result.returncode != 0:
            logger.error(f"❌ Lip-sync failed: {result.stderr}")
            raise Exception(f"Wav2Lip inference failed: {result.stderr}")
        
        if os.path.exists(output_video):
            file_size = os.path.getsize(output_video)
            logger.info(f"✅ Lip-sync video generated: {output_video} ({file_size} bytes)")
            return output_video
        else:
            raise Exception(f"Output video not created at {output_video}")
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Lip-sync generation timed out (exceeded 1 hour)")
        raise
    except Exception as e:
        logger.error(f"❌ Lip-sync failed: {str(e)}")
        raise
