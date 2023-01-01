import json
import logging

from functions.download import get_channel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    json_event = json.loads(json.dumps(event))
    request_context = json_event['requestContext']
    query_string = json_event['queryStringParameters']
    logging.info(query_string)

    URL = 'https://www.youtube.com/@MrBeast'

    channel_info = get_channel(query_string['id'])

    return({
            'statusCode': 200,
            'body': channel_info
        })