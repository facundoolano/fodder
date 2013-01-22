from fodder.models import User, Entry, Comment, Vote
from fodder.app import app
from fodder.views import *


#gunicorn -w 4 fodder.main:app -b 127.0.0.1:4000

if __name__ == '__main__':
    User.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
    Comment.create_table(fail_silently=True)
    Vote.create_table(fail_silently=True)

    app.run(use_reloader=False)
