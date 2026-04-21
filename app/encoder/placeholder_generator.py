"""
Generate placeholder/fallback videos for streaming.
Used when no actual news content is available.
"""

import os
import subprocess
import logging
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')

logger = logging.getLogger(__name__)

class PlaceholderGenerator:
    def __init__(self):
        self.videos_dir = VIDEOS_DIR
        self.temp_dir = TEMP_DIR
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_placeholder_image(self, text: str = "VartaPravah - Loading...") -> str:
        """Create a placeholder image."""
        try:
            # Create simple blue background
            img = Image.new('RGB', (1920, 1080), color=(25, 45, 85))
            draw = ImageDraw.Draw(img)
            
            # Try to use Devanagari font if available
            font_path = os.path.join(ASSETS_DIR, 'fonts', 'NotoSansDevanagari-Bold.ttf')
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 80)
            else:
                font = ImageFont.load_default()
            
            # Draw text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            
            draw.text((x, y), text, font=font, fill=(255, 255, 255))
            
            # Save image
            image_path = os.path.join(self.temp_dir, 'placeholder.png')
            img.save(image_path)
            logger.info(f"Placeholder image created: {image_path}")
            return image_path
        except Exception as e:
            logger.error(f"Error creating placeholder image: {e}")
            raise

    def create_placeholder_audio(self) -> str:
        """Create a placeholder audio file (silence)."""
        try:
            audio_path = os.path.join(self.temp_dir, 'placeholder_audio.aac')
            
            # Create 60 seconds of silence
            cmd = [
                'ffmpeg', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                '-t', '60', '-q:a', '9', '-acodec', 'aac', audio_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Placeholder audio created: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Error creating placeholder audio: {e}")
            raise

    def create_fallback_video(self) -> str:
        """Create a complete fallback video for streaming."""
        try:
            logger.info("Creating fallback video...")
            
            # Create placeholder image and audio
            image_path = self.create_placeholder_image("वर्ताप्रवाह\nVartaPravah - AI News Broadcasting")
            audio_path = self.create_placeholder_audio()
            
            # Combine into video
            fallback_video = os.path.join(self.videos_dir, 'fallback.mp4')
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1', '-i', image_path,
                '-i', audio_path,
                '-c:v', 'libx264', '-preset', 'fast', '-b:v', '3000k',
                '-c:a', 'aac', '-b:a', '128k',
                '-shortest', '-pix_fmt', 'yuv420p',
                '-t', '60',  # 60 seconds
                fallback_video
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info(f"Fallback video created: {fallback_video}")
            return fallback_video
        except Exception as e:
            logger.error(f"Error creating fallback video: {e}")
            raise
