import redis
import json
import time
import os
import shutil
from datetime import datetime, timedelta
import config
from services.news_fetcher import fetch_news
from services.script_generator import generate_script
from services.fact_checker import is_verified

# Using config for flexibility
r = redis.Redis(host=config.REDIS_HOST, port=int(config.REDIS_PORT))

# --- AUTO GENDER SWITCH LOGIC ---
is_female = True

def get_next_anchor():
    global is_female
    selected = "female" if is_female else "male"
    is_female = not is_female
    return selected

def cleanup_temp_files():
    """
    Cleans up the output directory to prevent disk overflow.
    Removes files older than 6 hours.
    Equivalent to user's 'rm -rf /tmp/*' logic but for the project scope.
    """
    print("🧹 [CLEANUP] Purging old temp files from output directory...")
    now = time.time()
    for f in os.listdir(config.OUTPUT_DIR):
        file_path = os.path.join(config.OUTPUT_DIR, f)
        # Delete if older than 6 hours (21600 seconds)
        if os.stat(file_path).st_mtime < now - 21600:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {f}")
            except Exception as e:
                print(f"⚠️ Failed to delete {f}: {e}")

def get_bulletin_type():
    hour = datetime.now().hour
    if 5 <= hour < 10: return "सकाळ"
    elif 10 <= hour < 14: return "दुपार"
    elif 14 <= hour < 18: return "संध्याकाळ"
    elif 18 <= hour < 22: return "प्राइम टाइम"
    else: return "रात्री"

def main():
    print("🏢 [ENTERPRISE] VARTAPRAVAH TV Master Scheduler Active.")

    while True:
        try:
            # 0. Clean up old production artifacts
            cleanup_temp_files()
            
            bulletin_type = get_bulletin_type()
            print(f"🕒 [SCHEDULER] Slot: {bulletin_type}")
            
            articles = fetch_news()
            verified_articles = []

            for article in articles:
                title = article["title"] if isinstance(article, dict) else article
                if not is_verified(title):
                    print(f"❌ Skipping unverified news: {title[:50]}")
                    continue
                verified_articles.append(title)

            if verified_articles:
                news_text = "\n".join(verified_articles)
                anchor_type = get_next_anchor()
                
                prompt = f"""
तुम्ही व्यावसायिक मराठी न्यूज अँकर आहात. ({anchor_type.upper()} ANCHOR)

बुलेटिन: {bulletin_type}

नियम:
- शुद्ध मराठी भाषा
- कोणतीही इंग्रजी शब्द नाही
- न्यूज शैली

न्यूज:
{news_text}
"""
                print(f"✍️ [ENTERPRISE] Generating {bulletin_type} script for {anchor_type.upper()} anchor...")
                script = generate_script(prompt)

                if script:
                    r.rpush(config.QUEUE_NAME, json.dumps({
                        "id": int(time.time()),
                        "type": bulletin_type,
                        "anchor_type": anchor_type,
                        "script": script
                    }))
                    print(f"✅ [{anchor_type.upper()}] {bulletin_type} Bulletin queued.")

            # 15-minute cycle
            time.sleep(900)

        except Exception as e:
            print(f"⚠️ [SCHEDULER] Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
