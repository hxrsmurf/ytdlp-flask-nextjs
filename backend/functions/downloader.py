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

    # http://127.0.0.1:5000/?video=https://www.youtube.com/watch?v=KjR0H8N94Ek
    # http://127.0.0.1:5000/?video=https://www.youtube.com/playlist?list=PLIwiAebpd5CJiaj64YaRzbW5XhymIXS6V
    # http://127.0.0.1:5000/?video=https://www.youtube.com/c/aliensrock

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=True)
        filename = ydl.prepare_filename(info)
        filename = filename.replace('\\','/')