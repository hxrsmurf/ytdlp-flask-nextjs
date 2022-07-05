from .shared import db

class Channel(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    channel = db.Column(db.String(100))
    channel_follower_count = db.Column(db.Integer)
    channel_id = db.Column(db.String(100))
    description = db.Column(db.String(100))
    original_url = db.Column(db.String(100))
    uploader = db.Column(db.String(100))
    uploader_id = db.Column(db.String(100))
    webpage_url = db.Column(db.String(100))
    picture_profile = db.Column(db.String(100))
    picture_cover = db.Column(db.String(100))
    last_updated = db.Column(db.String(100))
    latest_upload = db.Column(db.String(100))

    def __init__(self, channel, channel_follower_count, channel_id, description, original_url, uploader, uploader_id, webpage_url, picture_profile, picture_cover, last_updated, latest_upload):
        self.channel = channel
        self.channel_follower_count = channel_follower_count
        self.channel_id = channel_id
        self.description = description
        self.original_url = original_url
        self.uploader = uploader
        self.uploader_id = uploader_id
        self.webpage_url = webpage_url
        self.picture_profile = picture_profile
        self.picture_cover = picture_cover
        self.last_updated = last_updated
        self.latest_upload = latest_upload