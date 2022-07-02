import os
import json
from flask import jsonify

def handler_json(channel, description, title, thumbnail, playlist, original_url):
    file_name = './data.txt'

    json_info = {
        'channel' : channel,
        'description' : description,
        'title': title,
        'thumbnail' : thumbnail,
        'playlist' : playlist,
        'original_url' : original_url
    }

    with open(file_name, 'r') as f:
        data = f.read()

    if not data:
        pass
    else:
        records = json.loads(data)
        records.append(json_info)

    with open(file_name, 'w') as f:
        f.write(json.dumps(records, indent=2))

def handler_json_file(type, input):
    if '.txt' in type:
        type = type.split('.')[0]

    with open(f'data/{type}.txt', 'r') as f:
        data = f.read()

    if not input:
        return(data)
    else:
        if data:
            records = json.loads(data)
            if not input in records:
                records.append(input)

                with open(f'data/{type}.txt', 'w') as f:
                    f.write(json.dumps(records, indent=2))

def handler_downloader(directory):
    if 'data' in directory:
        available_files = os.listdir(directory)
        return available_files

    if 'static' in directory:
        available_videos = []
        for root, dirs, files in os.walk(directory):
            channel_videos = []
            files.sort(reverse=True)
            if not root == 'static':
                for file in files:
                    channel_videos.append(file)

                available_videos.append({
                    'channel': root.split('\\')[1],
                    'videos': channel_videos
                })

        return (available_videos)