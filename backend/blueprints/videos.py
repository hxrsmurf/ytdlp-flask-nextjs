from flask import Blueprint, Flask, jsonify, request, redirect
from functions.databaseCalls import firebase
from functions.databaseCalls import videos
from functions.databaseCalls import channels

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('/', methods=['GET'])
def root():
    return(firebase.getAllVideos())

@videos_bp.route('/unique/channel-name', methods=['GET'])
def channelName():
    videoList = videos.getAllVideos(distinct=True)
    videoListArray = []
    columns = videos.getColumns()
    for video in videoList:
        videoListArray.append({
            'channel' : video.channel,
            'channel_id' : video.channel_id
        })

    return(jsonify(videoListArray))

@videos_bp.route('/sync-channels', methods=['GET'])
def syncChannels():
    videoChannelList = videos.getAllVideos(distinct=True)
    columns = videos.getColumns()

    missing_channels = []
    for channel in videoChannelList:
        channel_name = channel[1]
        query = channels.getChannelByName(channel_name)
        if not query:
            query2 = videos.getVideoByChannelName(channel_name)
            for q in query2:
                missing_channels.append(dict(zip(columns, q)))

    return(jsonify(missing_channels))