from datetime import datetime, timedelta

def getCurrentTime():
    now = datetime.now()
    return(now.strftime('%Y-%m-%d %H:%M:%S:%f'))

def getCurrentDateString():
    now = datetime.now() - timedelta(2)
    return(now.strftime('%Y%m%d'))