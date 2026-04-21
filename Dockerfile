FROM python:3.10-slim

# Install system deps
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

# Install Python deps
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy project files
COPY requirements.txt .
RUN pip install -r requirements.txt

# Clone Wav2Lip repository
RUN git clone https://github.com/Rudrabha/Wav2Lip.git

# Create checkpoints directory
RUN mkdir -p Wav2Lip/checkpoints

# Download Wav2Lip models from reliable GitHub release mirrors
RUN curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth" -o Wav2Lip/checkpoints/wav2lip.pth
RUN mkdir -p Wav2Lip/face_detection/detection/sfd && \
    curl -L "https://github.com/justinjohn0306/Wav2Lip/releases/download/models/s3fd.pth" -o Wav2Lip/face_detection/detection/sfd/s3fd.pth

# Copy project
COPY . .

# Accept Coqui TTS Terms of Service
ENV COQUI_TOS_AGREED=1

CMD ["python", "app/main.py"]
