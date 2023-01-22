import boto3
import os
import logging

client = boto3.client('sns')

sns_arn = os.environ['sns_arn']

def publish_sns(channel=None, latest_video_title=None, url=None):
    sns_message = f'{channel};{latest_video_title};{url}'

    logging.info(f'SNS Publishing: {sns_arn} - {sns_message}')

    response = client.publish(
        TopicArn = sns_arn,
        Message = f'{latest_video_title}\n{url}'
        Subject = f'New Video from {channel}'
    )