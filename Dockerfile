FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    git \
    curl \
    libsndfile1 \
    espeak-ng \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Step 1: Install pip & light requirements
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN sed -i '/TTS/d' requirements.txt && \
    sed -i '/transformers/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Step 2: Install Torch (CPU)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Step 3: Install heavy AI components
RUN pip install --no-cache-dir transformers>=4.34.0
RUN pip install --no-cache-dir TTS>=0.22.0

# Step 4: Wav2Lip Setup
RUN git clone https://github.com/Rudrabha/Wav2Lip.git && \
    mkdir -p Wav2Lip/checkpoints && \
    curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth" -o Wav2Lip/checkpoints/wav2lip.pth && \
    mkdir -p Wav2Lip/face_detection/detection/sfd && \
    curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/s3fd.pth" -o Wav2Lip/face_detection/detection/sfd/s3fd.pth

# Copy project
COPY . .

# Environment
ENV COQUI_TOS_AGREED=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py", "tv"]
