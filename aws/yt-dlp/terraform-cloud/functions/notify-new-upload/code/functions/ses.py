import boto3
import logging
import os

client = boto3.client('ses')

def send_ses(channel, video):

    logging.info("Sending email")
    email = os.environ['email']

    subject = f'New Video from {channel}'
    message = f'Video Uploaded\n{video}'

    response = client.send_email(
        Source = email,
        Destination = {
            'ToAddresses': [
                email
            ]
        },
        Message = {
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body' : {
                'Text' : {
                    'Data': message,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

