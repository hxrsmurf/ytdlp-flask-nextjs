FROM python:latest

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./functions.py functions.py
COPY ./subscriber.py subscriber.py

CMD ["python3", "-u", "subscriber.py"]