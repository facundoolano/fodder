import datetime

from flask_peewee.auth import BaseUser, Auth
from flask_peewee.db import Database
from peewee import *

from fodder.app import app
from md5 import md5

db = Database(app)
auth = Auth(app, db)


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def gravatar_url(self, size=40):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)


class Entry(db.Model):
    content = TextField()
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)


#TODO put some other place?
def get_entries(limit, offset=0):
    return Entry.select().order_by(Entry.creation_date.desc())\
        .limit(limit).offset(offset)


class Comment(db.Model):
    entry = ForeignKeyField(Entry)
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)
