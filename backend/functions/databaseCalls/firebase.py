import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import jsonify
import json

from functions.utils import getCurrentTime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def addChannel(information, empty=False):
    channels_ref = db.collection(u'channels').document(information['channel_id'])
    if empty == True:
        print('Setting empty')
        channels_ref.set({
            'empty' : True
        })
        return(information)
    elif empty == False:
        channels_ref.set({
            'channel_id' : information['channel_id'],
            'channel_name' : information['channel'],
            'channel_follower_count' : information['channel_follower_count'],
            'description' : information['description'],
            'original_url' : information['original_url'],
            'uploader' : information['uploader'],
            'uploader_id' : information['uploader_id'],
            'webpage_url' : information['webpage_url'],
            'picture_profile' : information['thumbnails'][18]['url'],
            'picture_cover' : information['thumbnails'][15]['url'],
            'last_updated' : getCurrentTime(),
            'latest_upload' : information['entries'][0]['original_url']
        })
    else:
        return(f'There was an error adding {information}.')
    return(jsonify(information))

def getChannel(information):
    channels_ref = db.collection(u'channels').document(information)

    doc = channels_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        return(jsonify(doc.to_dict()))
    else:
        return False

def getAllChannels():
    channels_ref = db.collection(u'channels')
    query = channels_ref.order_by('channel_name')
    ordered_channels = query.stream()
    result = []
    for channel in ordered_channels:
        result.append(channel.to_dict())

    return(jsonify(result))

def addVideo(information):
    channel_exists = getChannel(information['channel_id'])

    if channel_exists == False:
        return(addChannel({'channel_id' : information['channel_id']}, empty=True))
    else:
        channel_ref = db.collection(u'channels').document(information['channel_id'])
        video_ref = channel_ref.collection('videos').document(information['id'])
        video_ref.set({
            'channel_id' : information['channel_id'],
            'channel' : information['channel'],
            'description' : information['description'],
            'duration' : information['duration'],
            'duration_string' : information['duration_string'],
            'fulltitle' : information['fulltitle'],
            'video_id' : information['id'],
            'like_count' : information['like_count'],
            'view_count' : information['view_count'],
            'original_url' : information['original_url'],
            'thumbnail' : information['thumbnail'],
            'title' : information['title'],
            'upload_date' : information['upload_date'],
            'webpage_url' : information['webpage_url'],
            'downloaded' : False,
            'downloaded_date' : getCurrentTime()
        })
        return(jsonify(information))

def getAllVideosByChannel(channel_id, limit=None):
    channels_ref = db.collection(u'channels').document(channel_id)
    video_ref = channels_ref.collection('videos')
    query = video_ref.order_by('upload_date')

    if limit:
        query = query.limit(limit)

    ordered_videos = query.stream()
    all_videos = []
    for video in ordered_videos:
        all_videos.append(video.to_dict())
    return(all_videos)

def getAllVideos():
    channel_ref = getAllChannels()
    channel_json = json.loads(channel_ref.data)
    all_videos = []
    for channel in channel_json:
        query = getAllVideosByChannel(channel['channel_id'])
        for q in query:
            all_videos.append(q)
    return(jsonify(all_videos))

def getMissingVideos():
    channel_ref = db.collection(u'channels').where('empty', '==', True).stream()
    all_videos = []
    for channel in channel_ref:
        query = getAllVideosByChannel(channel.id)
        for q in query:
            all_videos.append(q)

    return(jsonify(all_videos))