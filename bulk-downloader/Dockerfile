FROM python:alpine
RUN pip3 install yt-dlp
RUN apk add ffmpeg
COPY python.py python.py
ENTRYPOINT [ "python3", "python.py" ]