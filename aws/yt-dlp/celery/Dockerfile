FROM python:3.10-alpine as builder

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN apk add ffmpeg

FROM builder as app
COPY . /app
WORKDIR /app
CMD ["python", "-m", "celery", "-A", "app.app_celery", "worker"]