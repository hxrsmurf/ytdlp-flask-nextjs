import yt_dlp

def download(id):
    ydl_opts = {
        'playlistend': 1,
        'outtmpl' : '/tmp/%(id)s.%(ext)s',
        'ignoreerrors' : True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4',
        'ffmpeg_location': '/opt/python/ffmpeg'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(id, download=True)

    return info