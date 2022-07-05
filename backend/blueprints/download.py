from flask import Blueprint, Flask, jsonify, request, redirect

from functions.databaseCalls import videos
from functions.downloader import download
from functions.utils import getCurrentTime

from classes.shared import db
from classes import Videos

download_bp = Blueprint('download', __name__, url_prefix='/download')

@download_bp.route('/search', methods=['GET'])
def root():
    url = request.args['url']
    result_download_url = download(video=url, video_range=1, download_confirm=False)
    query_video = videos.getVideoByYouTubeId(result_download_url['id'])

    if query_video:
        print('The video already in database.')
    elif not query_video:
        db_entry = Videos.Videos(
            channel = result_download_url['channel'],
            channel_id = result_download_url['channel_id'],
            description = result_download_url['description'],
            duration = result_download_url['duration'],
            duration_string = result_download_url['duration_string'],
            fulltitle = result_download_url['fulltitle'],
            video_id = result_download_url['id'],
            like_count = result_download_url['like_count'],
            view_count = result_download_url['view_count'],
            original_url = result_download_url['original_url'],
            thumbnail = result_download_url['thumbnail'],
            title = result_download_url['title'],
            upload_date = result_download_url['upload_date'],
            webpage_url = result_download_url['webpage_url'],
            downloaded = False,
            downloaded_date = getCurrentTime()
        )
        db.session.add(db_entry)
        db.session.commit()
    else:
        print('There was another error.')
    return(jsonify(result_download_url))