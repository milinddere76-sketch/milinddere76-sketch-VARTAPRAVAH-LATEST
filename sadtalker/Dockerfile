FROM python:3.10-slim

# 1. Install Native ARM64 System Libraries (Permanent Solve)
RUN apt-get update && apt-get install -y \
    git ffmpeg curl wget build-essential cmake \
    libopenblas-dev liblapack-dev \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# 3. Permanent Dependency Solve (Manual Curated List for ARM64)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir \
    numpy==1.24.3 \
    opencv-python-headless \
    pillow \
    scipy \
    tqdm \
    yacs \
    pyyaml \
    dlib \
    face-alignment \
    facexlib \
    gfpgan \
    librosa \
    imageio \
    imageio-ffmpeg \
    kornia \
    ninja \
    resampy

# 4. Clean up any conflicting requirements
RUN rm requirements.txt && touch requirements.txt

# 5. Prep models directory
RUN mkdir -p checkpoints

CMD ["python3", "inference.py"]
