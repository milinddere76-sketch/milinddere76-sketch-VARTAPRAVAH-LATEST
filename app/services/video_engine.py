import os
import config

def create_video(sadtalker_video_path, output_path, script_text=""):
    """
    Generates a professional branded news video.
    Overlays: News Ticker, LIVE Badge, and Channel Logo.
    """
    logo_path = os.path.join(config.ASSETS_DIR, "varta_logo.png")
    font_path = "/usr/share/fonts/truetype/noto/NotoSansMarathi-Regular.ttf"
    
    if not os.path.exists(font_path):
        font_path = "DejaVu Sans"

    # Clean text for FFmpeg
    ticker_text = script_text.replace("\n", " | ").replace("'", "").replace("\"", "")
    if not ticker_text:
        ticker_text = "वार्ता प्रवाह - २४/७ बातम्या"

    # FFmpeg Filter Complex for Professional Look:
    # 1. Scale input video to 1280x720
    # 2. Overlay Logo at Top-Right
    # 3. Add "LIVE" red badge at Top-Left
    # 4. Add Scrolling Ticker at Bottom
    
    filters = (
        "[0:v]scale=1280:720[bg];"
        f"[1:v]scale=180:-1[logo];"
        "[bg][logo]overlay=W-w-20:20[v1];"
        "drawtext=text='● LIVE':fontcolor=white:fontsize=24:x=30:y=30:box=1:boxcolor=red@0.8:boxborderw=10[v2];"
        f"[v1][v2]overlay[v3];"
        f"[v3]drawtext=fontfile='{font_path}':text='{ticker_text}':x=w-mod(t*200,w+tw):y=h-60:fontsize=35:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=15"
    )

    cmd = f"""
    ffmpeg -y -i {sadtalker_video_path} \
    -i {logo_path} \
    -filter_complex "{filters}" \
    -r 24 \
    -c:v libx264 -preset ultrafast -pix_fmt yuv420p \
    -c:a aac -b:a 128k \
    {output_path}
    """
    
    print(f"🎬 [VIDEO-ENGINE] Branded Composition: {output_path}...")
    os.system(cmd)
    return output_path

class VideoEngine:
    def generate_video(self, video_path, script_text, output_filename):
        output_path = os.path.join(config.OUTPUT_DIR, output_filename)
        return create_video(video_path, output_path, script_text)
