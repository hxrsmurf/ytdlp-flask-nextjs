from datetime import datetime, timedelta
import os
import json
import redis

from classes import Mongo

def getCurrentTime():
    now = datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))

def getInitialVideosToLoad():
    now = datetime.now() - timedelta(int(os.environ.get('COUNT_VIDEOS_TO_LOAD')))
    return(now.strftime('%Y%m%d'))

def redis_publish(video_id,url):
    query = json.loads((Mongo.Videos.objects(video_id=video_id)).to_json())[0]
    video_id = query['_id']
    original_url = query['original_url']

    redis_db = redis.Redis(
        host='127.0.0.1',
        port='6379',
        decode_responses=True
    )

    redis_channel='download_queue'
    message = str({'url': url, 'video_id': video_id})
    redis_db.publish(redis_channel, message)
    return(message)