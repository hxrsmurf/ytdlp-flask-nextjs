import json
import requests
import os

from flask import Blueprint, Flask, jsonify, request, redirect

from functions.databaseCalls import videos
from functions.databaseCalls import channels
from functions.databaseCalls import firebase
from functions.downloader import download
from functions.utils import getCurrentTime

from classes.shared import db
from classes import Videos

download_bp = Blueprint('download', __name__, url_prefix='/download')

@download_bp.route('/search', methods=['GET'])
def root():
    url = request.args['url']
    result_download_url = download(video=url, video_range=1, download_confirm=False)
    return(firebase.addVideo(result_download_url))

@download_bp.route('/latest', methods=['GET'])
def latest():
    channel_id = request.args['id']
    range = int(request.args['range'])
    query_channel = []

    if channel_id == 'all':
        all_channels = firebase.getAllChannels()
        query = json.loads(all_channels.data)
        for q in query:
            channel_url = q['webpage_url']
            query_channel.append(channel_url)
    elif not channel_id == 'all':
        single_channel = firebase.getChannel(channel_id)
        query = json.loads(single_channel.data)
        query_channel.append(query['webpage_url'])

    for channel in query_channel:
        download_results = download(video=channel, video_range=range, download_confirm=False)
        for entry in download_results['entries']:
            video_url = entry['original_url']
            requests.get(os.environ.get("API_URL") + '/download/search?url=' + video_url)

    return(jsonify(download_results))