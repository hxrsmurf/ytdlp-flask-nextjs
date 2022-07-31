from datetime import datetime, timedelta
import os

def getCurrentTime():
    now = datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))

def getInitialVideosToLoad():
    now = datetime.now() - timedelta(int(os.environ.get('COUNT_VIDEOS_TO_LOAD')))
    return(now.strftime('%Y%m%d'))