FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in single layer - remove -dev packages not needed at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    espeak-ng \
    libsndfile1 \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.22.0 Cython pyworld==0.3.4 redis groq && \
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install TTS==0.22.0 && \
    pip install -r requirements.txt && \
    pip cache purge

# Copy application code
COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
