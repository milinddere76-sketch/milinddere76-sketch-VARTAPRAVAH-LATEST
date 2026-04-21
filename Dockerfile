FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Clone Wav2Lip repository
RUN git clone https://github.com/Rudrabha/Wav2Lip.git

# Create checkpoints directory
RUN mkdir -p Wav2Lip/checkpoints

# Download Wav2Lip model
RUN cd Wav2Lip/checkpoints && \
    curl -L "https://github.com/Rudrabha/Wav2Lip/releases/download/checkpoints/wav2lip.pth" -o wav2lip.pth

# Copy project
COPY . .

CMD ["python", "app/main.py"]
