FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

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

# Create necessary directories
RUN mkdir -p /app/output /app/app/assets /app/checkpoints /app/Wav2Lip /app/SadTalker

# Copy requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt -vvv

# Copy application code
COPY . .

ENV PYTHONPATH=/app:/app/Wav2Lip:/app/SadTalker

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
