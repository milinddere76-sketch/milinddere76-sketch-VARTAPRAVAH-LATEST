FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install required system libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -vvv

COPY render.py .

CMD ["python", "render.py"]
