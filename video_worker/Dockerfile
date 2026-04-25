FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

RUN pip3 install --no-cache-dir --disable-pip-version-check \
    requests \
    pydantic \
    moviepy

COPY render.py .

CMD ["python3", "render.py"]
