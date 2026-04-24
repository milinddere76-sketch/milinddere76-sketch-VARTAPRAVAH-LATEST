FROM ubuntu:22.04

# Fix for non-interactive apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and Essentials using the Native Ubuntu Repos
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# Use python3 and ensure pip is ready
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "inference.py"]
