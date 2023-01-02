import requests
import logging
import redis
import json
import yt_dlp
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

logging.basicConfig(level='INFO')

recreate_file = 'recreate.txt'
api_url = 'http://localhost:3000/api/addChannel?id='
base_url = 'https://6vgaxmdml7.execute-api.us-east-1.amazonaws.com/?id='

list_channels = []

r = redis.Redis(
    host='localhost',
    port='6379'
)


def get_channel(channel, download):
    ydl_opts = {
        'playlistend': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel, download=download)
            profile = info['thumbnails'][18]['url'],
            cover = info['thumbnails'][15]['url'],
        except Exception as e:
            logging.error(channel, e)
    return cover, profile


def blah():
    with open(recreate_file, 'r') as file:
        for line in file.readlines():
            channel = line.strip()
            check_valid_channel = False

            if check_valid_channel:
                result = requests.get(channel)
                status_code = result.status_code
                if status_code == 404:
                    print(channel)
            else:
                cover, profile = get_channel(channel)
                list_channels.append({
                    'url': channel,
                    'cover': cover,
                    'profile': profile
                })

    try:
        r.set('channels', json.dumps(list_channels))
    except Exception as e:
        logging.error('Error', e)


def read_file(file):
    list_contents = []
    with open(file, 'r') as f:
        for line in f.readlines():
            list_contents.append(line.strip())
    return list_contents


def get_channel_info(channel):
    url = base_url + channel
    logging.info(channel)
    result = requests.get(url)
    return result.content


def thready():
    file_contents = read_file(recreate_file)
    #file_contents = ['https://www.youtube.com/@MrBeast']
    start = perf_counter()
    with ThreadPoolExecutor(max_workers=100000000000) as pool:
        #results = pool.map(get_channel_info, file_contents)
        results = pool.map(get_channel, file_contents)

    for result in results:
        logging.info(result)

    finish = perf_counter()

    logging.info(f'{start} - {finish} - {finish - start}')


def multiprocessy():
    file_contents = read_file(recreate_file)
    procs = []
    start = perf_counter()

    for channel in file_contents:
        #proc = Process(target=get_channel, args=(channel,False))
        proc = Process(target=get_channel_info, args=(channel,))
        logging.info(channel)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    finish = perf_counter()
    logging.info(f'{start} - {finish} - {finish - start}')

def celery():
    file_contents = read_file(recreate_file)
    for channel in file_contents:
        url = f'http://homelabwithkevin.com:8080/download?url={channel}'
        result = requests.get(url)
        print(result.status_code)

if __name__ == '__main__':
    celery()