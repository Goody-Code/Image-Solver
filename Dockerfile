FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install transformers==4.28.0

CMD ["gunicorn", "--bind", "0.0.0.0:8443", "--workers", "4", "--timeout", "300", "app:app"]
