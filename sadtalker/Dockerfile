FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install required system libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone SadTalker with compression
RUN git clone https://github.com/OpenTalker/SadTalker.git && \
    cd SadTalker && \
    git config core.compression 9

WORKDIR /app/SadTalker

# Copy requirements
COPY requirements.txt .

# Install Python dependencies from requirements file
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt || cat /root/.cache/pip/log/debug.log

# Make output directory
RUN mkdir -p /app/output /app/checkpoints

# Default command
CMD ["python", "-c", "print('SadTalker service ready')"]
