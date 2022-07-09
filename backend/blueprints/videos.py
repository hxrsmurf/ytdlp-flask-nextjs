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
    return(firebase.getAllChannels())

@videos_bp.route('/sync-channels', methods=['GET'])
def syncChannels():
    return(firebase.getMissingVideos())