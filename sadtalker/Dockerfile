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

# 🔥 ULTIMATE FIX: remove ALL torch-related packages from requirements.txt
RUN sed -i '/torch/d' requirements.txt && \
    sed -i '/torchvision/d' requirements.txt && \
    sed -i '/torchaudio/d' requirements.txt

# Install opencv-headless (Stable on ARM64)
RUN pip install --no-cache-dir opencv-python-headless

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download pretrained models (REQUIRED)
RUN mkdir -p checkpoints

CMD ["python3", "inference.py"]
