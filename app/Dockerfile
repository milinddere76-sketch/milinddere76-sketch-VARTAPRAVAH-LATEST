FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg curl gcc build-essential libpq-dev \
    pkg-config libasound2-dev \
    espeak-ng libsndfile1-dev \
    fonts-noto-hinted fonts-noto-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Base Build Tools
RUN pip install --upgrade "pip<24.1" "setuptools<66.0.0" wheel

# 3. Pre-install Audio & AI Stack (The "Pickle" part)
# We install these together to force a valid resolver state
RUN pip install "numpy==1.22.0" Cython pyworld==0.3.4 redis groq

# 4. Heavy AI Frameworks (Cached)
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# 5. Main TTS Engine
RUN pip install --no-cache-dir TTS==0.22.0

# 6. Remaining App Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
COPY . .

# Corrected command: look for main:app directly since we are inside the app folder
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
