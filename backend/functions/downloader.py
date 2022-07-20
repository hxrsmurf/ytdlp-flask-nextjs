from yt_dlp import YoutubeDL

def download(video, video_range=2, download_confirm=False):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        #'outtmpl' : 'static/%(uploader)s/%(upload_date>%Y-%m-%d)s_%(id)s_%(title)s.%(ext)s',
        'outtmpl' : 'static/%(id)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        #'download_archive': 'static/downloaded_videos.txt',
        'windowsfilenames': True,
        'playlistend' : video_range,
        'ignoreerrors' : True
    }

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=download_confirm)
        return info