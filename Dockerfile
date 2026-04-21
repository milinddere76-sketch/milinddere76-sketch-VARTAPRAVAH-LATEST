# =========================
# BASE IMAGE (Debian - STABLE)
# =========================
FROM python:3.11-slim

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version || (echo "FFmpeg installation failed" && exit 1)

# Verify ffmpeg is at /usr/bin/ffmpeg
RUN test -x /usr/bin/ffmpeg || (echo "FFmpeg not found at /usr/bin/ffmpeg" && exit 1)

# =========================
# WORKDIR
# =========================
WORKDIR /app

# =========================
# COPY REQUIREMENTS (OPTIONAL)
# =========================
COPY requirements.txt .

# =========================
# UPGRADE PIP
# =========================
RUN pip install --upgrade pip setuptools wheel

# =========================
# INSTALL CORE PACKAGES
# =========================
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pydantic==2.5.0 \
    python-dotenv==1.0.0 \
    requests==2.31.0 \
    feedparser==6.0.10 \
    pillow==10.1.0 \
    apscheduler==3.10.4 \
    groq==0.4.2

# =========================
# INSTALL AI / AUDIO / VIDEO LIBS
# =========================
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    numba==0.57.1 \
    llvmlite==0.40.1 \
    librosa==0.10.0 \
    opencv-python-headless==4.8.1.78

# =========================
# INSTALL PYTORCH (CPU)
# =========================
RUN pip install --no-cache-dir \
    torch==2.1.2 \
    torchvision==0.16.2 \
    --index-url https://download.pytorch.org/whl/cpu

# =========================
# INSTALL TTS
# =========================
RUN pip install --no-cache-dir TTS==0.22.0

# =========================
# COPY APP
# =========================
COPY . .

# =========================
# CREATE DIRECTORIES
# =========================
RUN mkdir -p videos temp logs assets/anchors assets/fonts assets/graphics

# =========================
# EXPOSE PORT
# =========================
EXPOSE 8000

# =========================
# HEALTHCHECK
# =========================
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# =========================
# START APP
# =========================
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]