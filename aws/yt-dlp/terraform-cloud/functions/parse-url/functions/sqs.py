import boto3
import os
import logging

client = boto3.client('sqs')

VideoQueue = os.environ['QueueVideos']
ChannelQueue = os.environ['QueueVideos']

def send_sqs_message(message, download_type):
    logging.info(f'Adding to Video Queue: {message}')

    if download_type == 'channel':
        queue = ChannelQueue

    response = client.send_message(
        QueueUrl = queue,
        MessageBody = message
    )