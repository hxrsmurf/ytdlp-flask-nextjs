from email import header
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv('../.env')

library = os.environ.get("BUNNYCDN_LIBRARY")
api_key = os.environ.get("BUNNYCDN_KEY")
base_url = f'https://video.bunnycdn.com/library/{library}/videos'

headers = {
    "Accept": "application/json",
    "Content-Type": "application/*+json",
    "AccessKey": api_key
}

def bunnycdn_create_video(title):
    print('Getting Video GUID')
    payload = json.dumps({
        'title': title
    })

    response = requests.post(base_url, data=payload, headers=headers)
    return json.loads(response.text)['guid']

def bunnycdn_upload(title, video_id, url):
    guid = bunnycdn_create_video(title)
    print(f'Got {guid}')
    format_video_file = f'{video_id}/{video_id}.mp4'

    upload_video_file = open(format_video_file,'rb')
    video_url = f'{base_url}/{guid}'
    print('Uploading to BunnyCDN')
    response = requests.put(video_url, headers=headers, data=upload_video_file)

    if response.status_code == 200:
        print('Completed Upload to BunnyCDN')
    else:
        print('Failure to upload')

    return guid

def bunnycdn_get(id):
    video_url = f'{base_url}/{id}'
    response = requests.get(video_url, headers=headers)
    try:
        json_response = json.loads(response.text)
        return json_response['encodeProgress']
    except:
        return None

def bunnycdn_fetch(url, title):
    video_url = f'{base_url}/fetch'

    payload = json.dumps({
        'url': url,
        'title' : title
    })

    response = requests.post(base_url, data=payload, headers=headers)
    json_response = json.loads(response.text)
    return(json_response['guid'])

def bunnycdn_list():
    response = requests.get(base_url, headers=headers)
    return(json.loads(response.text))

def bunnycdn_list_broken_videos():
    videos = bunnycdn_list()
    bad_guids = []
    for video in videos['items']:
        guid = video['guid']
        status = video['status']
        if not status == 4:
            bad_guids.append(guid)

    return(bad_guids)

def bunnycdn_videos_broken_delete():
    guids = bunnycdn_list_broken_videos()
    for guid in guids:
        url = f'{base_url}/{guid}'
        try:
            print(f'Deleting {guid}')
            response = requests.delete(url, headers=headers)
            print(f'Success')
        except Exception as e:
            print(f'Error deleting {guid} -- {e}')

        if response.status_code == 200:
            print(f'Successfully deleted {guid}')
        else:
            print(f'Error deleting {guid}')

    return(guids)
