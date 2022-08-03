from shared import redis_db

redis_queue_name = 'download_queue'

while True:
    message = redis_db().blpop(redis_queue_name, 30)
    if not message:
        continue
    else:
        print(message)