import json
import yt_dlp
import logging
import os
from time import time

def download(url, playlistend):
    ydl_opts = {
        'playlistend': playlistend,
        'quiet': True,
        'cachedir': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return info