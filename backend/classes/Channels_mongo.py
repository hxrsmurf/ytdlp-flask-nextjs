from .shared import mongo_db

class Channels(mongo_db.Document):
    channel_id = mongo_db.StringField(primary_key = True)
    channel_name = mongo_db.StringField()
    channel_name_lowercase = mongo_db.StringField()
    channel_follower_count = mongo_db.IntField()
    description = mongo_db.StringField()
    original_url = mongo_db.StringField()
    uploader = mongo_db.StringField()
    uploader_id = mongo_db.StringField()
    webpage_url = mongo_db.StringField()
    picture_profile = mongo_db.StringField()
    picture_cover = mongo_db.StringField()
    last_updated = mongo_db.StringField()
    latest_upload = mongo_db.StringField()