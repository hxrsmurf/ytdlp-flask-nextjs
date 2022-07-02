from yt_dlp import YoutubeDL

def download(video):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : 'static/%(uploader)s/%(upload_date>%Y-%m-%d)s_%(id)s_%(title)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        'download_archive': 'static/downloaded_videos.txt'
    }

    if '/c/' in video:
        ytdl_opts['playlistend'] = 5 # Not sure how the python daterange works.

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=True)