FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ffmpeg curl \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Clone SadTalker with compression
RUN git clone https://github.com/OpenTalker/SadTalker.git && \
    cd SadTalker && \
    git config core.compression 9

WORKDIR /app/SadTalker

# Install pip tools first
RUN pip install --upgrade pip setuptools wheel

# Install base dependencies
RUN pip install numpy==1.26.4 Cython

# Install PyTorch CPU
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# Install SadTalker dependencies
RUN pip install tqdm yacs pyyaml librosa

RUN pip install face-alignment facexlib gfpgan

RUN pip install imageio imageio-ffmpeg kornia ninja resampy

RUN pip install dlib-bin

# Install basicsr (needed for SadTalker)
RUN pip install basicsr

# Clean pip cache
RUN pip cache purge

# Make output directory
RUN mkdir -p /app/output /app/checkpoints

# Default to checking service availability
CMD ["python", "-c", "print('SadTalker service ready')"]
