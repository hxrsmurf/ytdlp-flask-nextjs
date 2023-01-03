import json
import yt_dlp
import logging
import os
from time import time

from .parse import parse_info
from .database import get_item, put_item_channel, put_item_video
from .sqs import send_sqs_message

# Hard coding this so I can run locally
table_channels = 'nextjs-13-yt-dlp-channels'
table_videos = 'nextjs-13-yt-dlp-videos'

if 'TableChannels' in os.environ:
    table_channels = os.environ['TableChannels']
    table_videos = os.environ['TableVideos']

def download(url):
    ydl_opts = {
        'playlistend': 1,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return parse_info(info)

def current_epoch_time():
    return str(time())

def check_database(url_info):
    logging.info('Checking database')

    download_type = url_info['download_type']

    if download_type == 'playlist':
        table_name = table_channels
        original_url = ''.join(url_info['original_url'])
        latest_video_original_url = ''.join(url_info['latest_video_original_url'])
        latest_video_original_url_database = get_item(original_url, download_type, table_name)

        if not latest_video_original_url == latest_video_original_url_database:
            put_item_channel(original_url, url_info, table_name, updated_at=current_epoch_time())
            send_sqs_message(latest_video_original_url)
        else:
            logging.info('Already in database')
    elif download_type == 'video':
        table_name = table_videos
        id = url_info['id']
        like_count = url_info['like_count']
        like_count_database = get_item(id, download_type, table_name)

        if not like_count == like_count_database:
            put_item_video(id, url_info, table_name, updated_at=current_epoch_time())
        else:
            logging.info('Already in database')