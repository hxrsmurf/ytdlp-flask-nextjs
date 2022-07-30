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