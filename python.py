import json
from flask import Flask, jsonify, request, redirect, url_for
from yt_dlp import YoutubeDL

app = Flask(__name__)
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
                'progress_hooks' : [hook]
            }

            # http://127.0.0.1:5000/?video=https://www.youtube.com/

            with YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(video, download=True)
                filename = ydl.prepare_filename(info)
                filename = filename.replace('\\','/')
                return redirect(f'http://127.0.0.1:5000/{filename}')

    else:
        with open('data.txt', 'r') as f:
            data = json.loads(f.read())
            print(data)
            return jsonify(data)

@app.route('/', methods=['PUT'])
def create_record():
    try:
        record = json.loads(request.data)
    except:
        request_data = request.data.decode('UTF-8')
        record = {'youtube': request_data}
        print(record)

    with open('data.txt', 'r') as f:
        data = f.read()

    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))

    return jsonify(record)

app.run()