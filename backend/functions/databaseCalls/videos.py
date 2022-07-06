from numpy import var
from classes import Videos
from sqlalchemy import func, desc, asc

def getAllVideos():
    query = Videos.Videos.query.with_entities(Videos.Videos.id, Videos.Videos.upload_date).order_by(Videos.Videos.upload_date.desc()).all()
    return(query)

def getVideoById(videoID):
    query = Videos.Videos.query.filter_by(id=videoID).\
            with_entities(
                Videos.Videos.id,
                Videos.Videos.channel,
                Videos.Videos.channel_id,
                Videos.Videos.description,
                Videos.Videos.duration,
                Videos.Videos.duration_string,
                Videos.Videos.fulltitle,
                Videos.Videos.video_id,
                Videos.Videos.like_count,
                Videos.Videos.view_count,
                Videos.Videos.original_url,
                Videos.Videos.thumbnail,
                Videos.Videos.title,
                Videos.Videos.upload_date,
                Videos.Videos.webpage_url,
                Videos.Videos.downloaded,
                Videos.Videos.downloaded_date,
                )\
                .all()
    return(query)

def getVideoByYouTubeId(youtubeId):
    return(Videos.Videos.query.filter_by(video_id=youtubeId).first())

def getVideoByChannelName(channelName):
    print(channelName)
    print(len(channelName))
    query = Videos.Videos.query.filter_by(channel=channelName).\
            with_entities(
                Videos.Videos.id,
                Videos.Videos.channel,
                Videos.Videos.channel_id,
                Videos.Videos.description,
                Videos.Videos.duration,
                Videos.Videos.duration_string,
                Videos.Videos.fulltitle,
                Videos.Videos.video_id,
                Videos.Videos.like_count,
                Videos.Videos.view_count,
                Videos.Videos.original_url,
                Videos.Videos.thumbnail,
                Videos.Videos.title,
                Videos.Videos.upload_date,
                Videos.Videos.webpage_url,
                Videos.Videos.downloaded,
                Videos.Videos.downloaded_date,
                )\
                .order_by(Videos.Videos.upload_date.desc())\
                .all()
    return (query)

def getColumns():
    query = Videos.Videos.query.with_entities(
                Videos.Videos.id,
                Videos.Videos.channel,
                Videos.Videos.channel_id,
                Videos.Videos.description,
                Videos.Videos.duration,
                Videos.Videos.duration_string,
                Videos.Videos.fulltitle,
                Videos.Videos.video_id,
                Videos.Videos.like_count,
                Videos.Videos.view_count,
                Videos.Videos.original_url,
                Videos.Videos.thumbnail,
                Videos.Videos.title,
                Videos.Videos.upload_date,
                Videos.Videos.webpage_url,
                Videos.Videos.downloaded,
                Videos.Videos.downloaded_date,
                ).column_descriptions

    columns = []
    for column in query:
        columns.append(column['name'])

    return columns