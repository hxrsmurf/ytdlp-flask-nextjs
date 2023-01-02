import json
import yt_dlp
import logging

from .parse import parse_info
from .database import get_item, put_item_channel, put_item_video

def download(url):
    ydl_opts = {
        'playlistend': 1,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return parse_info(info)

def check_database(url_info):
    logging.info('Checking database')

    download_type = url_info['download_type']

    if download_type == 'playlist':
        original_url = ''.join(url_info['original_url'])
        latest_video_original_url = ''.join(url_info['latest_video_original_url'])
        latest_video_original_url_database = get_item(original_url)

        if not latest_video_original_url == latest_video_original_url_database:
            put_item_channel(original_url, url_info)
        else:
            logging.info('Already in database')
    elif download_type == 'video':
        id = url_info['id']
        id_database = get_item(id, download_type)

        if not id == id_database:
            put_item_video(id, url_info)
        else:
            logging.info('Already in database')