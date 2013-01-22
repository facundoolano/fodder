import datetime

from flask_peewee.auth import BaseUser, Auth
from flask_peewee.db import Database
from peewee import *

from fodder.app import app
import md5

db = Database(app)
auth = Auth(app, db)


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)
    session_key = CharField(null=True)

    def set_password(self, password):
        self.password = md5.md5(password).hexdigest()

    def authenticate(self, password):
        """
        If the password is valid, cretes a new session key and returns True.
        Otherwise returns False.
        """

        if md5.md5(password).hexdigest() == self.password:
            self.session_key = md5.md5(self.username + password +
                                   str(datetime.datetime.now())).hexdigest()
            self.save()
            return True
        else:
            return False

    def gravatar_url(self, size=40):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5.md5(self.email.strip().lower().encode('utf-8')).hexdigest(),
             size)


class Entry(db.Model):
    content = TextField()
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)

    def vote_count(self):
        #TODO
        return 0

    def comment_count(self):
        #TODO
        return 0

    def as_dict(self):
        return {'username': self.user.username,
                'content': self.content,
                'avatar': self.user.gravatar_url(),
                'date': self.creation_date.isoformat(),
                'votes': self.vote_count(),
                'comments': self.comment_count()}


#TODO put some other place?
def get_entries(limit, offset=0):
    return Entry.select().order_by(Entry.creation_date.desc())\
        .limit(limit).offset(offset)


def get_comments(entry_id):
    return Comment.select().join(Entry).where(Entry.id == entry_id)\
        .order_by(Comment.creation_date.desc())


class Comment(db.Model):
    entry = ForeignKeyField(Entry)
    user = ForeignKeyField(User)
    content = TextField()
    creation_date = DateTimeField(default=datetime.datetime.now)

    def as_dict(self):
        return {'username': self.user.username,
            'content': self.content,
            'avatar': self.user.gravatar_url(),
            'date': self.creation_date.isoformat()}


class Vote(db.Model):
    entry = ForeignKeyField(Entry)
    user = ForeignKeyField(User)
    creation_date = DateTimeField(default=datetime.datetime.now)
