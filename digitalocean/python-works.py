import requests
import json

library = 'LIBRARYID'

url = "https://video.bunnycdn.com/library/LIBRARYID/videos"

payload = "{\"title\":\"test\"}"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/*+json",
    "AccessKey": "ACCESSKEY"
}

response = requests.post(url, data=payload, headers=headers)

guid = json.loads(response.text)['guid']
print(guid)


file = open('VIDEOID.mp4','rb')
video_url = f'https://video.bunnycdn.com/library/LIBRARYID/videos/{guid}'
print(video_url)
headers = {
    "Accept": "application/json",
    "AccessKey": "ACCESSKEY",
}
response = requests.put(video_url, headers=headers, data=file)

print(response)
