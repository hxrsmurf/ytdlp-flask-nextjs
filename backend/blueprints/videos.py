from flask import Blueprint, Flask, jsonify, request, redirect
from functions.databaseCalls import videos

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('/', methods=['GET'])
def root():
    videoList = videos.getAllVideos()
    videoListArray = []
    columns = videos.getColumns()
    for video in videoList:
        videoListQuery = videos.getVideoById(video.id)
        for result in videoListQuery:
            videoListArray.append(dict(zip(columns, result)))

    return(jsonify(videoListArray))