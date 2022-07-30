from yt_dlp import YoutubeDL
import os

def handler(event, context):
    # https://github.com/kousiktn/lambda-youtube-dl/blob/master/youtubedl/downloader/views.py
    # https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
    # https://github.com/serverlesspub/ffmpeg-aws-lambda-layer

    # sam build; sam deploy --no-confirm-changeset

    try:
        ytdl_opts = {
            'outtmpl' : '/tmp/%(id)s.%(ext)s',
            'windowsfilenames': True,
            'playlistend' : 1,
            'ignoreerrors' : True,
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': 'mp4'
        }

        with YoutubeDL(ytdl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=RlOB3UALvrQ'])

        files = os.listdir('/tmp/')

        print(files)
        return(files)
    except Exception as e:
        print(e)
        return(e)