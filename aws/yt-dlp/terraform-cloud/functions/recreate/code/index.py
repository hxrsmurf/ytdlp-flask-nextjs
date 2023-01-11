import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from functions.sqs import send_sqs_message

def handler(event, context):
    recreate = open('recreate.txt', 'r')
    for line in recreate:
        channel = line.strip()
        send_sqs_message(channel)