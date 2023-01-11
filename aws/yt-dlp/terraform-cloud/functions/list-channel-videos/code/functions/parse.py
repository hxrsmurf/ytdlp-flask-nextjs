import logging
import json

from .sqs import send_sqs_message

def parse_info(info):
    json_info = json.loads(info)
    type = json_info['_type']
    original_url = json_info['original_url']
    logging.info(f'Parsing: {original_url} - {type}')

    if type == 'playlist':
        return parse_channel_videos(json.loads(info))
    else:
        return 'Error'

def parse_channel_videos(json_info):
    all_entries = json_info['entries'][0]['entries']
    all_videos = []
    for entry in all_entries:
        original_url = entry['original_url']
        send_sqs_message(original_url)
        logging.info(original_url)
    return all_videos