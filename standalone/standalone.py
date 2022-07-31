import asyncio
import json
import os
import requests
import sys

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

if __name__ == "__main__":
    FEATURE_DOWNLOAD = False
    config = parse_config()
    API_URL = config['API_URL']

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
        response = requests.get(f'{API_URL}/mongo/videos')
        response_json = json.loads(response.content)

        for video in response_json:
            video_id = video['_id']
            original_url = video['original_url']
            channel_name = video['channel_name']
            thumbnail_url = video['thumbnail']

            if 'HelloWorld' in channel_name and FEATURE_DOWNLOAD:
                if not os.path.exists(f'{video_id}/{video_id}.webp'):
                    download_thumbnail(thumbnail_url=thumbnail_url,video_id=video_id)

                if not os.path.exists(video_id):
                    download(video=original_url, video_range=1, download_confirm=True)
                    convert_to_hls(video_id=video_id)