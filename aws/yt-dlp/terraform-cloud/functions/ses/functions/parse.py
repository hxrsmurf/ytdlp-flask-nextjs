import logging

def parse_sqs_channel_video(event):
    logging.info('Parsing SQS')
    body = event['Records'][0]['body']
    message = body.split(',')
    channel = message[0]
    video = message[1]

    return channel, video