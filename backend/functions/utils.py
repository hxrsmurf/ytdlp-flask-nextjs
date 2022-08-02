from datetime import datetime, timedelta
import os
import redis

from classes import Mongo

def getCurrentTime():
    now = datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))

def getInitialVideosToLoad():
    now = datetime.now() - timedelta(int(os.environ.get('COUNT_VIDEOS_TO_LOAD')))
    return(now.strftime('%Y%m%d'))

def redis_publish(video_id, video_url, duration):
    redis_db = redis.Redis(
        host='127.0.0.1',
        port='6379',
        decode_responses=True
    )

    redis_channel='download_queue'
    message = str({'video_url': video_url, 'video_id': video_id, 'duration': duration})
    redis_db.publish(redis_channel, message)
    return(message)