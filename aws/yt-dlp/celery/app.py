from celery import Celery
from functions.downloader import download

app_celery = Celery('tasks')
app_celery.conf.broker_url = 'redis://redis:6379/0'

@app_celery.task(name='tasks.download_web')
def download_web(url):
    range = 1
    confirm = True
    download_result = download(video=url, video_range=range, download_confirm=confirm)
    return download_result