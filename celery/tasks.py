from celery import Celery
from celery.schedules import crontab
import requests

app = Celery('tasks', broker='redis://127.0.0.1:6379')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1, query, name='test')

@app.task
def test(arg):
    print(arg)

@app.task
def add(x,y):
    print(x+y)
    return x+y

@app.task
def query():
    print('test')
    base_api_url = 'https://api.youtube'
    api_url = base_api_url + '/mongo/videos/'
    requests.get(api_url)


# windows
# celery -A tasks worker --loglevel=INFO --pool=solo

# WSL
# python3 -m celery -A tasks beat -l info