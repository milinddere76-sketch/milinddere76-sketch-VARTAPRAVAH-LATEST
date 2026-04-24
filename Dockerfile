FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    curl \
    fontconfig \
    fonts-noto-hinted \
    fonts-noto-extra \
    libfreetype6-dev \
    gcc \
    python3-dev \
    git \
    libsm6 \
    libxext6 \
    libxrender-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/output /app/app/assets /app/checkpoints /app/Wav2Lip /app/SadTalker

# Allow switching between standard and lightweight requirements
ARG REQS_FILE=requirements.txt
COPY requirements.txt requirements-light.txt .
RUN pip install --no-cache-dir -r ${REQS_FILE}

# Wav2Lip is handled by dedicated workers

# SadTalker is handled by Dockerfile.sadtalker

WORKDIR /app
COPY . .

ENV PYTHONPATH=/app:/app/Wav2Lip:/app/SadTalker

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
