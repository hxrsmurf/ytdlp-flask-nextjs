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

import concurrent.futures

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
    thread_workers = None

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

    def download_channel(channel_url):
        download_result = download(video=channel, video_range=range, download_confirm=False)
        return download_result

    def download_video(video_url):
        requests.get(os.environ.get("API_URL") + '/download/search?url=' + video_url)
        return(video_url)

    def get_futures(thread, type=None):
        result = []
        for future in concurrent.futures.as_completed(thread):
            if type == 'channel':
                for f in future.result()['entries']:
                    result.append(f['original_url'])
            else:
                result.append(future.result())
        return result

    channel_threads = []
    video_threads = []
    completed_videos = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_workers) as executor:
        for channel in query_channel:
            channel_threads.append(executor.submit(download_channel,channel))

        videos_in_range = get_futures(channel_threads, type='channel')

        for video_url in videos_in_range:
                video_threads.append(executor.submit(download_video, video_url))

        completed_videos = get_futures(video_threads)

    return(jsonify({'available_videos': videos_in_range}, {'completed_videos' : completed_videos}))