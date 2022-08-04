import ast
from datetime import datetime, timedelta
import os
from flask import jsonify
import redis
import json

from classes import Mongo

redis_db = redis.Redis(
    host=os.environ.get('REDIS_SERVER'),
    port='6379',
    decode_responses=True
)

def getCurrentTime():
    now = datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))

def getInitialVideosToLoad():
    now = datetime.now() - timedelta(int(os.environ.get('COUNT_VIDEOS_TO_LOAD')))
    return(now.strftime('%Y%m%d'))

def redis_publish(video_id, video_url, duration):
    redis_channel='download_queue'
    message = str({'video_url': video_url, 'video_id': video_id, 'duration': duration})
    redis_db.publish(redis_channel, message)
    return(message)

def redis_add_to_list(video_id, video_url, duration):
    redis_db = redis.Redis(
        host=os.environ.get('REDIS_SERVER'),
        port='6379',
        decode_responses=True
    )

    redis_channel = os.environ.get('REDIS_CHANNEL_NAME')

    message = str({'video_url': video_url, 'video_id': video_id, 'duration': duration})
    try:
        print(redis_db.rpush(redis_channel, message))
    except Exception as e:
        print(e)


def redis_cache_videos(data=None):
    if not redis_db.get('videos'):
        redis_db.set('videos', str(data))
        redis_db.expire('videos',600)
        return None
    else:
        result = redis_db.get('videos')
        return(ast.literal_eval(result))