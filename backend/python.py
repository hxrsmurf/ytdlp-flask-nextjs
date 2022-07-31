import os
import json
from flask import Flask, jsonify, request, redirect
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import datetime
import requests

from functions.handler_json import handler_json, handler_json_file, handler_downloader
from functions.downloader import download

load_dotenv('.env')
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db' : 'ytdlp',
    'host' : '192.168.2.12',
    'port':  27017,
    'username' : os.environ.get("MONGODB_USER"),
    'password' : os.environ.get("MONGODB_PASSWORD"),
    'authentication_source' : 'admin'
}

from classes.shared import db
from classes.shared import mongo_db

db.init_app(app)
mongo_db.init_app(app)
db.app = app

# Blueprints
from blueprints.videos import videos_bp
from blueprints.channels import channels_bp
from blueprints.download import download_bp
from blueprints.search import search_bp
from blueprints.mongo import mongo_bp

app.register_blueprint(videos_bp)
app.register_blueprint(channels_bp)
app.register_blueprint(download_bp)
app.register_blueprint(search_bp)
app.register_blueprint(mongo_bp)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def default_route():
    return('Default')

@app.route('/videos', methods=['GET'])
@cross_origin()
def videos():
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    if not request.args:
        db_results = db_videos.query.order_by(desc(db_videos.upload_date), db_videos.downloaded_date).limit(10)
        all_videos = []

        for row in db_results:
            db_video_information = vars(row)
            db_video_information.pop("_sa_instance_state")
            all_videos.append(db_video_information)

        return(jsonify(all_videos))
    else:
        query_args = request.args
        for args in query_args:
            if args == 'channels':
                if not 'sync' in query_args:
                    db_query_all_channels =  db.session.query(db_videos.channel_id, db_videos.channel).order_by(collate(db_videos.channel, 'NOCASE')).distinct().all()
                    all_channels = []
                    for query in db_query_all_channels:
                        all_channels.append({
                            'channel' : query.channel,
                            'channel_id' : query.channel_id
                        })
                    return(jsonify(all_channels))

                # We have to do this because ytsearch yt-dlp is bad at finding channels by their ID.
                elif 'sync' in query_args:
                    db_query_all_channels =  db.session.query(db_videos.channel_id, db_videos.channel, db_videos.original_url, db_videos.title).order_by(db_videos.channel).distinct().all()
                    missing_channels = []
                    for channel in db_query_all_channels:
                        db_query_check_channel_exists = db.session.query(db_channel.channel_id,db_channel.channel).filter_by(channel_id=channel.channel_id).all()
                        if not db_query_check_channel_exists:
                            missing_channels.append({
                                'channel' : channel.channel,
                                'channel_id' : channel.channel_id,
                                'original_url' : channel.original_url,
                                'title' : channel.title
                            })
                    return(jsonify(missing_channels))
                else:
                    return('Error')
            elif args == 'search':
                search_query = request.args[args]
                channel_videos = db.session.query(db_videos).order_by(desc(db_videos.upload_date)).filter_by(channel=search_query).all()
                all_channel_videos = []
                for videos in channel_videos:
                    video_information = vars(videos)
                    video_information.pop("_sa_instance_state")
                    all_channel_videos.append(video_information)
                return(jsonify(all_channel_videos))
            elif args == 'add':
                add_query = request.args[args]
                download_results = download(video=add_query, video_range=1, download_confirm=False)
                download_exists = db.session.query(db_videos).filter_by(video_id=download_results['id']).all()
                if not download_exists:
                    db_entry = db_videos(
                        channel = download_results['channel'],
                        channel_id = download_results['channel_id'],
                        description = download_results['description'],
                        duration = download_results['duration'],
                        duration_string = download_results['duration_string'],
                        fulltitle = download_results['fulltitle'],
                        video_id = download_results['id'],
                        like_count = download_results['like_count'],
                        view_count = download_results['view_count'],
                        original_url = download_results['original_url'],
                        thumbnail = download_results['thumbnail'],
                        title = download_results['title'],
                        upload_date = download_results['upload_date'],
                        webpage_url = download_results['webpage_url'],
                        downloaded = False,
                        downloaded_date = current_time
                    )

                    db.session.add(db_entry)
                    db.session.commit()
                    return(jsonify({'result' : 'success'}))
                else:
                    return('Already downloaded')
            elif args == 'latest':
                for requested_args in request.args:
                    if 'search' in requested_args:
                        query_results = [{
                            'original_url' : request.args[requested_args]
                        }]
                    elif 'name' in requested_args:
                        channel_name = request.args[requested_args]
                        request_channel_information = json.loads((requests.get(os.environ.get("API_URL") + '/channels?name=' + channel_name)).content)
                        query_results = [{
                            'original_url' : request_channel_information[0]['url']
                        }]
                    elif 'id' in requested_args:
                        channel_id = request.args[requested_args]
                        request_channel_information = json.loads((requests.get(os.environ.get("API_URL") + '/channels?id=' + channel_id)).content)
                        query_results = [{
                            'original_url' : request_channel_information[0]['url']
                        }]
                    else:
                        query_channels = requests.get(os.environ.get("API_URL") + '/channels')
                        query_results = json.loads(query_channels.content)

                for channel in query_results:
                    channel_url = channel['original_url']
                    if request.args[args]:
                        latest_query = f'latest={request.args[args]}'
                    else:
                        latest_query = 'latest'
                    query_url = requests.get(os.environ.get("API_URL") + '/channels?' + latest_query + '&search=' + channel_url)
                    latest_videos = json.loads(query_url.content)
                    for video in latest_videos:
                        requests.get(os.environ.get("API_URL") + '/videos?add=' + video)

                return(jsonify({'result' : 'success'}))

if __name__ == "__main__":
    app.run(host='0.0.0.0')