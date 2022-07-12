from sqlalchemy import collate, desc
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

db = SQLAlchemy()

mongo_db = MongoEngine()