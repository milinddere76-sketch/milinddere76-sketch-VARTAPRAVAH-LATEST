import os
import time

while True:
    print("🎬 Rendering video...")

    # Ensure output directory exists
    os.makedirs("/app/output", exist_ok=True)

    # Using the placeholder command provided to ensure the loop works
    os.system("""
    ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=10 \
    -vf "drawtext=text='VartaPravah Live':x=100:y=100:fontsize=40:fontcolor=white" \
    /app/output/output.mp4
    """)

    time.sleep(10)
