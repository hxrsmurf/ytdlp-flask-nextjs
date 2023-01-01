import logging
import os
import subprocess

from functions.download import download

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    URL = 'https://www.youtube.com/@MrBeast'
    #video_id = '7IKab3HcfFk'
    video_url = 'https://www.youtube.com/watch?v=7IKab3HcfFk'
    video_id = download(video_url)
    videos = os.listdir('/tmp/')
    for video in videos:
        ffmpeg_cmd = f'/opt/python/ffmpeg -i /tmp/{video} -c copy -flags +cgop -g 30 -hls_time 2 -hls_playlist_type event /tmp/{video_id}.m3u8'
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(os.listdir('/tmp/'))

    return({
            'statusCode': 200,
            'body': 'Success'
    })