import boto3
import os
import logging

client = boto3.client('sqs')

VideoQueue = os.environ['QueueVideos']
ChannelQueue = os.environ['QueueVideos']
NewVideoQueue = os.environ['QueueNewVideo']

def send_sqs_message(channel=None, message=None, download_type=None, latest_video_title=None):

    if download_type == 'channel':
        queue = ChannelQueue
        sqs_message = message
    elif download_type == 'new-video':
        queue = NewVideoQueue
        sqs_message = f'{channel};{message};{latest_video_title}'

    logging.info(f'SQS Sending: {queue} - {sqs_message}')

    response = client.send_message(
        QueueUrl = queue,
        MessageBody = sqs_message
    )