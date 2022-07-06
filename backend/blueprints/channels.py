from flask import Blueprint, Flask, jsonify, request, redirect
from functions.databaseCalls import channels

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

@channels_bp.route('<int:videoID>', methods=['GET'])
def blueprint_testing_page(videoID):
    print(videoID)
    return('Hello World')