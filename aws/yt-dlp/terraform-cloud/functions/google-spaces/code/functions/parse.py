import logging

def parse_sqs_channel_video(event):
    logging.info('Parsing SQS')
    body = event['Records'][0]['body']
    message = body.split(';')
    channel = message[0]
    video = message[1]
    title = message[2]

    return channel, video, title

def parse_sns_message(event):
    logging.info('Parsing SNS')
    body = event['Records'][0]['Sns']
    subject = body['Subject']
    message = body['Message']
    return subject, message