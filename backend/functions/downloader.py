from yt_dlp import YoutubeDL
from functions.backblaze_upload import b2_upload

def download(video, video_range=1, download_confirm=False):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : 'static/%(uploader)s/%(upload_date>%Y-%m-%d)s_%(id)s_%(title)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        #'download_archive': 'static/downloaded_videos.txt',
        'windowsfilenames': True
    }

    if '/c/' in video or '/user/' in video:
        ytdl_opts['playlistend'] = video_range # Not sure how the python daterange works.

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=download_confirm)
        return info
        filename = ydl.prepare_filename(info)