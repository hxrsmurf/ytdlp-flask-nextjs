from flask import Flask, request
from celery import Celery
from functions.downloader import download

app = Flask(__name__)
app_celery = Celery('tasks')
app_celery.conf.broker_url = 'redis://localhost:6379/0'

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/download', methods=['GET'])
def download_route():
    url = request.args['url']
    range = 1
    download_web.delay(url)
    return ('Success')

@app_celery.task(name='tasks.download_web')
def download_web(url):
    range = 1
    confirm = True
    download_result = download(video=url, video_range=range, download_confirm=confirm)
    return download_result

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)