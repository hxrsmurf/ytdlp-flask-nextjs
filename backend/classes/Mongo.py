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
    cdn_photo_cover = mongo_db.StringField()
    last_updated = mongo_db.StringField()
    latest_upload = mongo_db.StringField()
    cdn_photo_cover = mongo_db.StringField()

class Videos(mongo_db.Document):
    channel_name = mongo_db.StringField()
    channel_name_lowercase = mongo_db.StringField()
    channel_id = mongo_db.StringField()
    description = mongo_db.StringField()
    duration = mongo_db.IntField()
    duration_string = mongo_db.StringField()
    fulltitle = mongo_db.StringField()
    video_id = mongo_db.StringField(primary_key = True)
    like_count = mongo_db.IntField()
    view_count = mongo_db.IntField()
    original_url = mongo_db.StringField()
    thumbnail = mongo_db.StringField()
    title = mongo_db.StringField()
    upload_date = mongo_db.StringField()
    webpage_url = mongo_db.StringField()
    cdn_video = mongo_db.StringField()
    cdn_video_hls = mongo_db.StringField()
    watched = mongo_db.BooleanField()
    cdn_video_thumbnail = mongo_db.StringField()

class DownloadQueue(mongo_db.Document):
    video_id = mongo_db.StringField()
    webpage_url = mongo_db.StringField()
    downloaded = mongo_db.BooleanField()
    duration = mongo_db.IntField()