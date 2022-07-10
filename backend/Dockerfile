from python:3.10.5-slim

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

COPY . /app

EXPOSE 5000

RUN chmod +x ./app/gunicorn.sh

ENTRYPOINT ["./app/gunicorn.sh"]
