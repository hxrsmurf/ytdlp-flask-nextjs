import asyncio
import json
import os
import requests
import shutil
import subprocess
import sys

import redis
import time
import ast


from ffmpeg import FFmpeg
from yt_dlp import YoutubeDL

def convert_to_hls(video_id, url=None):
    if url:
        source_path = url
    else:
        source_path = f'{video_id}/{video_id}.mp4'

    destination_path = f'{video_id}/{video_id}.m3u8'
    print(f'Converting to HLS\nSource: {source_path}\nDestination: {destination_path}')

    ffmpeg = FFmpeg().option('y').input(
        source_path,
    ).output(
        destination_path,
        {'c:v': 'libx264', 'c:a': 'copy'},
        flags='+cgop',
        g=30,
        hls_time=10,
        hls_playlist_type='event',
    )

    @ffmpeg.on('start')
    def on_start(arguments):
        print('Arguments:', arguments)

    @ffmpeg.on('stderr')
    def on_stderr(line):
        print('stderr:', line)

    @ffmpeg.on('progress')
    def on_progress(progress):
        print(progress)

    @ffmpeg.on('progress')
    def time_to_terminate(progress):
        pass

    @ffmpeg.on('completed')
    def on_completed():
        print('Completed')

    @ffmpeg.on('terminated')
    def on_terminated():
        print('Terminated')

    @ffmpeg.on('error')
    def on_error(code):
        print('Error:', code)

    asyncio.run(ffmpeg.execute())


def download(video, video_range=2, download_confirm=False):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : '%(id)s/%(id)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        'windowsfilenames': True,
        'playlistend' : video_range,
        'ignoreerrors' : True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=download_confirm)
        return info

def download_thumbnail(thumbnail_url,video_id):
    response_thumbnail = requests.get(thumbnail_url)
    destination_thumbnail = f'{video_id}/{video_id}'
    with open(f'{destination_thumbnail}.webp', 'wb') as f:
        f.write(response_thumbnail.content)

def parse_config():
    with open('config.json', 'r') as f:
        file_data = f.read()

    return json.loads(file_data)

def redis_subscriber():
    print('Starting redis subscriber')

    r = redis.Redis(
        host=config['REDIS_URL'],
        port='6379',
        decode_responses=True
    )

    p = r.pubsub()
    p.subscribe('download_queue')

    while True:
        time.sleep(1)
        message = p.get_message()
        if message:
            try:
                message_json = ast.literal_eval(message['data'])
                original_url = message_json['video_url']
                video_id = message_json['video_id']
                duration_seconds = message_json['duration'] # Seconds

                check_exists_cdn = requests.head(f'{CDN_URL}/{video_id}/{video_id}.mp4')
                print(f'{video_id} - {check_exists_cdn}')
                if not check_exists_cdn == 200:
                    if duration_seconds >= 600:
                        # To Do: After AWS upload, properly mark video complete
                        print(f'Send to AWS: {video_id}')
                        aws_api = f'{AWS_API_URL}/?id={video_id}'
                        print(requests.get(aws_api))
                        requests.get(f'{API_URL}/mongo/download/queue/{video_id}/complete')
                    else:
                        if not isWindowsOS:
                            subprocess.call(['./docker.sh',original_url,video_id])
                            if os.path.exists(f'/tmp/{video_id}'):
                                shutil.rmtree(f'/tmp/{video_id}')
                        elif isWindowsOS:
                            download(video=original_url,video_range=1, download_confirm=True)

                    if RUNNING_LOCAL:
                        pass
                    else:
                        requests.get(f'{API_URL}/mongo/download/queue/{video_id}/complete')

            except Exception as e:
                print(f'{message} -- {e}')

def redis_get_list():
    redis_db = redis.Redis(host=config['REDIS_URL'], port='6379', decode_responses=True)
    while True:
        message = redis_db.blpop([config['REDIS_QUEUE_NAME']],30)
        if not message:
            continue
        else:
            queue_message = ast.literal_eval(message[1])
            video_id = queue_message['video_id']
            video_url = queue_message['video_url']
            duration_seconds = queue_message['duration']

            check_exists_cdn = requests.head(f'{CDN_URL}/{video_id}/{video_id}.mp4')
            print(f'{video_id} - {check_exists_cdn}')
            if not check_exists_cdn == 200:
                if duration_seconds >= 180:
                    # To Do: After AWS upload, properly mark video complete
                    print(f'Send to AWS: {video_id}')
                    if not RUNNING_LOCAL:
                        aws_api = f'{AWS_API_URL}/?id={video_id}'
                        print(requests.get(aws_api))
                else:
                    if not isWindowsOS:
                        subprocess.call(['./docker.sh',video_url,video_id])
                        if os.path.exists(f'/tmp/{video_id}'):
                            shutil.rmtree(f'/tmp/{video_id}')
                    elif isWindowsOS:
                        download(video=video_url,video_range=1, download_confirm=True)

                if RUNNING_LOCAL:
                    break
                else:
                    requests.get(f'{API_URL}/mongo/download/queue/{video_id}/complete')

if __name__ == "__main__":
    FEATURE_DOWNLOAD, isWindowsOS, FEATURE_AWS_PROCESSING = True, False, False

    config = parse_config()
    RUNNING_LOCAL = config['RUNNING_LOCAL']

    if RUNNING_LOCAL:
        API_URL = config['LOCAL_API_URL']
    else:
        API_URL = config['API_URL']
    CDN_URL = config['CDN_URL']
    AWS_API_URL = config['AWS_API_URL']

    if os.name == 'nt':
        isWindowsOS = True

    # Used for quck, local runs
    if not len(sys.argv) == 1:
        video_id = sys.argv[1]
        if 'https' in video_id:
            youtube_url = video_id
        else:
            youtube_url = f'https://youtu.be/{video_id}'
        print(youtube_url)
        download(video=youtube_url, video_range=1, download_confirm=True)
        print(f'Successfully downloadeded {video_id}')
    else:
        redis_get_list()