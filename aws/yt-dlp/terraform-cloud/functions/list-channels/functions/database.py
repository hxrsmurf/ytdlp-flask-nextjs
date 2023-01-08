import boto3
import os
import logging

client = boto3.client('dynamodb')

def scan_items():
    logging.info('Scanning database')

    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName = os.environ['TableChannels']
    )

    return response_iterator