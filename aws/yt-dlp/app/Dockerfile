FROM python:3.10-slim as builder

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

FROM builder as app
COPY . /
CMD ["waitress-serve", "app:app" ]