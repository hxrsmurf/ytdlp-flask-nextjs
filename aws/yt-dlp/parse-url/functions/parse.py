import logging
import json

def parse_info(info):
    json_info = json.loads(info)
    type = json_info['_type']
    original_url = json_info['original_url']
    logging.info(f'Parsing: {original_url} - {type}')

    if type == 'playlist':
        return parse_channel_info(json.loads(info))
    elif type == 'video':
        return parse_video_info(json.loads(info))
    else:
        return 'Error'

def parse_channel_info(json_info):
    id = json_info['id']
    uploader = json_info['uploader']
    uploader_id = json_info['uploader_id']
    uploader_url = json_info['uploader_url']
    title = json_info['title']
    channel_follower_count = json_info['channel_follower_count']
    description = json_info['description']
    tags = json_info['tags']
    thumbnails = json_info['thumbnails']
    cover_photo = thumbnails[4]['url'] # height: 263, width: 960
    channel = json_info['channel']
    channel_id = json_info['channel_id']
    channel_url = json_info['channel_url']
    webpage_url = json_info['webpage_url'],
    original_url = json_info['original_url'],
    webpage_url_basename = json_info['webpage_url_basename']
    download_type = json_info['_type']

    # Latest Upload
    entries = json_info['entries'][0]['entries'][0]
    latest_video_id = entries['id']
    latest_video_webpage_url = entries['webpage_url']
    latest_video_original_url = entries['original_url']

    raw_info = {
        'id' : id,
        'uploader' : uploader,
        'uploader_id' : uploader_id,
        'uploader_url' : uploader_url,
        'title' : title,
        'channel_follower_count' : channel_follower_count,
        'description' : description,
        'tags' : tags,
        'thumbnails' : thumbnails,
        'cover_photo': cover_photo,
        'channel' : channel,
        'channel_id' : channel_id,
        'channel_url' : channel_url,
        'webpage_url' : webpage_url,
        'original_url' : original_url,
        'webpage_url_basename' : webpage_url_basename,
        'download_type' : download_type,

        # Latest Upload
        'latest_video_id': latest_video_id,
        'latest_video_webpage_url': latest_video_webpage_url,
        'latest_video_original_url': latest_video_original_url
    }

    return raw_info

def parse_video_info(json_info):
    id = json_info['id']
    title = json_info['title']
    thumbnail = json_info['thumbnail']
    description = json_info['description']
    uploader = json_info['uploader']
    uploader_id = json_info['uploader_id']
    uploader_url = json_info['uploader_url']
    channel_id = json_info['channel_id']
    channel_url = json_info['channel_url']
    duration = json_info['duration']
    view_count = json_info['view_count']
    webpage_url = json_info['webpage_url']
    categories = json_info['categories']
    tags = json_info['tags']
    release_timestamp = json_info['release_timestamp']
    comment_count = json_info['comment_count']
    chapters = json_info['chapters']
    like_count = json_info['like_count']
    channel = json_info['channel']
    channel_follower_count = json_info['channel_follower_count']
    upload_date = json_info['upload_date']
    availability = json_info['availability']
    original_url = json_info['original_url']
    display_id = json_info['display_id']
    fulltitle = json_info['fulltitle']

    raw_info = {
        'id': id,
        'title': title,
        'thumbnail': thumbnail,
        'description': description,
        'uploader': uploader,
        'uploader_id': uploader_id,
        'uploader_url': uploader_url,
        'channel_id': channel_id,
        'channel_url': channel_url,
        'duration': duration,
        'view_count': view_count,
        'webpage_url': webpage_url,
        'categories': categories,
        'tags': tags,
        'release_timestamp': release_timestamp,
        'comment_count': comment_count,
        'chapters': chapters,
        'like_count': like_count,
        'channel': channel,
        'channel_follower_count': channel_follower_count,
        'upload_date': upload_date,
        'availability': availability,
        'original_url': original_url,
        'display_id': display_id,
        'fulltitle': fulltitle,
    }

    return raw_info