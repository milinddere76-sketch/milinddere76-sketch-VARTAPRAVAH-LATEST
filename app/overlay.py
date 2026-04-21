"""
Dynamic TV Overlay Engine for VARTAPRAVAH

Adds professional overlays to video:
- Channel logo (top corner)
- Lower-third bar with headline
- Optional scrolling ticker

Dependencies: FFmpeg, assets (logo.png, lower_bg.png, font.ttf)
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Asset paths
LOGO_PATH = "assets/logo.png"
LOWER_BG_PATH = "assets/lower_bg.png"
FONT_PATH = "assets/font.ttf"


def validate_assets() -> bool:
    """Check if all required asset files exist"""
    missing = []
    
    for path, name in [
        (FONT_PATH, "Font file"),
        # Logo and lower_bg are optional for some effects
    ]:
        if not os.path.exists(path):
            missing.append(f"{name} ({path})")
    
    if missing:
        logger.warning(f"⚠️ Missing assets: {', '.join(missing)}")
        logger.warning("   → Logo and lower-third may not display")
        return False
    
    return True


def add_overlay(
    input_video: str,
    output_video: str,
    headline: str = "वार्ताप्रवाह LIVE",
    use_ticker: bool = False,
    ticker_text: Optional[str] = None
) -> bool:
    """
    Add professional overlays to video.
    
    Args:
        input_video: Path to input video
        output_video: Path to output video
        headline: Lower-third headline text (Marathi)
        use_ticker: Enable scrolling ticker
        ticker_text: Text for scrolling ticker (overrides headline for ticker)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(input_video):
            logger.error(f"❌ Input video not found: {input_video}")
            return False
        
        # Validate assets
        validate_assets()
        
        logger.info(f"🎬 Adding overlays to: {input_video}")
        
        # Build filter_complex
        filters = []
        input_count = 0
        
        # Step 1: Add logo overlay (if exists)
        logo_filter = ""
        if os.path.exists(LOGO_PATH):
            input_count += 1
            logo_filter = f"[0:v][1:v]overlay=W-w-20:20"
            logger.info("   ✓ Adding logo (top-right corner)")
        else:
            logo_filter = "[0:v]"
        
        # Step 2: Add lower-third bar with headline
        if not use_ticker:
            # Static lower-third
            lower_filter = (
                f"drawtext=fontfile={FONT_PATH}:"
                f"text='{headline}':"
                f"fontsize=36:"
                f"fontcolor=white:"
                f"box=1:boxcolor=black@0.7:"
                f"boxborderw=10:"
                f"x=20:y=h-80"
            )
            logger.info(f"   ✓ Adding lower-third: '{headline}'")
        else:
            # Scrolling ticker
            ticker = ticker_text if ticker_text else headline
            lower_filter = (
                f"drawtext=fontfile={FONT_PATH}:"
                f"text='{ticker}':"
                f"fontsize=30:"
                f"fontcolor=yellow:"
                f"x=w-mod(t*150\\,w+tw):"
                f"y=h-50"
            )
            logger.info(f"   ✓ Adding scrolling ticker: '{ticker}'")
        
        # Combine filters
        if os.path.exists(LOGO_PATH):
            filter_complex = f"{logo_filter},{lower_filter}"
        else:
            filter_complex = f"{logo_filter}{lower_filter}"
        
        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_video,
        ]
        
        # Add logo input if it exists
        if os.path.exists(LOGO_PATH):
            cmd.extend(["-i", LOGO_PATH])
        
        cmd.extend([
            "-filter_complex", filter_complex,
            "-c:a", "copy",
            "-preset", "veryfast",
            output_video
        ])
        
        logger.info(f"   Running: ffmpeg with {len(cmd)} arguments")
        
        # Execute FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            logger.error(f"❌ FFmpeg failed: {result.stderr[-500:]}")
            return False
        
        if not os.path.exists(output_video):
            logger.error(f"❌ Output video not created: {output_video}")
            return False
        
        output_size = os.path.getsize(output_video) / (1024 * 1024)
        logger.info(f"✅ Overlay complete: {output_video} ({output_size:.1f} MB)")
        
        return True
        
    except subprocess.TimeoutExpired:
        logger.error(f"❌ FFmpeg timeout (exceeded 5 min)")
        return False
    except Exception as e:
        logger.error(f"❌ Overlay error: {str(e)}")
        return False


def add_lower_third_only(
    input_video: str,
    output_video: str,
    headline: str = "मुख्य बातमी"
) -> bool:
    """
    Add only lower-third bar (no logo).
    Faster alternative when logo not needed.
    
    Args:
        input_video: Path to input video
        output_video: Path to output video
        headline: Lower-third text
    
    Returns:
        True if successful
    """
    return add_overlay(input_video, output_video, headline, use_ticker=False)


def add_ticker_only(
    input_video: str,
    output_video: str,
    ticker_text: str = "ब्रेकिंग न्यूज: महत्वाची माहिती येथे येईल"
) -> bool:
    """
    Add only scrolling ticker at bottom.
    
    Args:
        input_video: Path to input video
        output_video: Path to output video
        ticker_text: Scrolling text
    
    Returns:
        True if successful
    """
    return add_overlay(input_video, output_video, ticker_text, use_ticker=True)


def create_asset_structure():
    """Create recommended asset directory structure"""
    assets_dir = "assets"
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        logger.info(f"✅ Created {assets_dir}/ directory")
    
    logger.info("\n📁 Required assets structure:")
    logger.info(f"""
    {assets_dir}/
    ├── logo.png              # Channel logo (transparent PNG, ~200x200)
    ├── lower_bg.png          # Lower-third background (1920x300 px)
    ├── font.ttf              # Devanagari font (NotoSansDevanagari recommended)
    ├── promo.mp4             # Promo video (5-30 sec)
    └── background.mp4        # Optional background loop
    
    Download fonts:
    - NotoSansDevanagari: https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari
    - Place in {assets_dir}/font.ttf
    """)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test: Create asset structure guide
    create_asset_structure()
    
    # Example 1: Add full overlay (logo + lower-third)
    # result = add_overlay(
    #     "output/raw_video.mp4",
    #     "output/final_video.mp4",
    #     headline="आजच्या मुख्य बातम्या"
    # )
    
    # Example 2: Add only lower-third
    # result = add_lower_third_only(
    #     "output/raw_video.mp4",
    #     "output/final_video.mp4",
    #     headline="लाइव्ह समाचार"
    # )
    
    # Example 3: Add scrolling ticker
    # result = add_ticker_only(
    #     "output/raw_video.mp4",
    #     "output/final_video.mp4",
    #     ticker_text="ब्रेकिंग न्यूज: महत्वाची अपडेट"
    # )
    
    print("\n✅ Overlay engine ready!")
    print("Import this module and use add_overlay() in your pipeline")
