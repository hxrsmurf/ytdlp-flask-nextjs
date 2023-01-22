import logging
from json import dumps
import requests
import os
from functions.parse import parse_sqs_channel_video, parse_sns_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def  viaRequests(url, message_headers, bot_message):
    response = requests.post(url=url, headers=message_headers, data=dumps(bot_message))
    if not response.status_code == 200:
        print('Unsuccessful')

def handler(event, context):
    subject, message = parse_sns_message(event)

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    space = os.environ['Space']
    key = os.environ['Key']
    token = os.environ['Token']

    url = f'https://chat.googleapis.com/v1/spaces/{space}/messages?'\
          f'key={key}'\
          f'&token={token}'

    bot_message = {
        'text': f'{subject}\n{message}}'
    }

    logging.info(bot_message)

    viaRequests(url, message_headers, bot_message)