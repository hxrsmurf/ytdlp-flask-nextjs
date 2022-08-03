from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def add(x,y):
    return x+y

# windows
# celery -A tasks worker --loglevel=INFO --pool=solo