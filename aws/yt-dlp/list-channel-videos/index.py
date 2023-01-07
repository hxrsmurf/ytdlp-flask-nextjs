import logging
import json

from functions.utils import download
from functions.sqs import send_sqs_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    url = 'https://www.youtube.com/@MrBeast'

    url_info = json.loads(download(url=url, playlistend=2))
    for entry in url_info['entries']:
        for video in entry['entries']:
            original_url = video['original_url']
            send_sqs_message(original_url)

    return({
        'statusCode': 200,
        'body': json.dumps(url_info),
        'headers': {
            'Content-Type': 'application/json'
        }
    })

if __name__ == '__main__':
    handler(None, None)