from flask import Blueprint, Flask, jsonify, request, redirect
from functions.databaseCalls import videos
from functions.databaseCalls import channels

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/videos/channel/<string:channelName>', methods=['GET'])
def root(channelName):
    print(channelName)
    videoList = videos.getVideoByChannelName(channelName)
    videoListArray = []
    columns = videos.getColumns()
    for video in videoList:
        videoListArray.append(dict(zip(columns, video)))
    return(jsonify(videoListArray))