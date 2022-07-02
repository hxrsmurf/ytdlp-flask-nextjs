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
    with open(f'{type}.txt', 'r') as f:
        data = f.read()

    if data:
        records = json.loads(data)
        if not input in records:
            records.append(input)

            with open(f'{type}.txt', 'w') as f:
                f.write(json.dumps(records, indent=2))