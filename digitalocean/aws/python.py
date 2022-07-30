import base64

video_id = ''

data = f'\
#!/bin/bash\n\
apt-get update\n\
#apt-get install python pip ffmpeg docker.io -yf\n\
apt-get install python pip ffmpeg -yf\n\
pip install yt-dlp\n\
cd /root/\n\
yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output \'%(id)s/%(id)s.%(ext)s\' https://youtu.be/{video_id}\n\
cd {video_id}\n\
ffmpeg -i {video_id}.mp4 \
    -c:v libx264 \
    -c:a copy \
    -flags +cgop \
    -g 30 \
    -hls_time 1 \
    -hls_playlist_type event \
    {video_id}.m3u8'

encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
print(encodedStr)