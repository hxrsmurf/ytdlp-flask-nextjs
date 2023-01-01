import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    json_event = json.loads(json.dumps(event))
    request_context = json_event['requestContext']

    logging.info(request_context)

    return({
            'statusCode': 200,
            'body': 'Success'
        })