FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install transformers

CMD ["gunicorn", "--bind", "0.0.0.0:8443", "app:app"]
