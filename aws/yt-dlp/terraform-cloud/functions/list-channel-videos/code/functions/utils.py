import json
import yt_dlp
import logging
import os
from time import time

from .parse import parse_info

def current_epoch_time():
    return str(time())

def download(url, playlistend):
    ydl_opts = {
        'playlistend': playlistend,
        'quiet': True,
        'cachedir': False,
        'download_archive': '/tmp/download.txt',
        'outtmpl' : '/tmp/%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return parse_info(info)