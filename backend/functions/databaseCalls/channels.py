from classes import Channels
from sqlalchemy import collate, func, desc, asc

def getAllChannels():
    query = Channels.Channels.query.with_entities(Channels.Channels.id, Channels.Channels.channel_name).order_by(collate(Channels.Channels.channel_name, 'NOCASE')).all()
    return(query)

def getChannelById(channelID):
    query = Channels.Channels.query.filter_by(id=channelID).\
            with_entities(
                Channels.Channels.channel_name,
                Channels.Channels.channel_follower_count,
                Channels.Channels.channel_id,
                Channels.Channels.description,
                Channels.Channels.original_url,
                Channels.Channels.uploader,
                Channels.Channels.uploader_id,
                Channels.Channels.webpage_url,
                Channels.Channels.picture_profile,
                Channels.Channels.picture_cover,
                Channels.Channels.last_updated,
                Channels.Channels.latest_upload,
                )\
                .all()
    return(query)

def getChannelByName(channelName):
    return(Channels.Channels.query.filter_by(channel_name=channelName).first())

def getColumns():
    query = Channels.Channels.query.with_entities(
                Channels.Channels.channel_name,
                Channels.Channels.channel_follower_count,
                Channels.Channels.channel_id,
                Channels.Channels.description,
                Channels.Channels.original_url,
                Channels.Channels.uploader,
                Channels.Channels.uploader_id,
                Channels.Channels.webpage_url,
                Channels.Channels.picture_profile,
                Channels.Channels.picture_cover,
                Channels.Channels.last_updated,
                Channels.Channels.latest_upload,
                ).column_descriptions

    columns = []
    for column in query:
        columns.append(column['name'])

    return columns