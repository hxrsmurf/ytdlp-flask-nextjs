import os
import requests
from yt_dlp import YoutubeDL

from classes import Mongo

from .backblaze_upload import b2_upload

def download(video, video_range=2, download_confirm=False):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        #'outtmpl' : 'static/%(uploader)s/%(upload_date>%Y-%m-%d)s_%(id)s_%(title)s.%(ext)s',
        'outtmpl' : '%(id)s/%(id)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        #'download_archive': 'static/downloaded_videos.txt',
        'windowsfilenames': True,
        'playlistend' : video_range,
        'ignoreerrors' : True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=download_confirm)
        return info

def download_thumbnail(thumbnail_url, video_id):
    video_thumbnail_output_name = f'{video_id}.jpg'
    video_thumbnail_folder = 'video_thumbnails'
    cdn_video_thumbnail_url = f'{os.environ.get("CDN_URL")}/{os.environ.get("B2_BUCKET")}/{video_thumbnail_folder}/{video_thumbnail_output_name}'

    if '8ZMxwS57b4A' in thumbnail_url:
        thumbnail_request = requests.get(thumbnail_url, stream=True)
        if thumbnail_request.status_code == 200:
            with open(video_thumbnail_output_name, 'wb') as file:
                file.write(thumbnail_request.content)
            b2_upload(file=video_thumbnail_output_name,folder=video_thumbnail_folder)
        Mongo.Videos.objects(video_id=video_id).update_one(set__cdn_video_thumbnail=cdn_video_thumbnail_url)