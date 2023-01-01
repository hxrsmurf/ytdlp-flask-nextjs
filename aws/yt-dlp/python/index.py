import json
import os
import logging
import yt_dlp

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    json_event = json.loads(json.dumps(event))
    #request_context = json_event['requestContext']
    #logging.info(request_context)

    URL = 'https://www.youtube.com/@MrBeast'

    ydl_opts = {
        'playlistend': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return({
            'statusCode': 200,
            'body': info
        })