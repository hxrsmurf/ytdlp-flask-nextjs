import os
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

with open('channels.txt', 'r') as f:
    for line in f:
        r.publish('queue',line)