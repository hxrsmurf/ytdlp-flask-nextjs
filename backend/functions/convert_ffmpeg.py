import asyncio
from ffmpeg import FFmpeg
# https://github.com/jonghwanhyeon/python-ffmpeg

def convert_to_hls(video_id):
    source_path = f'{video_id}/{video_id}.mp4'
    destination_path = f'{video_id}/{video_id}.m3u8'
    print(f'Converting to HLS\nSource: {source_path}\nDestination:{destination_path}')

    ffmpeg = FFmpeg().option('y').input(
        source_path,

    ).output(
        destination_path,
        {'c:v': 'libx264', 'c:a': 'copy'},
        flags='+cgop',
        g=30,
        hls_time=10,
        hls_playlist_type='event',
    )

    @ffmpeg.on('start')
    def on_start(arguments):
        print('Arguments:', arguments)

    @ffmpeg.on('stderr')
    def on_stderr(line):
        print('stderr:', line)

    @ffmpeg.on('progress')
    def on_progress(progress):
        print(progress)

    @ffmpeg.on('progress')
    def time_to_terminate(progress):
        # Gracefully terminate when more than 200 frames are processed
        #if progress.frame > 200:
        #    ffmpeg.terminate()
        pass

    @ffmpeg.on('completed')
    def on_completed():
        print('Completed')

    @ffmpeg.on('terminated')
    def on_terminated():
        print('Terminated')

    @ffmpeg.on('error')
    def on_error(code):
        print('Error:', code)

    asyncio.run(ffmpeg.execute())