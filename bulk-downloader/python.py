import argparse
import yt_dlp
import time
import redis

parser = argparse.ArgumentParser()
parser.add_argument("--channel", "-c")
args = parser.parse_args()

ytdl_opts = {
    'outtmpl' : '/mnt/videos/%(uploader)s/%(id)s.%(ext)s',
    'windowsfilenames': True,
    'playlistend' : 1,
    'ignoreerrors' : True,
    'format': 'bestvideo*+bestaudio/best',
    'merge_output_format': 'mp4'
}

r = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)

pub = r.pubsub()
pub.subscribe('queue')

while True:
    message = pub.get_message()

    if message:
        # Have to do try/except to ensure python stays alive
        try:
            message_json = message['data']
            print(message_json)

            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                ydl.extract_info(message_json, download=True)
        except:
            print('No messages')