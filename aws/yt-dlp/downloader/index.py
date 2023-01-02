import logging
import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    URL = 'https://www.youtube.com/@MrBeast'
    video_id = '7IKab3HcfFk'
    video_url = 'https://www.youtube.com/watch?v=7IKab3HcfFk'
    base_url = os.environ['ApiUrl']
    url = f'{base_url}/download?url={video_url}'
    requests.get(url)

    return({
            'statusCode': 200,
            'body': 'Success'
    })