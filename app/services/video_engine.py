import os
import config

def create_video(audio_path, output_path, script_text=""):
    """
    Generates a video by overlaying audio on a static studio image,
    including a professional scrolling news ticker.
    """
    studio_img = os.path.join(config.ASSETS_DIR, "studio.jpg")
    font_path = "/usr/share/fonts/truetype/noto/NotoSansMarathi-Regular.ttf"
    
    if not os.path.exists(font_path):
        font_path = "DejaVu Sans"

    # Clean text for FFmpeg (remove newlines and quotes)
    ticker_text = script_text.replace("\n", " | ").replace("'", "").replace("\"", "")
    if not ticker_text:
        ticker_text = "वार्ता प्रवाह - ताज्या घडामोडी"

    # User's requested scrolling ticker filter
    # x=w-mod(t*200\,w+tw) provides the scrolling effect
    video_filter = (
        f"drawtext=fontfile='{font_path}':"
        f"text='{ticker_text}':"
        "x=w-mod(t*200,w+tw):"
        "y=h-50:"
        "fontsize=30:"
        "fontcolor=white:"
        "box=1:boxcolor=black@0.6" # Added box for better readability
    )

    cmd = f"""
    ffmpeg -y -loop 1 -i {studio_img} \
    -i {audio_path} \
    -vf "{video_filter}" \
    -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
    -shortest -pix_fmt yuv420p {output_path}
    """
    
    print(f"🎬 [VIDEO] Creating video with Ticker: {output_path}...")
    os.system(cmd)
    return output_path

class VideoEngine:
    def generate_video(self, audio_path, script_text, output_filename):
        output_path = os.path.join(config.OUTPUT_DIR, output_filename)
        return create_video(audio_path, output_path, script_text)
