from .shared import db

class Videos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    channel = db.Column(db.String(100))
    channel_id = db.Column(db.String(100))
    description = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    duration_string = db.Column(db.String(100))
    fulltitle = db.Column(db.String(100))
    video_id = db.Column(db.String(100))
    like_count = db.Column(db.String(100))
    view_count = db.Column(db.String(100))
    original_url = db.Column(db.String(100))
    thumbnail = db.Column(db.String(100))
    title = db.Column(db.String(100))
    upload_date = db.Column(db.String(100))
    webpage_url = db.Column(db.String(100))
    downloaded = db.Column(db.Boolean)
    downloaded_date = db.Column(db.String(100))

    def __init__(self, channel, channel_id, description, duration, duration_string, fulltitle, video_id, like_count, view_count, original_url, thumbnail, title, upload_date, webpage_url, downloaded, downloaded_date):
        self.channel = channel
        self.channel_id = channel_id
        self.description = description
        self.duration = duration
        self.duration_string = duration_string
        self.fulltitle = fulltitle
        self.video_id = video_id
        self.like_count = like_count
        self.view_count = view_count
        self.original_url = original_url
        self.thumbnail = thumbnail
        self.title = title
        self.upload_date = upload_date
        self.webpage_url = webpage_url
        self.downloaded = downloaded
        self.downloaded_date = downloaded_date