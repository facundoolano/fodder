from flask import request
from flask.templating import render_template
from fodder.app import app
from fodder.models import Entry, User
from flask.helpers import jsonify
from flask.wrappers import Response
from redis import Redis
import json
from fodder import models

red = Redis()


#TODO this might belong somewhere else
def entry_as_dict(entry):
    return {'username': entry.user.username,
            'content': entry.content,
            'avatar': entry.user.gravatar_url(),
            'date': entry.creation_date.isoformat()}


@app.route('/')
def home():
    #FIXME remove flask templates all together, return regular static file
    return render_template('base.html')


@app.route('/entries')
def get_entries():
    entries = []

    #TODO think of a more general pagination approach
    paginate_by = 5
    page = int(request.args.get('page', 1))
    offset = page * paginate_by

    for entry in models.get_entries(limit=paginate_by, offset=offset):
        entries.append(entry_as_dict(entry))

    return jsonify(success=True, entries=entries)


@app.route('/new_entry', methods=['POST'])
def post_entry():

    #FIXME get from request
    user = User.get_or_create(username='Facundo', email='facundo@fodder.com')
    user.set_password('pepe')
    user.save()

    entry = Entry.create(content=request.form['entry'], user=user)
    entry.save()

    #publish the entry to the channel
    message = json.dumps(entry_as_dict(entry))
    red.publish('entry', message)

    return jsonify(success=True)


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('entry')
    for message in pubsub.listen():
        print message
        if message['type'] == 'message':
            yield 'data: %s\n\n' % message['data']


@app.route('/entry_stream')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')
