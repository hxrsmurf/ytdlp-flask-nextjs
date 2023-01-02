import logging

from functions.database import get_item, put_item
from functions.utils import get_channel_info

logger = logging.getLogger()

def handler(event, context):
    if 'queryStringParameters' in event:
        url = event['queryStringParameters']['url']
        channel_info = url
    else:
        pass

    channel_info, video_id, video_original_url = get_channel_info(url)
    dynamo_video_id = get_item(url)

    if not video_id == dynamo_video_id:
        put_item(url, channel_info, video_id)

    return({
            'statusCode': 200,
            'body': channel_info
    })