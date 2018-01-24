import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class News(db.Document):
    title = db.StringField(required=True, max_length=200)
    content = db.StringField(required=True)
    author = db.StringField(required=True, max_length=50)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    published_at = db.DateTimeField()
    news_type = db.StringField(default="politics")
    tags = db.ListField(db.StringField(max_length=50))
