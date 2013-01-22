from flask import request
from flask.templating import render_template
from flask.helpers import jsonify
from flask.wrappers import Response
from redis import Redis
import json
from fodder.app import app
from fodder import models, auth
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


class UserView(MethodView):

    def _cookie_response(self, user=None):
        #FIXME not very restful

        resp = jsonify(success=True)
        if user:
            resp.set_cookie('session_key', user.session_key)
        else:
            resp.delete_cookie('session_key')
        return resp

    def put(self):
        """ Creates a new user of the given username. """

        username = request.form['username']
        email = request.form['email']
        pass1 = request.form['password1']
        pass2 = request.form['password2']

        print "hola"

        #TODO check email format
        #TODO check username not exists
        #TODO check pass1 == pass2

        user = models.User(username=username, email=email)
        user.set_password(pass1)
        user.authenticate(pass1)
        user.save()

        return self._cookie_response(user)

    def post(self):
        """ Logs the user in. """

        password = request.form['password']
        username = request.form['username']
        user = auth.login(username, password)

        if user:
            return self._cookie_response(user)
        else:
            #return error
            pass

    def delete(self):
        """ Logs the user out. """

        auth.logout()
        return self._cookie_response()

app.add_url_rule('/users/', view_func=UserView.as_view('users'),
                 methods=['PUT', 'POST', 'DELETE'])


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
