import time
import redis

r = redis.Redis(
    host='127.0.0.1',
    port='6379'
)

loop = False

def publish():
    test = {"original_url": "test", "video_id": "555"}
    r.publish('download_queue',str(test))

if loop:
    while True:
        publish()
        time.sleep(1)
else:
    publish()