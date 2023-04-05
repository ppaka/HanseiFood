FROM python:3.8-alpine

WORKDIR /HanseiFood

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./main.py"]