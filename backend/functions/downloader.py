from yt_dlp import YoutubeDL

def download(video):
    if video == None:
        pass

    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : 'static/%(uploader)s/%(title)s.%(ext)s',
        'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        'download_archive': 'downloaded_videos.txt'
    }

    if '/c/' in video:
        ytdl_opts['playlistend'] = 30 # Not sure how the python daterange works.

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=True)
        filename = ydl.prepare_filename(info)
        filename = filename.replace('\\','/')