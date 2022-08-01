import time
import redis

r = redis.Redis(
    host='127.0.0.1',
    port='6379'
)

test = {"url": "test", "id": "1234"}
print(type(test))
while True:
    r.publish('test',str(test))
    time.sleep(1)
