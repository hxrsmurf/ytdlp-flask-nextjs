import logging
import json
import os

from functions.utils import download

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    url = event['Records'][0]['body']
    # url = 'https://www.youtube.com/@MrBeast'
    # url = 'https://www.youtube.com/watch?v=7IKab3HcfFk'

    url_info = download(url, playlistend=600)

    return({
        'statusCode': 200,
        'body': url_info,
        'headers': {
            'Content-Type': 'application/json'
        }
    })

if __name__ == '__main__':
    handler(None, None)