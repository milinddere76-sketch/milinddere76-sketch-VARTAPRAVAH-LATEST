FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy the stream script
COPY stream.sh /app/stream.sh
RUN chmod +x /app/stream.sh

# Copy LOCAL assets for fallback if Hetzner fails
COPY assets /app/assets

CMD ["/bin/bash", "/app/stream.sh"]
