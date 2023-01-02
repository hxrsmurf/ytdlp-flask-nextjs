FROM python:3.10-alpine as builder

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN apk add ffmpeg

FROM builder as app
COPY . /
CMD ["waitress-serve", "app:app" ]