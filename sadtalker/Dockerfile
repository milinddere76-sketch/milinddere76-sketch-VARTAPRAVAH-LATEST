FROM python:3.10

RUN apt update && apt install -y git ffmpeg

WORKDIR /app

RUN git clone https://github.com/OpenTalker/SadTalker.git

WORKDIR /app/SadTalker

RUN pip install -r requirements.txt

CMD ["python", "inference.py"]
