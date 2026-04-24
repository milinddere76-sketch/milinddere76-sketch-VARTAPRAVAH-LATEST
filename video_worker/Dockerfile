FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    ffmpeg python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY render.py .

CMD ["python3", "render.py"]
