import requests
def download_queue():
            response = requests.get(f'{API_URL}/mongo/download/queue/')
            response_json = json.loads(response.content)

            if len(response_json) == 0:
                print('Nothing queued to download')
            else:
                for video in response_json:
                    video_id = video['video_id']
                    original_url = video['webpage_url']
                    duration = video['duration']
                    check_exists_cdn = requests.head(f'{CDN_URL}/{video_id}/{video_id}.mp4')
                    print(f'{video_id} - {check_exists_cdn}')