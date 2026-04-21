import os
import subprocess
import logging
from dotenv import load_dotenv
from graphics_engine import GraphicsEngine

load_dotenv()
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

logger = logging.getLogger(__name__)

class SceneBuilder:
    def __init__(self):
        self.studio_path = os.path.join(ASSETS_DIR, 'studio.jpg')
        self.graphics_engine = GraphicsEngine()

    def build_scene(self, anchor_video: str, headline: str, ticker_text: str, breaking: bool, output_path: str):
        """Build final scene with all layers."""
        # For simplicity, since graphics_engine handles overlays, just copy or process
        # But to combine background + anchor video
        # Assume anchor_video is already with lip sync
        # Add background if needed, but since studio is background, perhaps overlay anchor on studio

        temp_bg_video = os.path.join(TEMP_DIR, 'bg.mp4')
        # Create background video
        cmd_bg = [
            'ffmpeg', '-y', '-loop', '1', '-i', self.studio_path,
            '-i', anchor_video, '-c:v', 'libx264', '-c:a', 'copy',
            '-shortest', temp_bg_video
        ]
        subprocess.run(cmd_bg, check=True)

        # Now add graphics
        self.graphics_engine.add_graphics(temp_bg_video, headline, ticker_text, breaking, output_path)

        logger.info(f"Scene built: {output_path}")
        return output_path