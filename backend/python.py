import os
import json
from flask import Flask, jsonify, request, redirect
from sqlalchemy import desc
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import datetime

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

    def __init__(self, channel, channel_follower_count, channel_id, description, original_url, uploader, uploader_id, webpage_url, picture_profile, picture_cover, last_updated):
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

class db_videos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    channel = db.Column(db.String(100))
    description = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    duration_string = db.Column(db.String(100))
    fulltitle = db.Column(db.String(100))
    video_id = db.Column(db.String(100))
    like_count = db.Column(db.String(100))
    original_url = db.Column(db.String(100))
    thumbnail = db.Column(db.String(100))
    title = db.Column(db.String(100))
    upload_date = db.Column(db.String(100))
    webpage_url = db.Column(db.String(100))
    downloaded = db.Column(db.Boolean)

    def __init__(self, channel, description, duration, duration_string, fulltitle, video_id, like_count, original_url, thumbnail, title, upload_date, webpage_url, downloaded):
        self.channel = channel
        self.description = description
        self.duration = duration
        self.duration_string = duration_string
        self.fulltitle = fulltitle
        self.video_id = video_id
        self.like_count = like_count
        self.original_url = original_url
        self.thumbnail = thumbnail
        self.title = title
        self.upload_date = upload_date
        self.webpage_url = webpage_url
        self.downloaded = downloaded

db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def query_records():
    if request.args:
        video_url = request.args.get('video')

        parse_video_url = video_url.split('/')

        if not 'youtube.com' in parse_video_url[2]:
            return json.dumps({'message': 'Not Youtube'}), 400, {'ContentType':'application/json'}
        else:
            def hook(d):
                if d['status'] == 'finished':
                    return(d['filename'])

            ytdl_opts = {
                'outtmpl' : 'static/%(uploader)s/%(title)s.%(ext)s',
                'progress_hooks' : [hook],
                'daterange' : 'today-1weeks',
                'ignoreerrors' : True
            }

            # http://127.0.0.1:5000/?video=https://www.youtube.com/watch?v=KjR0H8N94Ek
            # http://127.0.0.1:5000/?video=https://www.youtube.com/playlist?list=PLIwiAebpd5CJiaj64YaRzbW5XhymIXS6V
            # http://127.0.0.1:5000/?video=https://www.youtube.com/c/aliensrock

            with YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                filename = filename.replace('\\','/')

                title, thumbnail, playlist = None, None, None

                try:
                    if not info['_type']:
                        title = info['fulltitle']
                        thumbnail = info['thumbnail']
                        playlist = info['playlist']
                except:
                    thumbnail = None
                    playlist = True
                    title = info['title']

                channel = info['channel']
                description = info['description']
                original_url = info['original_url']

                handler_json(channel, description, title, thumbnail, playlist, original_url)

                return redirect(f'http://127.0.0.1:5000/{filename}')

    else:
        with open('data.txt', 'r') as f:
            data = json.loads(f.read())
            return jsonify(data)

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
        download_results = download(search, 1)
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
                last_updated = current_time
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
    if not request.args:
        db_results = db_videos.query.all()
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
                all_channels =  db.session.query(db_videos.channel).order_by(db_videos.channel).distinct().all()
                print(all_channels)
                return(jsonify(all_channels))
            elif args == 'search':
                search_query = request.args[args]
                channel_videos = db.session.query(db_videos).filter_by(channel=search_query).all()
                all_channel_videos = []
                for videos in channel_videos:
                    video_information = vars(videos)
                    video_information.pop("_sa_instance_state")
                    all_channel_videos.append(video_information)
                return(jsonify(all_channel_videos))
            elif args == 'add':
                add_query = request.args[args]
                download_results = download(add_query, 1)
                download_exists = db.session.query(db_videos).filter_by(video_id=download_results['id']).all()
                if not download_exists:
                    db_entry = db_videos(
                        channel = download_results['channel'],
                        description = download_results['description'],
                        duration = download_results['duration'],
                        duration_string = download_results['duration_string'],
                        fulltitle = download_results['fulltitle'],
                        video_id = download_results['id'],
                        like_count = download_results['like_count'],
                        original_url = download_results['original_url'],
                        thumbnail = download_results['thumbnail'],
                        title = download_results['title'],
                        upload_date = download_results['upload_date'],
                        webpage_url = download_results['webpage_url'],
                        downloaded = False
                    )

                    db.session.add(db_entry)
                    db.session.commit()
                    return(jsonify({'result' : 'success'}))
                else:
                    return('Already downloaded')

@app.route('/download_all_videos', methods=['GET'])
@cross_origin()
def download_all_videos():
    files = handler_downloader('data')
    available_files = []

    for file in files:
        file_data = handler_json_file(file, input=None)
        available_files.append({file:file_data})

    # Bad way to iterate through the JSON and get the values.
    for key, value in enumerate(available_files):
        json_array = json.loads(json.dumps(value))
        for key, value in json_array.items():
            json_value = json.loads(value)
            if len(json_value) >= 1:
                for j in json_value:
                    download(j)

    return(jsonify(available_files))

@app.route('/available_videos', methods=['GET'])
def available_videos():
    available_files = handler_downloader('static')
    return(jsonify(available_files))

@app.route('/download',methods=['GET'])
def single_download():
    video = request.args.get('url')
    download(video)
    return ('Success')

@app.route('/test_env_variables')
def test():
    API_url = os.environ.get("API_url")
    return(API_url)

@app.route('/sqlalchemy')
def db_sqllite():
    if request.args:
        request_data = request.args.get('channels')
        # http://127.0.0.1:5000/sqlalchemy?channels=test
        if request_data:
            query_result = db.session.query(db_channel).filter_by(channel=request_data).all()
            if not query_result:
                db_entry = db_channel(request_data)
                db.session.add(db_entry)
                db.session.commit()
                return('Success')
            else:
                return('Record already exists')
        else:
            db_results = db_channel.query.all()
            all_db_results = []

            for result in db_results:
                all_db_results.append({
                    'id' : result.id,
                    'channel' : result.channel,
                    'videos' : result.videos
                })

            return(jsonify(all_db_results))
    else:
        return('Hello World')

app.run()