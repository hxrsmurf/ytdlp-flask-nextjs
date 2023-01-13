import logging
import json
import os

from functions.ses import send_ses
from functions.parse import parse_sqs_channel_video

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):

    channel, video, title = parse_sqs_channel_video(event)
    send_ses(channel, video, title)

    return({
        'statusCode': 200,
        'body': event,
        'headers': {
            'Content-Type': 'application/json'
        }
    })

if __name__ == '__main__':
    handler(None, None)