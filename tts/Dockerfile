FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install build tools needed for TTS on ARM64
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    espeak-ng \
    ffmpeg \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install TTS
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir TTS

COPY tts.py .

CMD ["python3", "tts.py"]
