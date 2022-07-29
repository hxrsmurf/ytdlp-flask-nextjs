import json
import os
import requests
import concurrent.futures
from flask import Blueprint, jsonify, request, Response
import shutil

from functions.downloader import download
from functions.utils import getCurrentTime
from functions.backblaze_upload import b2_upload, b2_sync
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

    query = Mongo.Videos.objects(watched=False).order_by('-upload_date')[limit]
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
    is_playlist = False

    if len(url.split('playlist?')) > 1:
        range = 99
        is_playlist = True
    else:
        range = 1

    download_result = download(video=url, video_range=range, download_confirm=False)

    if download_result == None:
        return(f'Video error {url}')


    try:
        def download_video(video_url):
            requests.get(os.environ.get("API_URL") + '/mongo/videos/add?url=' + video_url)

        if download_result['entries']:
            with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
                for entry in download_result['entries']:
                    video_url = entry['webpage_url']
                    executor.submit(download_video, video_url)
    except:
        pass

    if not is_playlist:
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
            webpage_url = download_result['webpage_url'],
            watched = False
        )

        query.save()

        query_json = json.loads(query.to_json())
        return({'download_results' : download_result, 'query_json' : query_json})
    else:
        return({'download_results' : download_result})


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

@mongo_bp.route('/videos/sync/watched')
def videos_sync_watched():
    # This was a one-time deal to update the database.
    # query = Mongo.Videos.objects(watched__ne='True').order_by('-upload_date')

    query = Mongo.Videos.objects(watched='').order_by('-upload_date')
    query_json = json.loads(query.to_json())

    try:
        for q in query_json:
            print(q)
            videos_mark_unwatched(q['_id'])
        return('Success')
    except Exception as e:
        return(f'Error because {e}')

@mongo_bp.route('/videos/downloaded')
def videos_already_downloaded():
    query = Mongo.Videos.objects(cdn_video__contains='https').order_by('-upload_date')
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

# Could probably boolean the watched URL, but opting to do this for now.
@mongo_bp.route('/videos/<string:video_id>/watched')
def videos_mark_watched(video_id):
    try:
        Mongo.Videos.objects(video_id=video_id).update_one(watched=True)
        return('Success')
    except:
        print('Error')
        return Response('Error', status=500)

@mongo_bp.route('/videos/<string:video_id>/unwatched')
def videos_mark_unwatched(video_id):
    try:
        Mongo.Videos.objects(video_id=video_id).update_one(watched=False)
        return('Success')
    except:
        print('Error')
        return Response('Error', status=500)

@mongo_bp.route('/videos/watched')
def videos_view_watched():
    limit = slice(0,25)
    query = Mongo.Videos.objects(watched=True).order_by('-upload_date')[limit]
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/videos/unwatched')
def videos_view_unwatched():
    limit = slice(0,25)
    query = Mongo.Videos.objects(watched__ne=True).order_by('-upload_date')[limit]
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

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

    original_url = query_json['original_url']

    video_file_name = f'{video_id}.mp4'
    video_folder = 'videos'
    cdn_video_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/{video_folder}/{video_id}/{video_file_name}'

    check_exists_cdn = requests.head(cdn_video_url)

    if (check_exists_cdn.status_code == 200):
        print(f'{video_id} exists on CDN')
        query = Mongo.Videos.objects(cdn_video=cdn_video_url)
        if not query:
            print(f'Database is out of date. Updating...')
            Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)
            print('Complete Database Update')
        return(f'{video_id} exists on CDN')
    else:
        print(f'Downloading {video_id}')
        download_result = download(video=original_url, video_range=1, download_confirm=True)
        print(f'Completed Download')

        file_name = download_result['requested_downloads'][0]['_filename']
        file_path = download_result['requested_downloads'][0]['filepath']

        print(f'Uploading {video_id} to BackBlaze...')
        b2_sync(video_id)
        print('Completed Upload')

        print(f'Updating database for {video_id}')
        Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)
        print('Complete Database Update')

        if os.path.exists(video_file_name):
            shutil.rmtree(video_file_name)

        return(cdn_video_url)

@mongo_bp.route('/database/clear/cdn/videos')
def clear_cdn_videos():
    videos = videos_already_downloaded()
    for video in json.loads(videos.data):
        video_id = video['_id']
        Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=None)
    return(videos)