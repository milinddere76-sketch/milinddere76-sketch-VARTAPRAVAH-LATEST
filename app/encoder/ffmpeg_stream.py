import os
import subprocess
import logging
import time
from dotenv import load_dotenv

load_dotenv()
TEMP_DIR = os.getenv('TEMP_DIR', 'app/temp')
VIDEOS_DIR = os.getenv('VIDEOS_DIR', 'app/videos')
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1920))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1080))
VIDEO_FPS = int(os.getenv('VIDEO_FPS', 30))
AUDIO_BITRATE = os.getenv('AUDIO_BITRATE', '128k')
VIDEO_BITRATE = os.getenv('VIDEO_BITRATE', '3000k')
YOUTUBE_STREAM_KEY = os.getenv('YOUTUBE_STREAM_KEY')

logger = logging.getLogger(__name__)

class FFmpegStreamer:
    def __init__(self):
        self.stream_process = None
        self.font_path = os.path.join(ASSETS_DIR, 'fonts', 'NotoSansDevanagari-Bold.ttf')

    def combine_audio_video(self, image_path: str, audio_path: str, output_path: str, ticker_text: str, intro_path=None, outro_path=None):
        """Combine image and audio into video with ticker, intro/outro."""
        try:
            inputs = []
            filters = []

            # Intro
            if intro_path:
                inputs.extend(['-i', intro_path])
                filters.append(f"[0:v]concat=n=3:v=1:a=0[base];[base][1:v]concat=n=2:v=1:a=0[vout]")
            else:
                inputs.extend(['-loop', '1', '-i', image_path])
                filters.append("[0:v]")

            inputs.extend(['-i', audio_path])

            vf = f"{filters[0]}drawtext=fontfile='{self.font_path}':textfile='{os.path.join(TEMP_DIR, 'ticker.txt')}':fontsize=40:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-100:scroll=1"

            cmd = [
                'ffmpeg', '-y'
            ] + inputs + [
                '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac',
                '-b:a', AUDIO_BITRATE, '-b:v', VIDEO_BITRATE,
                '-pix_fmt', 'yuv420p', '-shortest',
                '-vf', vf,
                '-f', 'mp4', output_path
            ]
            subprocess.run(cmd, check=True)
            logger.info(f"Video created: {output_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e}")
            raise

    def stream_to_youtube(self, video_path: str):
        """Stream video to YouTube Live with loop."""
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1', '-i', video_path,
            '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', VIDEO_BITRATE,
            '-c:a', 'aac', '-b:a', AUDIO_BITRATE,
            '-f', 'flv', rtmp_url
        ]
        try:
            self.stream_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("Started streaming to YouTube with loop")
            return self.stream_process
        except Exception as e:
            logger.error(f"Error starting stream: {e}")
            raise

    def loop_stream(self, video_list: list):
        """Stream videos in loop."""
        if not video_list:
            fallback = os.path.join(VIDEOS_DIR, 'fallback.mp4')
            if os.path.exists(fallback):
                video_list = [fallback]
            else:
                logger.error("No videos to stream")
                return

        # Create concat file
        concat_file = os.path.join(TEMP_DIR, 'playlist.txt')
        with open(concat_file, 'w') as f:
            for vid in video_list:
                f.write(f"file '{vid}'\n")

        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', '-f', 'flv', rtmp_url
        ]
        try:
            self.stream_process = subprocess.Popen(cmd)
            logger.info("Started looped streaming")
        except Exception as e:
            logger.error(f"Error starting loop stream: {e}")
            raise

    def stop_stream(self):
        """Stop the stream."""
        if self.stream_process:
            self.stream_process.terminate()
            self.stream_process.wait()
            logger.info("Stream stopped")

    def is_streaming(self):
        """Check if streaming."""
        return self.stream_process and self.stream_process.poll() is None

    def concat_videos(self, video_paths: list, output_path: str):
        """Concatenate multiple videos."""
        concat_file = os.path.join(TEMP_DIR, 'concat_list.txt')
        with open(concat_file, 'w') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")
        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', output_path
        ]
        subprocess.run(cmd, check=True)