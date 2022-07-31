$video_id = ''
$directory = ''

docker run -v ${directory}:/media:Z tnk4on/yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output '%(id)s/%(id)s.%(ext)s' https://youtu.be/$video_id
ffmpeg -i $video_id/$video_id.mp4 -c:v libx264 -c:a copy -flags +cgop -g 30 -hls_time 1 -hls_playlist_type event $video_id/$video_id.m3u8