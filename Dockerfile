FROM python:3.8-alpine

WORKDIR /DockerHanseiFood

COPY requirements.txt .

RUN apk add --no-cache tzdata

ENV TZ=Asia/Seoul

RUN pip install -r requirements.txt

COPY . /DockerHanseiFood

CMD ["python", "./main.py"]
