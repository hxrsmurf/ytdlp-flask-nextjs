import logging

from functions.download import get_channel
from functions.database import get_item, put_item

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    url = event['Records'][0]['body']
    channel_info, video_id = get_channel(url)
    dynamo_video_id = get_item(url)
    if not video_id == dynamo_video_id:
        put_item(url, channel_info, video_id)

    return({
            'statusCode': 200,
            'body': channel_info
        })