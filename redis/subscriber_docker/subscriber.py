import redis
import time
import ast

from functions import youtube_download

r = redis.Redis(
    host='192.168.1.58',
    port='6379',
    decode_responses=True
)

p = r.pubsub()
p.subscribe('download_queue')

while True:
    message = p.get_message()
    if message:
        #print(message)
        try:
            message_json = ast.literal_eval(message['data'])
            url = message_json['url']
            video_id = message_json['video_id']
            print(f'{url} - {video_id}')
            youtube_download(video=url)
            print(f'Completed {video_id}')
        except Exception as e:
            print(f'{message} -- {e}')
    time.sleep(1)