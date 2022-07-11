from flask import Blueprint, jsonify

from classes.shared import mongo_db
from classes import Channels_mongo

mongo_bp = Blueprint('mongo', __name__, url_prefix='/mongo')

@mongo_bp.route('/', methods=['GET'])
def root():
    user = Channels_mongo.User.objects()
    #user.save()
    t = []
    for u in user:
        t.append({
            'name' : u['name']
        })

    return(jsonify(t))