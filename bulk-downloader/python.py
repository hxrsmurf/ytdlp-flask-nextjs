import argparse
import yt_dlp

parser = argparse.ArgumentParser()
parser.add_argument("--channel", "-c")
args = parser.parse_args()

ytdl_opts = {
    'outtmpl' : '/mnt/videos/%(uploader)s/%(id)s.%(ext)s',
    'windowsfilenames': True,
    'playlistend' : 1,
    'ignoreerrors' : True,
    'format': 'bestvideo*+bestaudio/best',
    'merge_output_format': 'mp4'
}

with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
    ydl.extract_info(args.channel, download=True)