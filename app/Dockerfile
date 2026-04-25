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

# Copy requirements
COPY requirements.txt .

# Install pip tools first
RUN pip install --upgrade pip setuptools wheel

# Install build dependencies for audio libraries
RUN pip install Cython numpy==1.24.3

# Install remaining requirements
RUN pip install -r requirements.txt

# Clean pip cache
RUN pip cache purge

# Copy application code
COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
