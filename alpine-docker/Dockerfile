FROM python:alpine
RUN pip install yt-dlp
RUN pip install ffmpeg
RUN apk update
RUN apk add ffmpeg
WORKDIR /media
ENTRYPOINT ["yt-dlp"]