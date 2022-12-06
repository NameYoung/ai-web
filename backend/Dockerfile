FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "cd ./src;python3 -m uvicorn main:app --host=0.0.0.0 --port=8000"]
