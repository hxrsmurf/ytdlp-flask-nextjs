import json
import logging

from functions.download import get_channel
from functions.database import get_item, put_item
from functions.sqs import send_sqs_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    testing = False
    if not testing:
        json_event = json.loads(json.dumps(event))
        request_context = json_event['requestContext']
        url = json_event['queryStringParameters']['id']
        channel_info, video_id = get_channel(url)
        dynamo_video_id = get_item(url)
        if not video_id == dynamo_video_id:
            put_item(url, channel_info, video_id)
    else:
        URL = 'https://www.youtube.com/@MrBeast'
        video_id = '7IKab3HcfFk'
        channel_info, video_id = get_channel(URL)
        dynamo_video_id = get_item(URL)
        if not video_id == dynamo_video_id:
            put_item(URL, channel_info, video_id)
            #send_sqs_message(video_id)

    return({
            'statusCode': 200,
            'body': channel_info
        })