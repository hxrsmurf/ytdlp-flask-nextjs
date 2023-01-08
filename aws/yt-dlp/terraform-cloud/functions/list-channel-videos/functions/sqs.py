import boto3
import os
import logging

client = boto3.client('sqs')

def send_sqs_message(message):
    logging.info(f'Adding to Video Queue: {message}')

    queue = ChannelQueue

    response = client.send_message(
        QueueUrl = os.environ['QueueChannels'],
        MessageBody = message
    )