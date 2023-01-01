import boto3
import os

client = boto3.client('sqs')
queue = os.environ['QueueUrl']

def send_sqs_message(message):
    response = client.send_message(
        QueueUrl=queue,
        MessageBody=message
    )