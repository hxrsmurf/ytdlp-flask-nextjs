import json
import os
import requests
import concurrent.futures
from flask import Blueprint, jsonify, request, Response
import shutil
import time

from functions.downloader import download, download_thumbnail
from functions.utils import getCurrentTime, getInitialVideosToLoad
from functions.backblaze_upload import b2_upload, b2_sync
from functions.convert_ffmpeg import convert_to_hls
from functions.utils import redis_publish, redis_add_to_list, redis_cache_videos

from functions.bunnycdn import *

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

@mongo_bp.route('/videos/', methods=['GET'])
def get_videos():
    cached_videos = redis_cache_videos()
    if cached_videos:
        return(jsonify(cached_videos))
    else:
        query = Mongo.Videos.objects(watched=False,upload_date__gte=getInitialVideosToLoad()).order_by('-upload_date')
        query_json = json.loads(query.to_json())
        redis_cache_videos(data=query_json)
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
        thumbnail = download_result['thumbnail']
        video_id = download_result['id']
        download_thumbnail(thumbnail_url=thumbnail, video_id=video_id)

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
    limit = slice(0,30)
    query = Mongo.Videos.objects(watched=True,upload_date__gte=getInitialVideosToLoad()).order_by('-upload_date')[limit]
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/videos/unwatched')
def videos_view_unwatched():
    limit = slice(0,30)
    query = Mongo.Videos.objects(watched__ne=True,upload_date__gte=getInitialVideosToLoad()).order_by('-upload_date')[limit]
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/videos/thumbnails/')
def videos_get_thumbnails():
    videos = json.loads(get_videos().data)
    list_of_thumbnails = []
    for video in videos:
        thumbnail = video['thumbnail']
        video_id = video['_id']
        if 'https' in thumbnail:
            list_of_thumbnails.append(thumbnail)
            download_thumbnail(thumbnail_url=thumbnail, video_id=video_id)
    return(jsonify(list_of_thumbnails))

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
    video_title = query_json['title']
    duration = query_json['duration']

    cdn_mp4_exists, cdn_mp4_db, cdn_hls_exists, cdn_hls_db, check_cdn_mp4 = False,False, False, False, False

    if 'cdn_video' in query_json.keys():
        cdn_mp4_db = True
        cdn_video_url = query_json['cdn_video']
    else:
        cdn_video_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/videos/{video_id}/{video_id}.mp4'

    if not cdn_video_url == 'queued':
        check_cdn_mp4 = requests.head(cdn_video_url)

    debug = False
    if check_cdn_mp4:
        if check_cdn_mp4.status_code == 200 & debug == False:
            cdn_mp4_exists = True

    if 'cdn_video_hls' in query_json.keys():
        cdn_hls_db = True
        cdn_video_hls_id = query_json['cdn_video_hls']
        cdn_video_hls_url = f'https://video.bunnycdn.com/play/{os.environ.get("BUNNYCDN_LIBRARY")}/{cdn_video_hls_id}'
        check_cdn_hls = requests.get(cdn_video_hls_url)
        if check_cdn_hls.status_code == 200:
            cdn_hls_exists = True

    if cdn_mp4_exists:
        query = Mongo.Videos.objects(cdn_video=cdn_video_url)
        if not query:
            Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)
            return('Updated database')
        return('Video in database already')

    if cdn_mp4_exists and not cdn_hls_exists:
        if cdn_hls_db:
            bunnycdn_video_uploaded = bunnycdn_get(id=cdn_video_hls_id)
            message = (f'{video_id} has HLS DB Entry: {cdn_video_hls_id}\nBunnyCDN Progress: {bunnycdn_video_uploaded}%')
            print(message)
            return(message)
        else:
            print(f'Queuing to BunnyCDN: {video_id} - {video_title}')
            bunnycdn_video_guid = bunnycdn_fetch(url=cdn_video_url, title=video_title)
            print(f'GUID: {bunnycdn_video_guid}')
            query.update_one(set__cdn_video_hls=bunnycdn_video_guid)
            return(bunnycdn_video_guid)
    else:
        if cdn_mp4_db:
            return(f'{cdn_video_url} for {video_id}')
        else:
            FEATURE_DOWNLOAD_QUEUE = True
            FEATURE_REDIS = True

            if FEATURE_DOWNLOAD_QUEUE:
                db_check_existing = Mongo.DownloadQueue.objects(video_id=video_id)
                if db_check_existing:
                    message = f'{video_id} - Exists in database'
                    print(message)
                    return(message)
                else:
                    message = f'Queueing {video_id} - {original_url}'
                    redis_add_to_list(video_id=video_id, video_url=original_url, duration=duration)
                    return(message)
                    if not FEATURE_REDIS:
                        Mongo.DownloadQueue(
                            video_id = video_id,
                            webpage_url = original_url,
                            downloaded = False,
                            duration = duration
                        ).save()
                        Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video='queued')
                        print(message)
                        return(message)

            FEATURE_AWS_API = False
            if FEATURE_AWS_API:
                bunnycdn_video_guid = bunnycdn_create_video(title=video_title)

                # Use AWS to download and upload the video
                print(f'Submitting to AWS: {video_id} - {bunnycdn_video_guid}')
                aws_api_url = f'{os.environ.get("AWS_API_URL")}/?id={video_id}&guid={bunnycdn_video_guid}'
                requests.get(aws_api_url)

                cdn_video_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/videos/{video_id}/{video_id}.mp4'
                #Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)
                return(cdn_video_url)
            else:
                if not FEATURE_DOWNLOAD_QUEUE:
                    print(f'Downloading: {video_id} - {video_title}')
                    download(video=original_url, video_range=1, download_confirm=True)

                    print(f'Completed download\nUploading to Backblaze')
                    b2_sync(video_id)

                    print(f'Completed upload to Backblaze\nUpdating database')
                    cdn_video_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/videos/{video_id}/{video_id}.mp4'
                    Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)

                    print(f'Completed update todatabase\nRemoving local file')
                    if os.path.exists(video_id):
                        shutil.rmtree(video_id)
                    print(f'Completed {video_id}')

                    return(cdn_video_url)

    if cdn_mp4_exists and cdn_hls_exists:
        return(f'MP4 reachable on CDN: {cdn_video_url}</br>CDN reachable on CDN: {cdn_video_hls_url}')

    message = (f'Error in Download Video Return for {video_id}')
    print(message)
    return(message)

    # To Do:
    # Once available on CDN, add to HLS Queue

@mongo_bp.route('/download/queue/')
def get_download_queue():
    query = Mongo.DownloadQueue.objects(downloaded=False)
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/download/queue/<string:video_id>/complete')
def update_download_queue_video(video_id):
    cdn_video_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/videos/{video_id}/{video_id}.mp4'
    print(f'Marking {video_id} as complete and updating database with CDN URL')
    Mongo.DownloadQueue.objects(video_id=video_id).update_one(set__downloaded=True)
    Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=cdn_video_url)

    return(f'{cdn_video_url} - {video_id}')

@mongo_bp.route('/download/queue/delete-queue/')
def delete_download_queue_video():
    videos_with_queued_download_status = json.loads((Mongo.Videos.objects(cdn_video='queued')).to_json())
    for video in videos_with_queued_download_status:
        video_id = video['_id']
        Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=None)
    return('Successfully queued cdn_video')

@mongo_bp.route('/database/clear/cdn/videos')
def clear_cdn_videos():
    videos = videos_already_downloaded()
    try:
        confirm = request.args['confirm']
        if confirm == 'true':
            for video in json.loads(videos.data):
                video_id = video['_id']
                Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video=None)
            return('Database cleared')
        else:
            return('<a href="?confirm=true">Click this to confirm deletion</a>')
    except:
        return(videos)

@mongo_bp.route('/bunnycdn/list/')
def list_videos_on_bunnycdn():
    return bunnycdn_list()

@mongo_bp.route('/bunnycdn/list/broken/')
def list_broken_videos_on_bunnycdn():
    return jsonify(bunnycdn_list_broken_videos())

@mongo_bp.route('/bunnycdn/list/broken/delete')
def delete_broken_videos_on_bunnycdn():
    return jsonify(bunnycdn_videos_broken_delete())