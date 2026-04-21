FROM --platform=linux/amd64 python:3.11-alpine AS builder

# Install minimal build dependencies using apk (Alpine package manager - more reliable)
RUN apk add --no-cache --update \
    gcc musl-dev linux-headers \
    git wget curl \
    ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install Python packages - remove problematic ones
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.5.0 python-dotenv==1.0.0 \
    requests==2.31.0 feedparser==6.0.10 pillow==10.1.0 \
    apscheduler==3.10.4 groq==0.4.2 && \
    pip cache purge

RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    numpy==1.24.3 librosa==0.10.0 opencv-python==4.8.1.78 && \
    pip cache purge

# Install PyTorch CPU-only (smaller footprint)
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu && \
    pip cache purge

# Install TTS
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 TTS==0.22.0 && \
    pip cache purge

# Final stage - minimal runtime image
FROM --platform=linux/amd64 python:3.11-alpine

# Install only essential runtime dependencies using apk
RUN apk add --no-cache --update \
    git curl \
    ffmpeg

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p videos temp logs assets/anchors assets/fonts assets/graphics

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]