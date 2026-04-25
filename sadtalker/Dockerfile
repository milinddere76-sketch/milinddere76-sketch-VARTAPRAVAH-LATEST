FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies (Optimized for CPU)
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    git ffmpeg cmake build-essential wget curl \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# 3. Install Python Deps (Hardened & CPU Optimized)
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install "numpy==1.26.4" Cython
RUN pip3 install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir \
    tqdm yacs pyyaml face-alignment facexlib gfpgan \
    librosa imageio imageio-ffmpeg kornia ninja resampy \
    dlib-bin

# 4. Patch basicsr (Fix for torchvision 0.15+ compatibility)
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g" /usr/local/lib/python3.10/dist-packages/basicsr/data/degradations.py

# 4. Clean up
RUN rm -f requirements.txt && touch requirements.txt

# 5. Prep models directory & Download Checkpoints
RUN mkdir -p checkpoints
RUN bash scripts/download_models.sh

CMD ["python3", "inference.py", "--cpu"]
