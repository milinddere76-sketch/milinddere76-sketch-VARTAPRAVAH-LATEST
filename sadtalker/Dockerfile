FROM python:3.10-slim

# Install system dependencies (CRITICAL)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    curl \
    wget \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git

WORKDIR /app/SadTalker

# Upgrade pip tools
RUN pip install --upgrade pip setuptools wheel

# Install torch FIRST (CPU stable)
RUN pip install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    torchaudio==2.1.0 \
    --index-url https://download.pytorch.org/whl/cpu

# 🔥 DIAGNOSTIC FIX: Clean requirements and install ONE BY ONE
RUN sed -i '/torch/d' requirements.txt && \
    sed -i '/torchvision/d' requirements.txt && \
    sed -i '/torchaudio/d' requirements.txt

# Pre-install stable ARM64 versions of problematic libs
RUN pip install --no-cache-dir opencv-python-headless scipy numpy

# Attempt one-by-one install to find the culprit
RUN while read p; do pip install "$p" || exit 1; done < requirements.txt

# Download pretrained models
RUN mkdir -p checkpoints

CMD ["python3", "inference.py"]
