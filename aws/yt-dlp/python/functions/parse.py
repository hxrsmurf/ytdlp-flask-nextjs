import logging
import json

def parse_channel_info(info):
    json_info = json.loads(info)

    output_info = {
        'id' : json_info['id'],
        'uploader' : json_info['uploader'],
        'uploader_id' : json_info['uploader_id'],
        'uploader_url' : json_info['uploader_url'],
        'title' : json_info['title'],
        'channel_follower_count' : json_info['channel_follower_count'],
        'description' : json_info['description'],
        'tags' : json_info['tags'],
        'thumbnails' : json_info['thumbnails'],
        'channel' : json_info['channel'],
        'channel_id' : json_info['channel_id'],
        'channel_url' : json_info['channel_url'],
        'webpage_url' : json_info['webpage_url'],
        'original_url' : json_info['original_url'],
        'webpage_url_basename' : json_info['webpage_url_basename']
    }

    logging.info(output_info)
    return json.dumps(output_info)