from .shared import mongo_db

class User(mongo_db.Document):
    name = mongo_db.StringField()
    email = mongo_db.StringField()

    def to_json(self):
        return {'name' : self.name, 'email' : self.email}