from flask import Flask, request
from functions.downloader import download

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/download', methods=['GET'])
def download_web():
    url = request.args['url']
    range = 1
    confirm = False
    download_result = download(video=url, video_range=range, download_confirm=confirm)
    return download_result

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)