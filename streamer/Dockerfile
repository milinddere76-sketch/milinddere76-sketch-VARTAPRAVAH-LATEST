FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY stream.sh /stream.sh
RUN chmod +x /stream.sh

CMD ["/bin/bash", "/stream.sh"]
