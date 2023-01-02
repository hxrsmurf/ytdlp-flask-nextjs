import json
import yt_dlp
import logging

from .parse import parse_info
from .database import get_item, put_item_channel

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

    original_url = ''.join(url_info['original_url'])
    latest_video_original_url = ''.join(url_info['latest_video_original_url'])
    latest_video_original_url_database = get_item(original_url)

    if not latest_video_original_url == latest_video_original_url_database:
        put_item_channel(original_url, url_info)
    else:
        logging.info('Already in database')