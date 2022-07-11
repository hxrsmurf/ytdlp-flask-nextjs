import json
from flask import Blueprint, jsonify, request

from functions.downloader import download
from functions.utils import getCurrentTime
from classes import Mongo

mongo_bp = Blueprint('mongo', __name__, url_prefix='/mongo')

@mongo_bp.route('/channels/', methods=['GET'])
def root():
    query = Mongo.Channels.objects()
    query_json = json.loads(query.to_json())
    return(jsonify(query_json))

@mongo_bp.route('/channels/add', methods=['GET'])
def add():
    url = request.args['url']
    download_result = download(video=url, video_range=1, download_confirm=False)

    channel_name_lowercase = download_result['channel'].lower()

    query = Mongo.Channels(
        channel_id = download_result['channel_id'],
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

    return(json.loads(query.to_json()))