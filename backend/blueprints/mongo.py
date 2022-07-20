import json
import os
import requests
import concurrent.futures
from flask import Blueprint, jsonify, request

from functions.downloader import download
from functions.utils import getCurrentTime
from functions.backblaze_upload import b2_upload
from classes import Mongo

mongo_bp = Blueprint('mongo', __name__, url_prefix='/mongo')

@mongo_bp.route('/channels/', methods=['GET'])
def get_channels():
    query = Mongo.Channels.objects().order_by('channel_name_lowercase')
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/channels/search/<string:channel_id>', methods=['GET'])
def search_channels(channel_id):
    query = Mongo.Channels.objects(channel_id=channel_id)
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/channels/add', methods=['GET'])
def add_channels():
    url = request.args['url']
    download_result = download(video=url, video_range=1, download_confirm=False)
    channel_id = download_result['channel_id']
    channel_name_lowercase = download_result['channel'].lower()

    query = Mongo.Channels(
        channel_id = channel_id,
        channel_name = download_result['channel'],
        channel_name_lowercase = channel_name_lowercase,
        channel_follower_count = download_result['channel_follower_count'],
        description = download_result['description'],
        original_url = download_result['original_url'],
        uploader = download_result['uploader'],
        uploader_id = download_result['uploader_id'],
        webpage_url = download_result['webpage_url'],
        picture_profile = download_result['thumbnails'][18]['url'],
        picture_cover = download_result['thumbnails'][15]['url'],
        last_updated = getCurrentTime(),
        latest_upload = download_result['entries'][0]['original_url']
    )

    query.save()

    download_channel_cover(channel_id)

    return(json.loads(query.to_json()))

@mongo_bp.route('/channels/cover-photo-missing', methods=['GET'])
def get_channels_cover_photo_missing():
    query = Mongo.Channels.objects(cdn_photo_cover=None)
    query_json = json.loads(query.to_json())
    for q in query_json:
        channel_id = q['_id']
        result_download_cover_photo = download_channel_cover(channel_id)
        Mongo.Channels.objects(channel_id=channel_id).update_one(set__cdn_photo_cover=result_download_cover_photo)
    return(jsonify(query_json))

@mongo_bp.route('/videos', methods=['GET'])
def get_videos():
    if len(request.args) == 0:
        limit = slice(0,25)
    else:
        limit = slice(0,int(request.args['limit']))

    query = Mongo.Videos.objects().order_by('-upload_date')[limit]
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/videos/search/<string:channel_id>', methods=['GET'])
def search_videos(channel_id):
    query = Mongo.Videos.objects(channel_id=channel_id).order_by('-upload_date')
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/videos/add', methods=['GET'])
def add_videos():
    url = request.args['url']
    download_result = download(video=url, video_range=1, download_confirm=False)

    if download_result == None:
        return(f'Video error {url}')

    channel_name_lowercase = download_result['channel'].lower()

    query = Mongo.Videos(
        channel_name = download_result['channel'],
        channel_name_lowercase = channel_name_lowercase,
        channel_id = download_result['channel_id'],
        description = download_result['description'],
        duration = download_result['duration'],
        duration_string = download_result['duration_string'],
        fulltitle = download_result['fulltitle'],
        video_id = download_result['id'],
        like_count = download_result['like_count'],
        view_count = download_result['view_count'],
        original_url = download_result['original_url'],
        thumbnail = download_result['thumbnail'],
        title = download_result['title'],
        upload_date = download_result['upload_date'],
        webpage_url = download_result['webpage_url']
    )

    query.save()

    query_json = json.loads(query.to_json())

    return({'download_results' : download_result, 'query_json' : query_json})

@mongo_bp.route('/videos/unique/channel', methods=['GET'])
def get_videos_unique_channel():
    query = Mongo.Videos.objects.aggregate([
        { "$group" :
            {
                "_id" : {
                    "channel_name" : "$channel_name", "channel_id" : "$channel_id", "channel_name_lowercase" : "$channel_name_lowercase"
                    },
                "lowercase" : {
                    "$push" : {
                        "channel_name_lowercase" : "$channel_name_lowercase"
                        }
                    }
            }
        },
        { "$sort" : {"lowercase": 1}}
    ])

    query_array = []

    for q in query:
        query_array.append({
            'channel_name' : q['_id']['channel_name'],
            'channel_id' : q['_id']['channel_id'],
            'channel_name_lowercase' : q['_id']['channel_name_lowercase'],
            })

    return(jsonify(query_array))

@mongo_bp.route('/videos/sync-channels')
def videos_sync_channels():
    channel_videos = json.loads(get_videos_unique_channel().data)
    channels = json.loads(get_channels().data)

    available_channels = []
    missing_channels = []
    result_missing = []

    for channel in channels:
        available_channels.append(channel['_id'])

    for channel in channel_videos:
        if not channel['channel_id'] in available_channels:
            missing_channels.append(json.loads(search_videos(channel['channel_id']).data))

    for missing in missing_channels:
        for m in missing:
            result_missing.append(m)

    return(jsonify(result_missing))

@mongo_bp.route('/download/latest', methods=['GET'])
def download_latest():
    channel_id = request.args['id']
    range = int(request.args['range'])
    query_channel = []

    if not channel_id == 'all':
        query_channel.append(json.loads(search_channels(channel_id).data)[0]['original_url'])
    else:
        all_channels = json.loads(get_channels().data)
        for channel in all_channels:
            query_channel.append(channel['original_url'])

    def download_channel(channel_url):
        download_result = download(video=channel_url, video_range=range, download_confirm=False)
        return download_result

    def download_video(video_url):
        requests.get(os.environ.get("API_URL") + '/mongo/videos/add?url=' + video_url)
        return(video_url)

    def get_futures(thread, type=None):
        result = []
        for future in concurrent.futures.as_completed(thread):
            if type == 'channel':
                for f in future.result()['entries']:
                    if f == None:
                        pass
                    else:
                        result.append(f['original_url'])
            else:
                result.append(future.result())
        return result

    channel_threads = []
    video_threads = []
    completed_videos = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for channel in query_channel:
            channel_threads.append(executor.submit(download_channel,channel))

        videos_in_range = get_futures(channel_threads, type='channel')

        for video_url in videos_in_range:
                video_threads.append(executor.submit(download_video, video_url))

        completed_videos = get_futures(video_threads)

    return(jsonify({'videos_in_range': videos_in_range}, {'completed_videos' : completed_videos}))

@mongo_bp.route('/download/channel/cover/<string:channel_id>', methods=['GET'])
def download_channel_cover(channel_id):
    photo_cover_output_filename = f'{channel_id}.jpg'
    photo_cover_output_folder = 'channel_photo_cover'

    photo_cover_url = json.loads(search_channels(channel_id).data)[0]['picture_cover']
    cdn_photo_cover_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/channel_photo_cover/{photo_cover_output_filename}'
    photo_cover_request = requests.get(photo_cover_url)
    cdn_photo_cover_request = requests.get(cdn_photo_cover_url)

    # If on CDN
    if cdn_photo_cover_request.status_code == 200:
        return(cdn_photo_cover_url)
    else:
        if photo_cover_request.status_code == 200:
            with open(photo_cover_output_filename, 'wb') as file:
                file.write(photo_cover_request.content)

            b2_upload(file=photo_cover_output_filename, folder=photo_cover_output_folder)

            Mongo.Channels.objects(channel_id=channel_id).update_one(set__cdn_photo_cover=cdn_photo_cover_url)

            if os.path.exists(photo_cover_output_filename):
                os.remove(photo_cover_output_filename)

            return(cdn_photo_cover_url)
        else:
            return(photo_cover_url)

@mongo_bp.route('/download/video/<string:video_id>', methods=['GET'])
def download_video_by_id(video_id):
    query = Mongo.Videos.objects(video_id=video_id)
    query_json = json.loads(query.to_json())[0]
    print(query_json['original_url'])
    return(jsonify(query_json))