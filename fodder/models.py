import datetime

from flask_peewee.auth import BaseUser, Auth
from flask_peewee.db import Database
from peewee import *

from fodder.app import app

db = Database(app)
auth = Auth(app, db)


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)


class Entry(db.Model):
    content = TextField()
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)


class Comment(db.Model):
    entry = ForeignKeyField(Entry)
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)
