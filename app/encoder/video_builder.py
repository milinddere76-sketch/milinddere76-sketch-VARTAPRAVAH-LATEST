import os
import logging
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1920))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1080))

logger = logging.getLogger(__name__)

class VideoBuilder:
    def __init__(self):
        self.font_path = os.path.join(ASSETS_DIR, 'fonts', 'NotoSansDevanagari-Bold.ttf')
        self.logo_path = os.path.join(ASSETS_DIR, 'logo.png')
        self.studio_path = os.path.join(ASSETS_DIR, 'studio.jpg')

    def create_image_with_text(self, headline: str, category: str = '', breaking: bool = False):
        """Create image with headline overlay."""
        try:
            # Load background
            bg = Image.open(self.studio_path).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
            draw = ImageDraw.Draw(bg)

            # Load font
            font_size = 80
            font = ImageFont.truetype(self.font_path, font_size)

            # Headline position
            headline_bbox = draw.textbbox((0, 0), headline, font=font)
            headline_width = headline_bbox[2] - headline_bbox[0]
            headline_x = (VIDEO_WIDTH - headline_width) // 2
            headline_y = VIDEO_HEIGHT // 3

            # Draw headline
            draw.text((headline_x, headline_y), headline, font=font, fill='white')

            # Category
            if category:
                cat_font = ImageFont.truetype(self.font_path, 50)
                cat_bbox = draw.textbbox((0, 0), category, font=cat_font)
                cat_width = cat_bbox[2] - cat_bbox[0]
                cat_x = (VIDEO_WIDTH - cat_width) // 2
                cat_y = headline_y + 100
                draw.text((cat_x, cat_y), category, font=cat_font, fill='yellow')

            # Breaking news flash
            if breaking:
                flash_font = ImageFont.truetype(self.font_path, 60)
                flash_text = "तातडीची बातमी"
                flash_bbox = draw.textbbox((0, 0), flash_text, font=flash_font)
                flash_width = flash_bbox[2] - flash_bbox[0]
                flash_x = (VIDEO_WIDTH - flash_width) // 2
                flash_y = VIDEO_HEIGHT // 6
                draw.rectangle([flash_x-20, flash_y-10, flash_x+flash_width+20, flash_y+60], fill='red')
                draw.text((flash_x, flash_y), flash_text, font=flash_font, fill='white')

            # Add logo
            if os.path.exists(self.logo_path):
                logo = Image.open(self.logo_path).resize((200, 200))
                bg.paste(logo, (50, 50), logo if logo.mode == 'RGBA' else None)

            # Save image
            image_path = os.path.join(TEMP_DIR, 'news_image.png')
            bg.save(image_path)
            logger.info(f"Image saved to {image_path}")
            return image_path
        except Exception as e:
            logger.error(f"Error creating image: {e}")
            raise