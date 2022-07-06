import requests
import os

from flask import Blueprint, Flask, jsonify, request, redirect

from functions.utils import getCurrentTime
from functions.databaseCalls import channels
from functions.downloader import download

from classes.shared import db
from classes import Channels

channels_bp = Blueprint('channels', __name__, url_prefix='/channels')

@channels_bp.route('/', methods=['GET'])
def root():
    channelList = channels.getAllChannels()
    channelListArray = []
    columns = channels.getColumns()
    for channel in channelList:
        channelListQuery = channels.getChannelById(channel.id)
        for result in channelListQuery:
            channelListArray.append(dict(zip(columns, result)))

    return(jsonify(channelListArray))

@channels_bp.route('/add', methods=['GET'])
def add():
    url = request.args['url']
    download_results = download(video=url, video_range=1, download_confirm=False)
    result_latest_upload = download_results['entries'][0]['original_url']
    channel_exists = channels.getChannelByName(download_results['channel'])

    if channel_exists:
        print(f'The {download_results["channel"]} is already in the database.')
    elif not channel_exists:
        requests.get(os.environ.get("API_URL") + '/download/search?url=' + result_latest_upload)

        db_entry = Channels.Channels(
            channel_name = download_results['channel'],
            channel_follower_count = download_results['channel_follower_count'],
            channel_id = download_results['channel_id'],
            description = download_results['description'],
            original_url = download_results['original_url'],
            uploader = download_results['uploader'],
            uploader_id = download_results['uploader_id'],
            webpage_url = download_results['webpage_url'],
            picture_profile = download_results['thumbnails'][18]['url'],
            picture_cover = download_results['thumbnails'][15]['url'],
            last_updated = getCurrentTime(),
            latest_upload = download_results['entries'][0]['original_url']
        )

        db.session.add(db_entry)
        db.session.commit()
    else:
        print(f'There was another error.')

    return(jsonify(download_results))