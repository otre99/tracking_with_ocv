FROM python:bullseye

WORKDIR /app
RUN apt update && apt upgrade -y && apt install -y python3-pip

# OpenCV dependences
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .
RUN pip3 install -r ./requirements.txt

CMD ["python3", "-u", "main.py"]
