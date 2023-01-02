import logging
import json

from functions.database import get_item, put_item
from functions.utils import download

logger = logging.getLogger()

def handler(event, context):
    if 'queryStringParameters' in event:
        url = event['queryStringParameters']['url']
        channel_info = url
    else:
        # Parses SQS Input
        url = event['Records'][0]['body']

    prod = False

    if prod:
        channel_info, video_id, video_original_url, cover_photo = get_channel_info(url)
        dynamo_video_id = get_item(url)

        if not video_id == dynamo_video_id:
            put_item(url, channel_info, video_id, video_original_url, cover_photo)
    else:
        info, id, type = download(url)
        logging.info(info)

    return({
        'statusCode': 200,
        'body': json.dumps(info),
        'headers': {
            'Content-Type': 'application/json'
        }
    })