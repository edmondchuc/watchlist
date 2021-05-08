FROM python:3.9.5-alpine

RUN apk update

RUN apk add --no-cache gcc libffi-dev build-base

RUN pip3 install --no-cache-dir --upgrade pip setuptools

WORKDIR /app

ADD tmdb_api/ tmdb_api/
ADD watchlist/ watchlist/
COPY requirements.txt .
COPY run.py .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP=run:app

RUN flask db init && \
    flask db migrate && \
    flask db upgrade

RUN chown -R 1000:1000 /app
USER 1000

ENTRYPOINT gunicorn --workers=1 --threads=1 --forwarded-allow-ips=* --bind=0.0.0.0:5000 --log-level=info run:app