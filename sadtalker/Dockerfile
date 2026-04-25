FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install only runtime dependencies - remove cmake, build-essential, wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ffmpeg curl \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git && \
    cd SadTalker && \
    git config core.compression 9

WORKDIR /app/SadTalker

# Install Python dependencies in single RUN layer
RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.26.4 Cython && \
    pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-build-isolation \
      tqdm yacs pyyaml face-alignment facexlib gfpgan \
      librosa imageio imageio-ffmpeg kornia ninja resampy \
      dlib-bin && \
    pip cache purge

# 6. Patch basicsr (Compatibility Fix)
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g" $(python -c 'import basicsr; print(basicsr.__path__[0])')/data/degradations.py || true

# 7. Prep models
RUN mkdir -p checkpoints && bash scripts/download_models.sh

CMD ["python", "inference.py", "--cpu"]
