FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    espeak-ng \
    libsndfile1 \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt requirements-light.txt ./

# Install pip tools first
RUN pip install --upgrade pip setuptools wheel

# Install core dependencies separately
RUN pip install numpy==1.22.0 Cython pyworld==0.3.4

# Install audio/ML dependencies
RUN pip install redis groq librosa

# Install PyTorch CPU (may be slow, but reliable)
RUN pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# Install TTS
RUN pip install TTS

# Install remaining requirements
RUN pip install -r requirements.txt

# Clean pip cache
RUN pip cache purge

# Copy application code
COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
