import logging

from functions.database import scan_items
from functions.parser import parse_paginated_info
from functions.sqs import send_sqs_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    result_scan = scan_items()
    channels = parse_paginated_info(result_scan)
    for channel in channels:
        logging.info(channel)
        send_sqs_message(channel)

    return({
        'statusCode': 200,
        'body': 'Success'
    })