import json
import logging
import os

from functions.download import download

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    URL = 'https://www.youtube.com/@MrBeast'
    video_id = '7IKab3HcfFk'
    video_url = 'https://www.youtube.com/watch?v=7IKab3HcfFk'
    download(video_url)

    complete = os.listdir('/tmp/')
    print(complete)

    return({
            'statusCode': 200,
            'body': 'Success'
    })