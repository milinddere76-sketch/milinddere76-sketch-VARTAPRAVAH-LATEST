import os
import subprocess
import logging
from dotenv import load_dotenv

load_dotenv()
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1920))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1080))
FONT_PATH = os.path.join(ASSETS_DIR, 'fonts', 'NotoSansDevanagari-Bold.ttf')

logger = logging.getLogger(__name__)

class GraphicsEngine:
    def __init__(self):
        self.logo_path = os.path.join(ASSETS_DIR, 'graphics', 'logo.png')
        self.lower_third_path = os.path.join(ASSETS_DIR, 'graphics', 'lower_third.png')
        self.breaking_path = os.path.join(ASSETS_DIR, 'graphics', 'breaking.png')
        self.ticker_bg_path = os.path.join(ASSETS_DIR, 'graphics', 'ticker_bg.png')

    def add_graphics(self, input_video: str, headline: str, ticker_text: str, breaking: bool, output_video: str):
        """Add TV graphics to video."""
        filters = []

        # Logo overlay
        if os.path.exists(self.logo_path):
            filters.append(f"[0:v][1:v]overlay=x=W-w-10:y=10[logo]")

        # Lower third
        if os.path.exists(self.lower_third_path):
            filters.append(f"[logo][2:v]overlay=x=0:y=H-h-200[lower]")

        # Breaking news
        if breaking and os.path.exists(self.breaking_path):
            filters.append(f"[lower][3:v]overlay=x=0:y=0[break]")

        # Ticker
        ticker_filter = f"drawtext=fontfile='{FONT_PATH}':textfile='{os.path.join(TEMP_DIR, 'ticker.txt')}':fontsize=40:fontcolor=white:box=1:boxcolor=black@0.5:x=w-mod(t*150,w+tw):y=h-100"
        filters.append(f"[break]{ticker_filter}[ticker]")

        # Clock
        clock_filter = f"drawtext=fontfile='{FONT_PATH}':text='%{localtime\\: %H\\:%M\\:%S}':fontsize=30:fontcolor=white:x=10:y=10"
        filters.append(f"[ticker]{clock_filter}[final]")

        # Headline on lower third
        headline_filter = f"drawtext=fontfile='{FONT_PATH}':text='{headline}':fontsize=50:fontcolor=white:x=50:y=H-150"
        filters.append(f"[final]{headline_filter}[out]")

        inputs = ['-i', input_video]
        if os.path.exists(self.logo_path):
            inputs.extend(['-i', self.logo_path])
        if os.path.exists(self.lower_third_path):
            inputs.extend(['-i', self.lower_third_path])
        if breaking and os.path.exists(self.breaking_path):
            inputs.extend(['-i', self.breaking_path])

        cmd = ['ffmpeg', '-y'] + inputs + ['-filter_complex', ';'.join(filters), '-map', '[out]', '-c:v', 'libx264', '-c:a', 'copy', output_video]
        try:
            subprocess.run(cmd, check=True)
            logger.info(f"Graphics added to video: {output_video}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Graphics addition failed: {e}")
            # Copy input to output as fallback
            subprocess.run(['cp', input_video, output_video], check=True)