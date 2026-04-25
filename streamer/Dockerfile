FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the stream script
COPY stream.sh /app/stream.sh
RUN chmod +x /app/stream.sh

# Copy LOCAL assets for fallback if Hetzner fails
COPY assets /app/assets

CMD ["/bin/bash", "/app/stream.sh"]
