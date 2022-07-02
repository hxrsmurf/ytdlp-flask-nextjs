import os
import json
from flask import Flask, jsonify, request, redirect
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

from functions.handler_json import handler_json, handler_json_file, handler_downloader
from functions.downloader import download

load_dotenv('.env')
app = Flask(__name__)
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
    search = request.args.get('search')
    if search:
        # http://127.0.0.1:5000/channels?search=https://www.youtube.com/c/aliensrock

        handler_json_file('channels', search)

        return('Success')
    else:
        search = None
        return(handler_json_file('channels', search))


@app.route('/videos', methods=['GET'])
@cross_origin()
def videos():
    search = request.args.get('search')
    if search:
        # http://127.0.0.1:5000/channels?search=https://www.youtube.com/c/aliensrock

        handler_json_file('videos', search)

        return('Success')
    else:
        search = None
        return(handler_json_file('videos', search))

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

app.run()