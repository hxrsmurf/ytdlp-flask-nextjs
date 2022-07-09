from flask import Blueprint, request

from functions.databaseCalls import firebase
from functions.downloader import download

channels_bp = Blueprint('channels', __name__, url_prefix='/channels')

@channels_bp.route('/', methods=['GET'])
def root():
    return(firebase.getAllChannels())

@channels_bp.route('/add', methods=['GET'])
def add():
    url = request.args['url']
    download_results = download(video=url, video_range=1, download_confirm=False)
    result_latest_upload = download_results['entries'][0]['original_url']
    return(firebase.addChannel(download_results))