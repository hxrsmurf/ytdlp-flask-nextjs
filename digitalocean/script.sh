#!/bin/bash

yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output '%(id)s/%(id)s.%(ext)s' https://youtu.be/lZJ56cXSI-o


#!/bin/bash
apt-get update
#apt-get install python pip ffmpeg docker.io -yf
apt-get install python pip ffmpeg -yf
pip install yt-dlp
cd /root/
yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output '%(id)s/%(id)s.%(ext)s' https://youtu.be/RlOB3UALvrQ
cd RlOB3UALvrQ
ffmpeg -i RlOB3UALvrQ.mp4 \
    -c:v libx264 \
    -c:a copy \
    -flags +cgop \
    -g 30 \
    -hls_time 1 \
    -hls_playlist_type event \
    RlOB3UALvrQ.m3u8

#!/bin/bash
apt-get update
apt-get install docker-compose git -yf
git clone https://github.com/hxrsmurf/ytdlp-flask-nextjs
docker pull python:3.10.5-slim
docker pull mongo
docker pull mongo-express
cd ytdlp-flask-nextjs/backend
docker-compose --build

cd ytdlp-flask-nextjs/mongodb
docker-compose up --build -d
cd ytdlp-flask-nextjs/backend
docker-compose up --build

ffmpeg -i VIDEOID.mp4 \
    -c copy \
    -flags +cgop \
    -g 30 \
    -hls_time 1 \
    -hls_playlist_type event \
    VIDEOID.m3u8

docker run -v $(pwd):$(pwd) \
    -w $(pwd) \
    jrottenberg/ffmpeg \
    -i VIDEOID.mp4 \
    -c copy \
    -flags +cgop \
    -g 30 \
    -hls_time 1 \
    -hls_playlist_type event \
    VIDEOID.m3u8

    #######
