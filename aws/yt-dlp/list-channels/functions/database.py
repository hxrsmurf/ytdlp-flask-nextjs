import boto3
import os
import logging

client = boto3.client('dynamodb')
table_name = os.environ['TableName']

def scan_items():
    logging.info('Scanning database')

    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName = table_name
    )

    return response_iterator