import logging
import json
import os

from functions.utils import download, check_database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    if event:
        source_ip = event['requestContext']['http']['sourceIp']
        if not source_ip == os.environ['SourceIp']:
            return({
                'statusCode': 500,
                'body': 'Not Authorized'
            })

        if 'queryStringParameters' in event:
            url = event['queryStringParameters']['url']
        elif 'Records' in event:
            # Parses SQS Input
            url = event['Records'][0]['body']
        else:
            url = 'https://www.youtube.com/@MrBeast'
            url = 'https://www.youtube.com/watch?v=7IKab3HcfFk'

    url_info = download(url)
    check_database(url_info)

    return({
        'statusCode': 200,
        'body': json.dumps(url_info),
        'headers': {
            'Content-Type': 'application/json'
        }
    })

if __name__ == '__main__':
    handler(None, None)