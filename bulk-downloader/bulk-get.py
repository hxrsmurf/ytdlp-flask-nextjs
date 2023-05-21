import argparse
import yt_dlp
import time
import redis

parser = argparse.ArgumentParser()
args = parser.parse_args()

ytdl_opts = {
    'outtmpl' : '/mnt/videos/%(uploader)s/%(title)s-%(id)s.%(ext)s',
    'windowsfilenames': True,
    #'playlistend' : 2,
    'ignoreerrors' : True,
    'quiet' : True,
    'format': 'bestvideo*+bestaudio/best',
    'merge_output_format': 'mp4'
}

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


channel = "https://www.youtube.com/@MichelleKhare"

with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
    info = ydl.extract_info(channel, download=False)
    entries = info['entries']
    for entry in entries:
        for e in entry['entries']:
            video = e['webpage_url']
            r.publish('queue', video)
