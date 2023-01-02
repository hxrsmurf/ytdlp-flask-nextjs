from yt_dlp import YoutubeDL

def download(video, video_range=2, download_confirm=False):
    def hook(d):
            if d['status'] == 'finished':
                return(d['filename'])

    ytdl_opts = {
        'outtmpl' : '%(id)s/%(id)s.%(ext)s',
        'progress_hooks' : [hook],
        #'windowsfilenames': True,
        'playlistend' : video_range,
        #'ignoreerrors' : True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(video, download=download_confirm)
        return info