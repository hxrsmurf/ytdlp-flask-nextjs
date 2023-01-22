import json
import yt_dlp
import logging
import os
from time import time

from .parse import parse_info
from .database import get_item, put_item_channel, put_item_video
from .sqs import send_sqs_message
from .sns import publish_sns

def current_epoch_time():
    return str(time())

def download(url):
    ydl_opts = {
        'playlistend': 1,
        'quiet': True,
        'cachdir': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return parse_info(info)


def check_database(url_info):
    logging.info('Checking database')

    table_channels = os.environ['TableChannels']
    table_videos = os.environ['TableVideos']
    download_type = url_info['download_type']

    if download_type == 'playlist':
        table_name = table_channels
        channel = ''.join(url_info['channel'])
        latest_video_original_url = ''.join(url_info['latest_video_original_url'])
        latest_video_title = url_info['latest_video_title']
        latest_video_original_url_database = get_item(channel, download_type, table_name)

        if not latest_video_original_url == latest_video_original_url_database:
            logging.info(f'New video uploaded: {channel} - {latest_video_original_url}')
            put_item_channel(channel, url_info, table_name, updated_at=current_epoch_time())
            send_sqs_message(None, latest_video_original_url, 'channel')
            # send_sqs_message(channel, latest_video_original_url, 'new-video', latest_video_title)
            publish_sns(channel=channel, latest_video_title=latest_video_title, url=latest_video_original_url)
        else:
            logging.info(f'Already in database: {channel} - {latest_video_original_url}')

    elif download_type == 'video':
        table_name = table_videos

        id = url_info['id']
        channel = url_info['channel']
        logging.info(f'Video is for {channel}')
        id_database = get_item(id, download_type, table_name)

        if not id == id_database:
            put_item_video(id, url_info, table_name, updated_at=current_epoch_time())
        else:
            logging.info('Already in database')