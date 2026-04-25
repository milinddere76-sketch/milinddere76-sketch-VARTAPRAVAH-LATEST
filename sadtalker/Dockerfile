FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    git ffmpeg cmake build-essential wget curl \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Clone SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# 3. Base Build Tools
RUN pip install --upgrade pip setuptools wheel
RUN pip install "numpy==1.26.4" Cython

# 4. Heavy AI Frameworks (CPU Optimized)
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# 5. SadTalker Specific AI Tools (Forced NumPy Stability)
# We use --no-build-isolation to prevent them from pulling NumPy 2.0
RUN pip install --no-cache-dir --no-build-isolation \
    tqdm yacs pyyaml face-alignment facexlib gfpgan \
    librosa imageio imageio-ffmpeg kornia ninja resampy \
    dlib-bin

# 6. Patch basicsr (Compatibility Fix)
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g" $(python -c 'import basicsr; print(basicsr.__path__[0])')/data/degradations.py || true

# 7. Prep models
RUN mkdir -p checkpoints && bash scripts/download_models.sh

CMD ["python", "inference.py", "--cpu"]
