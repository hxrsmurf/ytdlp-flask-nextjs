import redis

def redis_db():
    return redis.Redis(
        host='127.0.0.1',
        port='6379'
    )