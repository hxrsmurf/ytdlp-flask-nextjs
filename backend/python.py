import os
import json
from flask import Flask, jsonify, request, redirect
from sqlalchemy import collate, desc
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import datetime
import requests

from flask_sqlalchemy import SQLAlchemy

from functions.handler_json import handler_json, handler_json_file, handler_downloader
from functions.downloader import download

load_dotenv('.env')
app = Flask(__name__)

# SQLAlchemy
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youtube.sqlite3'
db = SQLAlchemy(app)

class db_channel(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    channel = db.Column(db.String(100))
    channel_follower_count = db.Column(db.Integer)
    channel_id = db.Column(db.String(100))
    description = db.Column(db.String(100))
    original_url = db.Column(db.String(100))
    uploader = db.Column(db.String(100))
    uploader_id = db.Column(db.String(100))
    webpage_url = db.Column(db.String(100))
    picture_profile = db.Column(db.String(100))
    picture_cover = db.Column(db.String(100))
    last_updated = db.Column(db.String(100))
    latest_upload = db.Column(db.String(100))

    def __init__(self, channel, channel_follower_count, channel_id, description, original_url, uploader, uploader_id, webpage_url, picture_profile, picture_cover, last_updated, latest_upload):
        self.channel = channel
        self.channel_follower_count = channel_follower_count
        self.channel_id = channel_id
        self.description = description
        self.original_url = original_url
        self.uploader = uploader
        self.uploader_id = uploader_id
        self.webpage_url = webpage_url
        self.picture_profile = picture_profile
        self.picture_cover = picture_cover
        self.last_updated = last_updated
        self.latest_upload = latest_upload

class db_videos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    channel = db.Column(db.String(100))
    channel_id = db.Column(db.String(100))
    description = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    duration_string = db.Column(db.String(100))
    fulltitle = db.Column(db.String(100))
    video_id = db.Column(db.String(100))
    like_count = db.Column(db.String(100))
    view_count = db.Column(db.String(100))
    original_url = db.Column(db.String(100))
    thumbnail = db.Column(db.String(100))
    title = db.Column(db.String(100))
    upload_date = db.Column(db.String(100))
    webpage_url = db.Column(db.String(100))
    downloaded = db.Column(db.Boolean)
    downloaded_date = db.Column(db.String(100))

    def __init__(self, channel, channel_id, description, duration, duration_string, fulltitle, video_id, like_count, view_count, original_url, thumbnail, title, upload_date, webpage_url, downloaded, downloaded_date):
        self.channel = channel
        self.channel_id = channel_id
        self.description = description
        self.duration = duration
        self.duration_string = duration_string
        self.fulltitle = fulltitle
        self.video_id = video_id
        self.like_count = like_count
        self.view_count = view_count
        self.original_url = original_url
        self.thumbnail = thumbnail
        self.title = title
        self.upload_date = upload_date
        self.webpage_url = webpage_url
        self.downloaded = downloaded
        self.downloaded_date = downloaded_date

db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def default_route():
    return('Default')

@app.route('/channels', methods=['GET'])
@cross_origin()
def channels():
    search = request.args.get('search', None)
    now = datetime.datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    if not request.args:
        db_results = db_channel.query.all()
        all_channels = []
        for row in db_results:
            db_channel_information = vars(row)
            db_channel_information.pop("_sa_instance_state")
            all_channels.append(db_channel_information)
        return(jsonify(all_channels))
    else:
        query_args = request.args
        for args in query_args:
            if args == 'latest':
                desired_range = request.args[args]
                if desired_range:
                    desired_range = int(desired_range)
                else:
                    desired_range = 1

                results = download(video=search, video_range=desired_range, download_confirm=False)
                all_videos = []
                for video in results['entries']:
                    all_videos.append(video['original_url'])

                for video in all_videos:
                    requests.get(os.environ.get("API_URL") + '/videos?add=' + video)

                return(jsonify(all_videos))
            elif args == 'name':
                    channel_name = request.args[args]
                    channel_information = []
                    query = db.session.query(db_channel).filter_by(channel=channel_name)
                    for q in query:
                        channel_information.append({
                            'channel' : q.channel,
                            'url' : q.original_url
                        })
                    return(jsonify(channel_information))
            elif args == 'id' or args =='channel_id':
                    channel_id = request.args[args]
                    channel_information = []
                    query = db.session.query(db_channel).filter_by(channel_id=channel_id)
                    for q in query:
                        channel_information.append({
                            'channel' : q.channel,
                            'channel_id' : q.channel_id,
                            'url' : q.original_url
                        })
                    return(jsonify(channel_information))
            elif args == 'search':
                download_results = download(search, video_range=1, download_confirm=False)
                channel_exists = db.session.query(db_channel).filter_by(webpage_url=download_results['original_url']).all()

                if not channel_exists:
                    db_entry = db_channel(
                        channel = download_results['channel'],
                        channel_follower_count = download_results['channel_follower_count'],
                        channel_id = download_results['channel_id'],
                        description = download_results['description'],
                        original_url = download_results['original_url'],
                        uploader = download_results['uploader'],
                        uploader_id = download_results['uploader_id'],
                        webpage_url = download_results['webpage_url'],
                        picture_profile = download_results['thumbnails'][18]['url'],
                        picture_cover = download_results['thumbnails'][15]['url'],
                        last_updated = current_time,
                        latest_upload = download_results['entries'][0]['original_url']

                    )
                    db.session.add(db_entry)
                    db.session.commit()

                # Requery after add
                channel_exists = db.session.query(db_channel).filter_by(webpage_url=download_results['original_url']).all()

                channel_information = {}
                for db_results in channel_exists:
                    channel_information = vars(db_results)
                    channel_information.pop("_sa_instance_state")

                return(channel_information)

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
                                'channel' : channel['channel'],
                                'channel_id' : channel['channel_id'],
                                'original_url' : channel['original_url'],
                                'title' : channel['title']
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

@app.route('/download',methods=['GET'])
def single_download():
    video = request.args.get('url')
    download(video)
    return ('Success')

app.run()