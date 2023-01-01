import json
import yt_dlp

def get_channel(id):
    ydl_opts = {
        'playlistend': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(id, download=False)
        info = json.dumps(ydl.sanitize_info(info))

    return info