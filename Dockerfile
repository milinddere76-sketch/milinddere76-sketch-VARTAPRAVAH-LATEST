FROM python:3.10-slim

# Install system deps and clean up apt cache in one layer
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    git \
    curl \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python deps with --no-cache-dir to save space
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone Wav2Lip and download models in a single layer to minimize layer size
RUN git clone https://github.com/Rudrabha/Wav2Lip.git && \
    mkdir -p Wav2Lip/checkpoints && \
    curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth" -o Wav2Lip/checkpoints/wav2lip.pth && \
    mkdir -p Wav2Lip/face_detection/detection/sfd && \
    curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/s3fd.pth" -o Wav2Lip/face_detection/detection/sfd/s3fd.pth

# Copy project
COPY . .

# Accept Coqui TTS Terms of Service
ENV COQUI_TOS_AGREED=1

CMD ["python", "app/main.py"]
