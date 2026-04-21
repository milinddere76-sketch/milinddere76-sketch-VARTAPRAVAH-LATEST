#!/usr/bin/env python3
"""
VARTAPRAVAH - Main Entry Point
Supports two modes:
  1. API Server Mode (FastAPI) - HTTP endpoints
  2. TV Mode (24×7 Scheduler) - Automated bulletins
"""

import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_api_server():
    """Run FastAPI server mode"""
    try:
        logger.info("🚀 Starting VARTAPRAVAH API Server...")
        logger.info("   📍 Server: http://localhost:8000")
        logger.info("   📍 Docs: http://localhost:8000/docs")
        logger.info("   📍 Use HTTP endpoints for manual control")
        
        from api import app
        import uvicorn
        
        # Run FastAPI server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {str(e)}")
        sys.exit(1)


def run_tv_mode():
    """Run TV mode (24×7 automated scheduler)"""
    try:
        logger.info("📺 Starting VARTAPRAVAH 24×7 TV Mode...")
        logger.info("   Mode: Automated bulletin scheduling")
        logger.info("   Bulletins: 5 per day (05:00, 12:00, 17:00, 20:00, 23:00)")
        logger.info("   News cycling with promos and breaking news handling")
        
        from scheduler import start_channel
        
        # Run TV engine
        start_channel()
        
    except KeyboardInterrupt:
        logger.info("\n✅ TV mode stopped by user")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"❌ Failed to start TV mode: {str(e)}")
        sys.exit(1)


def show_usage():
    """Show usage information"""
    print("\n" + "=" * 70)
    print("🎬 VARTAPRAVAH - AI News Avatar Generator")
    print("=" * 70)
    print("\nUSAGE:")
    print("  python app/main.py [MODE]")
    print("\nMODES:")
    print("  api       → FastAPI Server (HTTP endpoints)")
    print("             Usage: python app/main.py api")
    print("             Runs on: http://localhost:8000")
    print("             Docs: http://localhost:8000/docs")
    print("")
    print("  tv        → 24×7 Automated TV Mode")
    print("             Usage: python app/main.py tv")
    print("             Bulletins: 5 per day (05:00, 12:00, 17:00, 20:00, 23:00)")
    print("             Auto loops with promos and breaking news")
    print("")
    print("  demo      → Pipeline Demo (One-time run)")
    print("             Usage: python app/pipeline_demo.py")
    print("")
    print("ENVIRONMENT VARIABLES:")
    print("  NEWSAPI_KEY         - NewsAPI key (required)")
    print("  GROQ_API_KEY        - Groq API key (for AI scripts)")
    print("  YOUTUBE_RTMP_URL    - YouTube RTMP URL (for streaming)")
    print("")
    print("EXAMPLES:")
    print("  # Start API server")
    print("  python app/main.py api")
    print("")
    print("  # Start 24×7 TV mode")
    print("  python app/main.py tv")
    print("")
    print("  # Default (API server)")
    print("  python app/main.py")
    print("=" * 70 + "\n")


def main():
    """Main entry point with mode selection"""
    
    # Get mode from command line
    mode = "api"  # Default mode
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    # Validate mode
    valid_modes = ["api", "tv", "help", "-h", "--help"]
    if mode not in valid_modes:
        logger.error(f"❌ Invalid mode: {mode}")
        show_usage()
        sys.exit(1)
    
    # Show help
    if mode in ["help", "-h", "--help"]:
        show_usage()
        sys.exit(0)
    
    # Run selected mode
    if mode == "api":
        run_api_server()
    elif mode == "tv":
        run_tv_mode()


if __name__ == "__main__":
    main()
