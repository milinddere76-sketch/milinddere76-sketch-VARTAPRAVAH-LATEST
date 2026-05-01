import os
from app import config

PLAYLIST = "/app/queue/playlist.txt"
VIDEO_DIR = "/app/output"
FALLBACK = "/app/assets/promo.mp4"

def generate_playlist():
    """
    FIX 4: Proactive Playlist Generation.
    BULLETPROOF FIX: Auto-fallback if playlist is missing.
    """
    # 0. BULLETPROOF INITIALISATION: Ensure a playlist always exists
    if not os.path.exists(PLAYLIST):
        print("🛡️ [BULLETPROOF] Playlist missing. Initialising auto-fallback...")
        try:
            os.makedirs(os.path.dirname(PLAYLIST), exist_ok=True)
            with open(PLAYLIST, "w") as f:
                f.write(f"file '{FALLBACK}'\n")
        except Exception as e:
            print(f"⚠️ [BULLETPROOF] Startup repair failed: {e}")

    print("📋 [PLAYLIST] Synchronizing broadcast queue...")
    files = []

    # 1. Scan for fresh news bulletins
    if os.path.exists(VIDEO_DIR):
        # Sort by timestamp to ensure chronological news flow
        all_files = sorted(os.listdir(VIDEO_DIR))
        for f in all_files:
            if f.endswith(".mp4") and "bulletin" in f:
                files.append(f"/app/output/{f}")

    # 2. Inject fallback branding if no news is available
    if not files:
        print("⚠️ [PLAYLIST] No news bulletins found. Injecting fallback promo.")
        files.append(FALLBACK)
    else:
        # Add a promo after every few bulletins for branding continuity
        # This is a 'Pro' version of the fallback logic
        files.insert(0, FALLBACK)

    # 3. Write to the shared handoff directory
    try:
        os.makedirs(os.path.dirname(PLAYLIST), exist_ok=True)
        with open(PLAYLIST, "w") as f:
            for video in files:
                # FFmpeg concat format requires 'file' prefix
                f.write(f"file '{video}'\n")
        print(f"✅ [PLAYLIST] Updated with {len(files)} items.")
    except Exception as e:
        print(f"❌ [PLAYLIST] Error writing playlist: {e}")

if __name__ == "__main__":
    generate_playlist()
