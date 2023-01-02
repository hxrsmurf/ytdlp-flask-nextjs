import logging
import json

def parse_info(info):
    logging.info('Parsing info...')
    json_info = json.loads(info)
    type = json_info['_type']
    if type == 'playlist':
        logging.info('Parsing channel/playlist')
        return parse_channel_info(json.loads(info))
    elif type == 'video':
        logging.info('Parsing video')
        return parse_video_info(json.loads(info))
    else:
        return 'Error'

def parse_channel_info(json_info):
    video_id = json_info['entries'][0]['entries'][0]['id']
    video_original_url = json_info['entries'][0]['entries'][0]['original_url']
    thumbnails = json_info['thumbnails']
    cover_photo = thumbnails[4]['url'] # height: 263, width: 960
    uploader_id = json_info['uploader_id']

    output_info = {
        'id' : json_info['id'],
        'uploader' : json_info['uploader'],
        'uploader_id' : uploader_id,
        'uploader_url' : json_info['uploader_url'],
        'title' : json_info['title'],
        'channel_follower_count' : json_info['channel_follower_count'],
        'description' : json_info['description'],
        'tags' : json_info['tags'],
        'thumbnails' : thumbnails,
        'channel' : json_info['channel'],
        'channel_id' : json_info['channel_id'],
        'channel_url' : json_info['channel_url'],

        # First Entry of Channel's Video
        'video_id': video_id,
        'video_webpage_url': json_info['entries'][0]['entries'][0]['webpage_url'],
        'video_original_url': video_original_url,

        # Thumbnails
        'cover_photo': cover_photo,

        'webpage_url' : json_info['webpage_url'],
        'original_url' : json_info['original_url'],
        'webpage_url_basename' : json_info['webpage_url_basename']
    }

    return output_info, uploader_id, 'playlist'

def parse_video_info(json_info):
    channel_id = json_info['channel_id']
    output_info = {
        'id': json_info['id'],
        'title': json_info['title'],
        'thumbnail': json_info['thumbnail'],
        'description': json_info['description'],
        'uploader': json_info['uploader'],
        'uploader_id': json_info['uploader_id'],
        'uploader_url': json_info['uploader_url'],
        'channel_id': channel_id,
        'channel_url': json_info['channel_url'],
        'duration': json_info['duration'],
        'view_count': json_info['view_count'],
        'webpage_url': json_info['webpage_url'],
        'categories': json_info['categories'],
        'tags': json_info['tags'],
        'release_timestamp': json_info['release_timestamp'],
        'comment_count': json_info['comment_count'],
        'chapters': json_info['chapters'],
        'like_count': json_info['like_count'],
        'channel': json_info['channel'],
        'channel_follower_count': json_info['channel_follower_count'],
        'upload_date': json_info['upload_date'],
        'availability': json_info['availability'],
        'original_url': json_info['original_url'],
        'display_id': json_info['display_id'],
        'fulltitle': json_info['fulltitle'],
    }

    return output_info, channel_id, 'video'