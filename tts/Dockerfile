FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install only runtime dependencies - espeak is needed for TTS
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Install TTS and dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install TTS && \
    pip cache purge

COPY tts.py .

CMD ["python3", "tts.py"]
