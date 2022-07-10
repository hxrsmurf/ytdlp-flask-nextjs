import datetime

def getCurrentTime():
    now = datetime.datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))