import json
from flask import Flask, jsonify, request, redirect, url_for
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin

from functions.handler_json import handler_json, handler_json_file

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
                'daterange' : 'today-1weeks'
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

                #return (info)

                return redirect(f'http://127.0.0.1:5000/{filename}')

    else:
        with open('data.txt', 'r') as f:
            data = json.loads(f.read())
            print(data)
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

app.run()