from flask import Blueprint, Flask, jsonify, request, redirect
from functions.databaseCalls import firebase
from functions.databaseCalls import videos
from functions.databaseCalls import channels

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/videos/channel/<string:channel_id>', methods=['GET'])
def root(channel_id):
    return(jsonify(firebase.getAllVideosByChannel(channel_id)))