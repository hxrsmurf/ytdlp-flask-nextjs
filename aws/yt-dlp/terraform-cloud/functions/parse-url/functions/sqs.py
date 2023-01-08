import boto3
import os
import logging

client = boto3.client('sqs')

if 'TableChannels' in os.environ:
    queue = os.environ['QueueUrl']

def send_sqs_message(message):
    logging.info(f'Adding to queue: {message}')
    response = client.send_message(
        QueueUrl=queue,
        MessageBody=message
    )