from flask import request
from flask.templating import render_template
from flask.helpers import jsonify
from flask.wrappers import Response
from redis import Redis
import json
from fodder.app import app
from fodder import models
from flask.views import MethodView

red = Redis()


def get_user():
    #FIXME get from request
    user = models.User.get_or_create(username='Facundo',
                                     email='facundo@fodder.com')
    user.set_password('pepe')
    user.save()

    return user


@app.route('/')
def home():
    #FIXME remove flask templates all together, return regular static file
    return render_template('base.html')


class EntryView(MethodView):
    def get(self):

        #TODO think of a more general pagination approach
        paginate_by = 5
        page = int(request.args.get('page', 1))
        offset = page * paginate_by

        entries = [e.as_dict() for e in
                   models.get_entries(limit=paginate_by, offset=offset)]

        return jsonify(success=True, entries=entries)

    def post(self):

        user = get_user()

        entry = models.Entry.create(content=request.form['entry'], user=user)
        entry.save()

        #publish the entry to the channel
        message = json.dumps(entry.as_dict())
        red.publish('entry', message)

        return jsonify(success=True)

app.add_url_rule('/entries/', view_func=EntryView.as_view('entries'))


class CommentView(MethodView):

    def get(self, entry_id):
        comments = [c.as_dict() for c in
                    models.get_comments(entry_id)]

        return jsonify(success=True, comments=comments)

    def post(self, entry_id):

        entry = models.Entry.get(models.Entry.id == entry_id)
        comment = models.Comment(entry=entry, content=request.form['entry'],
                                 user=user)
        comment.save()

        #publish to some channel
        message = json.dumps(entry.as_dict())
        red.publish('entry_' + str(entry.id), message)


app.add_url_rule('/entries/<int:entry_id>/comments/',
                 view_func=CommentView.as_view('comments'))


@app.route('/entries/<int:entry_id>/votes/', methods=['POST'])
def vote(entry_id):
    #TODO
    pass


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('entry')
    for message in pubsub.listen():
        print message
        if message['type'] == 'message':
            yield 'data: %s\n\n' % message['data']


@app.route('/entry_stream')
def sse_request():
    #TODO authenticate and different channels
    return Response(
            event_stream(),
            mimetype='text/event-stream')
