FROM python:3.10-slim

# 1. Install EVERYTHING needed for AI, Video, and Compiling
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    cmake \
    pkg-config \
    libboost-all-dev \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libavutil-dev \
    libswresample-dev \
    libswscale-dev \
    libavfilter-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Clone the repo
RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# 3. Pre-install build tools and CPU Torch (to ensure compatibility and save RAM)
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4. Install the rest
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "inference.py"]
