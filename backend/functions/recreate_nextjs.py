import requests
import logging
import redis
import json

logging.basicConfig(level='INFO')

recreate_file = 'recreate.txt'
api_url = 'http://localhost:3000/api/addChannel?id='
list_channels = []

r = redis.Redis(
    host='localhost',
    port='6379'
)

with open(recreate_file, 'r') as file:
    for line in file.readlines():
        channel = line.strip()
        check_valid_channel = False

        if check_valid_channel:
            result = requests.get(channel)
            status_code = result.status_code
            if status_code == 404:
                print(channel)
        else:
            list_channels.append(channel)

try:
    r.set('channels', json.dumps(list_channels))
except Exception as e:
    logging.error('Error', e)