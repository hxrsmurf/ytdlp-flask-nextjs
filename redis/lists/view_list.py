import time

from shared import redis_db

redis_queue_name = 'download-queue'

while True:
    print(redis_db().lrange(redis_queue_name, 0, -1))
    time.sleep(2)