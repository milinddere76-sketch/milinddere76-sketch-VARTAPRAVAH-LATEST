FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Combine all apt-get operations in single RUN to reduce layers
# Remove unnecessary -dev packages and build tools not needed at runtime
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
RUN mkdir -p /app/output /app/app/assets /app/checkpoints /app/Wav2Lip /app/SadTalker && \
    find /app -type d -exec chmod 755 {} \;

# Copy requirements early
COPY requirements.txt requirements-light.txt ./

# Install Python dependencies efficiently
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt && \
    pip cache purge

COPY . .

ENV PYTHONPATH=/app:/app/Wav2Lip:/app/SadTalker

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
