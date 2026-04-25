FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including LLVM for numba/llvmlite
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    espeak-ng \
    ffmpeg \
    python3-dev \
    llvm \
    llvm-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install build tools
RUN pip3 install --upgrade pip setuptools wheel

# Install TTS (this will take time on ARM64 as it compiles dependencies)
RUN pip3 install --no-cache-dir TTS

COPY tts.py .

CMD ["python3", "tts.py"]
