import requests
import concurrent.futures

def add_channel(channel):
    url = f'{API_URL}/channels/add?url={channel}'
    requests.get(url)
    return(url)

def get_latest(range):
    url = f'{API_URL}/download/latest?range={range}&id=all'
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


API_URL = 'http://127.0.0.1:5000'
#recreate_channels(debug=True)
#get_latest(1)