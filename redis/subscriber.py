import redis
import time
import ast

r = redis.Redis(
    host='127.0.0.1',
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
            id = message_json['id']
            print(f'{url} - {id}')
        except Exception as e:
            print(f'{message} -- {e}')
    time.sleep(1)