from yt_dlp import YoutubeDL

def youtube_download(video):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : '%(id)s/%(id)s.%(ext)s',
        #'progress_hooks' : [hook],
        #'daterange' : 'today-1year',
        'windowsfilenames': True,
        'playlistend' : 1,
        'ignoreerrors' : True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=True)
        return info
