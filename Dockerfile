FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    curl \
    fontconfig \
    fonts-noto-hinted \
    fonts-noto-extra \
    libfreetype6-dev \
    gcc \
    python3-dev \
    git \
    libsm6 \
    libxext6 \
    libxrender-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/output /app/app/assets /app/checkpoints /app/Wav2Lip /app/SadTalker

# Install main requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Wav2Lip Integration ---
RUN git clone https://github.com/Rudrabha/Wav2Lip.git /app/Wav2Lip
WORKDIR /app/Wav2Lip
RUN sed -i 's/==/>=/g' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# --- SadTalker Integration ---
WORKDIR /app
RUN git clone https://github.com/OpenTalker/SadTalker.git /app/SadTalker
WORKDIR /app/SadTalker
# Installing SadTalker dependencies (skipping torch/torchvision as they are heavy and should be handled by host/base image)
RUN pip install --no-cache-dir -r requirements.txt
# Install GFPGAN for professional face enhancement
RUN pip install gfpgan

WORKDIR /app
COPY . .

ENV PYTHONPATH=/app:/app/Wav2Lip:/app/SadTalker

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
