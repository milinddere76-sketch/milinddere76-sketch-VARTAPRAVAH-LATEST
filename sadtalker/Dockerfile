FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies (Native ARM64)
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    git ffmpeg cmake build-essential \
    python3-numpy python3-scipy python3-opencv \
    libopenblas-dev liblapack-dev \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# 3. Install Python Deps (Bypass compilation where possible)
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip3 install --no-cache-dir \
    tqdm yacs pyyaml face-alignment facexlib gfpgan \
    librosa imageio imageio-ffmpeg kornia ninja resampy dlib

# 4. Clean up
RUN rm -f requirements.txt && touch requirements.txt

# 5. Prep models directory
RUN mkdir -p checkpoints

CMD ["python3", "inference.py"]
