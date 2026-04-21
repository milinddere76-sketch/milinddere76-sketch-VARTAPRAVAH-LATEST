#!/usr/bin/env python3
"""
🎬 VARTAPRAVAH Setup Script - Parts 1 & 2 (Overlays + Recovery)

This script verifies and sets up:
1. Overlay engine (app/overlay.py)
2. Streaming recovery (app/streamer.py)
3. Asset structure
4. System dependencies
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Add app directory to path for imports
app_path = os.path.join(os.getcwd(), "app")
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Colors for output (disable on Windows CMD for safety)
USE_COLORS = sys.platform != 'win32'
GREEN = '\033[92m' if USE_COLORS else ''
YELLOW = '\033[93m' if USE_COLORS else ''
RED = '\033[91m' if USE_COLORS else ''
BLUE = '\033[94m' if USE_COLORS else ''
RESET = '\033[0m' if USE_COLORS else ''

class SetupChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
    
    def check_python_version(self):
        """Verify Python 3.8+"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self.success.append(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
        else:
            self.errors.append(f"[FAIL] Python 3.8+ required (found {version.major}.{version.minor})")
    
    def check_files_exist(self):
        """Verify core files are in place"""
        required_files = [
            "app/overlay.py",
            "app/streamer.py",
            "app/scheduler.py",
            "app/api.py",
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                size_kb = os.path.getsize(file_path) / 1024
                self.success.append(f"[OK] {file_path} ({size_kb:.1f} KB)")
            else:
                self.errors.append(f"[FAIL] {file_path} not found")
    
    def check_imports(self):
        """Verify Python imports work"""
        try:
            import overlay
            self.success.append("[OK] overlay module imports successfully")
        except ImportError as e:
            self.errors.append(f"[ERROR] overlay import failed: {e}")
        
        try:
            import streamer
            self.success.append("[OK] streamer module imports successfully")
        except ImportError as e:
            self.errors.append(f"[ERROR] streamer import failed: {e}")
    
    def check_ffmpeg(self):
        """Verify FFmpeg is installed"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Extract version
                version_line = result.stdout.split('\n')[0]
                self.success.append(f"[OK] FFmpeg installed: {version_line}")
            else:
                self.errors.append("[FAIL] FFmpeg not working properly")
        except FileNotFoundError:
            self.errors.append("[FAIL] FFmpeg not found (install: apt-get install ffmpeg)")
    
    def check_assets(self):
        """Check asset structure"""
        assets_dir = "assets"
        
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            logger.info(f"[INFO] Created {assets_dir}/ directory")
        
        # Check font
        font_path = "assets/font.ttf"
        if os.path.exists(font_path):
            size = os.path.getsize(font_path) / (1024*1024)
            self.success.append(f"[OK] Font file found: assets/font.ttf ({size:.1f} MB)")
        else:
            self.warnings.append(f"[WARN] Font not found: assets/font.ttf (Marathi text may not display)")
        
        # Check logo
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            size = os.path.getsize(logo_path) / 1024
            self.success.append(f"[OK] Logo found: assets/logo.png ({size:.1f} KB)")
        else:
            self.warnings.append(f"[WARN] Logo not found: assets/logo.png (channel logo won't appear)")
        
        # Check promo
        promo_path = "assets/promo.mp4"
        if os.path.exists(promo_path):
            size = os.path.getsize(promo_path) / (1024*1024)
            self.success.append(f"[OK] Promo video found: assets/promo.mp4 ({size:.1f} MB)")
        else:
            self.warnings.append(f"[WARN] Promo not found: assets/promo.mp4 (no promos between stories)")
    
    def check_output_dir(self):
        """Ensure output directory exists"""
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.success.append(f"[OK] Created output/ directory")
        else:
            self.success.append(f"[OK] output/ directory exists")
    
    def check_environment(self):
        """Verify environment variables"""
        env_vars = ["NEWSAPI_KEY", "GROQ_API_KEY", "YOUTUBE_RTMP_URL"]
        
        for var in env_vars:
            if os.getenv(var):
                value = os.getenv(var)
                masked = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
                self.success.append(f"[OK] {var} = {masked}")
            else:
                self.warnings.append(f"[WARN] {var} not set (required for streaming)")
    
    def run_all_checks(self):
        """Run all checks"""
        logger.info(f"\n{BLUE}{'='*60}")
        logger.info("🎬 VARTAPRAVAH Setup Verification")
        logger.info(f"{'='*60}{RESET}\n")
        
        logger.info(f"{BLUE}[1/7] Checking Python...{RESET}")
        self.check_python_version()
        
        logger.info(f"{BLUE}[2/7] Checking core files...{RESET}")
        self.check_files_exist()
        
        logger.info(f"{BLUE}[3/7] Checking imports...{RESET}")
        self.check_imports()
        
        logger.info(f"{BLUE}[4/7] Checking FFmpeg...{RESET}")
        self.check_ffmpeg()
        
        logger.info(f"{BLUE}[5/7] Checking assets...{RESET}")
        self.check_assets()
        
        logger.info(f"{BLUE}[6/7] Checking output directory...{RESET}")
        self.check_output_dir()
        
        logger.info(f"{BLUE}[7/7] Checking environment variables...{RESET}")
        self.check_environment()
        
        self.print_results()
    
    def print_results(self):
        """Print summary"""
        logger.info(f"\n{BLUE}{'='*60}")
        logger.info("Results")
        logger.info(f"{'='*60}{RESET}\n")
        
        for msg in self.success:
            logger.info(f"{GREEN}{msg}{RESET}")
        
        if self.warnings:
            logger.info("")
            for msg in self.warnings:
                logger.info(f"{YELLOW}{msg}{RESET}")
        
        if self.errors:
            logger.info("")
            for msg in self.errors:
                logger.info(f"{RED}{msg}{RESET}")
        
        # Summary
        logger.info(f"\n{BLUE}Summary:{RESET}")
        logger.info(f"  [OK] Success: {len(self.success)}")
        logger.info(f"  [WARN] Warnings: {len(self.warnings)}")
        logger.info(f"  [FAIL] Errors: {len(self.errors)}")
        
        # Status
        if self.errors:
            logger.info(f"\n{RED}[FAIL] Setup incomplete - fix errors above{RESET}")
            return False
        elif self.warnings:
            logger.info(f"\n{YELLOW}[WARN] Setup ready but some features may be limited{RESET}")
            return True
        else:
            logger.info(f"\n{GREEN}[OK] Setup complete and verified!{RESET}")
            return True
    
    def print_next_steps(self):
        """Print next steps"""
        logger.info(f"\n{BLUE}{'='*60}")
        logger.info("🚀 Next Steps")
        logger.info(f"{'='*60}{RESET}\n")
        
        if not os.path.exists("assets/font.ttf"):
            logger.info(f"{YELLOW}1. Download Devanagari font:{RESET}")
            logger.info("   wget https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf -O assets/font.ttf")
            logger.info("")
        
        if not os.path.exists("assets/logo.png"):
            logger.info(f"{YELLOW}2. Create channel logo:{RESET}")
            logger.info("   • Use Canva (free): https://www.canva.com")
            logger.info("   • Or GIMP (free): https://www.gimp.org")
            logger.info("   • Dimensions: 200×200 pixels")
            logger.info("   • Format: PNG with transparent background")
            logger.info("   • Save to: assets/logo.png")
            logger.info("")
        
        logger.info(f"{BLUE}3. Set environment variables:{RESET}")
        logger.info("   export NEWSAPI_KEY='your_key'")
        logger.info("   export GROQ_API_KEY='gsk_your_key'")
        logger.info("   export YOUTUBE_RTMP_URL='rtmp://...'")
        logger.info("")
        
        logger.info(f"{BLUE}4. Start TV mode:{RESET}")
        logger.info("   python app/main.py tv")
        logger.info("")
        
        logger.info(f"{BLUE}5. Monitor progress:{RESET}")
        logger.info("   tail -f vartapravah.log")
        logger.info("")


def main():
    """Run setup verification"""
    checker = SetupChecker()
    checker.run_all_checks()
    
    # Print next steps if setup is ready
    if len(checker.errors) == 0:
        checker.print_next_steps()
    
    # Exit code
    sys.exit(0 if len(checker.errors) == 0 else 1)


if __name__ == "__main__":
    main()
