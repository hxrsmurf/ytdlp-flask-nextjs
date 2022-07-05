from .shared import db

class Testing(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    testing = db.Column(db.String(100))

    def __init__(self, testing):
        self.testing = testing