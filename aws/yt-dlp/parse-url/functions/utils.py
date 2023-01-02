import json
import yt_dlp
import logging

from .parse import parse_info
from .database import get_item, put_item

def download(url):
    ydl_opts = {
        'playlistend': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    info, id, type = parse_info(info)

    return info, id, type

def check_database(info, id, type):
    logging.info('Checking database')
    # in_database = get_item(id)
    put_item(id, info)