FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg curl gcc build-essential libpq-dev \
    pkg-config libasound2-dev \
    espeak-ng libsndfile1-dev \
    fonts-noto-hinted fonts-noto-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# 1. Base Build Tools
RUN pip3 install --upgrade "pip<24.1" "setuptools<66.0.0" wheel

# 2. Heavy AI Frameworks (Cached)
RUN pip3 install --no-cache-dir torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# 3. Audio, Queue & AI Deps (Cached)
RUN pip3 install "numpy==1.22.0" Cython pyworld==0.3.4 redis groq

# 4. Main TTS Engine (Forced NumPy 1.22.0)
RUN pip3 install --no-cache-dir TTS "numpy==1.22.0"

# 5. Remaining App Requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
COPY . .

# Corrected command: look for main:app directly since we are inside the app folder
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
