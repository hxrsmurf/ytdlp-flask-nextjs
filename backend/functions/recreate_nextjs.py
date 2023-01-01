import requests
import logging
import redis
import json
import yt_dlp

logging.basicConfig(level='INFO')

recreate_file = 'recreate.txt'
api_url = 'http://localhost:3000/api/addChannel?id='
list_channels = []

r = redis.Redis(
    host='localhost',
    port='6379'
)

def get_channel(channel):
    ydl_opts = {
        'playlistend': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel, download=False)
            profile = info['thumbnails'][18]['url'],
            cover = info['thumbnails'][15]['url'],
        except Exception as e:
            logging.error(channel, e)
    return cover, profile

with open(recreate_file, 'r') as file:
    for line in file.readlines():
        channel = line.strip()
        check_valid_channel = False

        if check_valid_channel:
            result = requests.get(channel)
            status_code = result.status_code
            if status_code == 404:
                print(channel)
        else:
            cover, profile = get_channel(channel)
            list_channels.append({
                'url': channel,
                'cover': cover,
                'profile': profile
            })

try:
    r.set('channels', json.dumps(list_channels))
except Exception as e:
    logging.error('Error', e)