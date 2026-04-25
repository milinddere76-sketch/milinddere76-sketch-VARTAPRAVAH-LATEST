FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    curl \
    fonts-noto \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/output /app/app/assets /app/checkpoints /app/Wav2Lip /app/SadTalker

# Copy requirements
COPY requirements.txt requirements-light.txt ./

# Install pip tools first
RUN pip install --upgrade pip setuptools wheel

# Install requirements
RUN pip install -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONPATH=/app:/app/Wav2Lip:/app/SadTalker

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
