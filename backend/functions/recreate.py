import requests
import concurrent.futures
import json

def add_channel(channel):
    url = f'{API_URL}/mongo/channels/add?url={channel}'
    requests.get(url)
    return(url)

def get_latest(range):
    url = f'{API_URL}/mongo/download/latest?range={range}&id=all'
    requests.get(url)
    print('Completed latest')

def recreate_channels(debug=True):
    x = 0
    channels = []
    threads = []
    with open('recreate.txt', 'r') as file:
        for line in file.readlines():
            channels.append(line.strip())

    if debug:
        max_range = 10
    else:
        max_range = len(channels)

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for channel in channels:
            if x == max_range:
                break
            else:
                threads.append(executor.submit(add_channel, channel))
                x+=1

    for futures in concurrent.futures.as_completed(threads):
        print(futures.result())

    print('Completed recreate')

def get_channel_ids(API_URL):
    result = requests.get(f'{API_URL}/mongo/channels/')
    json_result = json.loads(result.content)
    channel_ids = []
    for channel in json_result:
        channel_ids.append(channel['_id'])

    return(channel_ids)

def download_photo_cover(channel_ids):
    threads = []

    def download(url):
        try:
            requests.get(url)
            return(f'Success for {url}')
        except:
            return(f'Error for {url}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for id in channel_ids:
            url = f'{API_URL}/mongo/download/channel/cover/{id}'
            threads.append(executor.submit(download,url))

    for futures in concurrent.futures.as_completed(threads):
        print(futures.result())

API_URL = 'http://127.0.0.1:5000'
#recreate_channels(debug=True)
#get_latest(1)

#channel_ids = get_channel_ids(API_URL)
#download_photo_cover(channel_ids)