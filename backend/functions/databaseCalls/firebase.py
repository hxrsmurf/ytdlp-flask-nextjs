import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import jsonify

from functions.utils import getCurrentTime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def addChannel(information):
    channels_ref = db.collection(u'channels').document(information['channel_id'])
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
    return(jsonify(information))

def getChannel(information):
    channels_ref = db.collection(u'channels').document(information)

    doc = channels_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        return(jsonify(doc.to_dict()))
    else:
        print(u'No such document!')
        return('No such document!')

def getAllChannels():
    channels_ref = db.collection(u'channels')
    query = channels_ref.order_by('channel_name')
    ordered_channels = query.stream()
    result = []
    for channel in ordered_channels:
        result.append(channel.to_dict())

    return(jsonify(result))