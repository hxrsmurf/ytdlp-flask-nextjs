import logging
import json

from functions.utils import download, check_database

logger = logging.getLogger()

def handler(event, context):
    if 'queryStringParameters' in event:
        url = event['queryStringParameters']['url']
    else:
        # Parses SQS Input
        url = event['Records'][0]['body']

    info, id, type = download(url)

    # Check id in database
    # As required, update database
    check_database(info, id, type)

    return({
        'statusCode': 200,
        'body': json.dumps(info),
        'headers': {
            'Content-Type': 'application/json'
        }
    })