FROM python:3.10

# Minimal, stable dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/OpenTalker/SadTalker.git
WORKDIR /app/SadTalker

# Use pre-built wheels for everything
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "inference.py"]
