from fodder.models import User, Entry, Comment
from fodder.app import app
from fodder.routes import *

if __name__ == '__main__':
    User.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
    Comment.create_table(fail_silently=True)

#    app.run(threaded=True)
