FROM --platform=linux/amd64 jrottenberg/ffmpeg:latest AS ffmpeg-stage
FROM --platform=linux/amd64 python:3.11 AS builder

# Copy only ffmpeg binary and required libraries from ffmpeg stage
COPY --from=ffmpeg-stage /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg-stage /usr/local/lib /usr/local/lib

# Set library path
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget build-essential python3-dev \
    libsndfile1 libsndfile1-dev \
    espeak-ng libespeak-ng1 libespeak-ng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install in stages
COPY requirements.txt .

# Upgrade pip and set binary preference
RUN pip install --upgrade pip setuptools wheel && \
    pip config set global.prefer-binary true && \
    pip cache purge

# Install all Python packages with aggressive cache cleaning
RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.5.0 python-dotenv==1.0.0 \
    requests==2.31.0 feedparser==6.0.10 pillow==10.1.0 ffmpeg-python==0.2.0 \
    apscheduler==3.10.4 groq==0.4.2 wavefile==1.6.3 && \
    pip cache purge

RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    numpy==1.24.3 scipy==1.11.4 librosa==0.10.0 opencv-python==4.8.1.78 && \
    pip cache purge

RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 \
    torch==2.1.2 torchvision==0.16.2 transformers>=5.0.0 && \
    pip cache purge

RUN pip install --no-cache-dir --default-timeout=1000 --retries 5 --prefer-binary TTS==0.22.0 && \
    pip cache purge

# Final stage
FROM --platform=linux/amd64 python:3.11

# Copy ffmpeg binaries and libraries
COPY --from=ffmpeg-stage /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg-stage /usr/local/lib /usr/local/lib
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
RUN ldconfig 2>/dev/null || true

# Copy installed Python packages and all binaries from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git libsndfile1 espeak-ng libespeak-ng1 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p videos temp

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]