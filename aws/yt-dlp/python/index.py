import json
import logging

from functions.download import get_channel
from functions.database import get_item
from functions.sqs import send_sqs_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    testing = True
    if not testing:
        json_event = json.loads(json.dumps(event))
        request_context = json_event['requestContext']
        query_string = json_event['queryStringParameters']
        channel_info = get_channel(query_string['id'])
    else:
        URL = 'https://www.youtube.com/@MrBeast'
        video_id = '7IKab3HcfFk'
        exists_in_database = get_item(video_id)
        if not exists_in_database:
            send_sqs_message(video_id)
        #channel_info = get_channel(URL)
        channel_info = 'kevin'

    return({
            'statusCode': 200,
            'body': channel_info
        })