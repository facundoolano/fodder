from flask import request
from flask.templating import render_template
from fodder.app import app
from fodder.models import Entry, User
from flask.helpers import jsonify


@app.route('/')
def home():
    #FIXME remove flask templates all together, return regular static file
    return render_template('base.html')


@app.route('/entries')
def get_entries():
    entries = []
    for entry in Entry.select().order_by(Entry.creation_date.desc()):
        entries.append({'username': entry.user.username,
                        'content': entry.content})

    return jsonify(success=True, entries=entries)


@app.route('/new_entry', methods=['GET', 'POST'])
def post_entry():

    #FIXME get from request
    user = User.get_or_create(username='Facundo', email='facundo@fodder.com')
    user.set_password('pepe')
    user.save()

    if 'entry' in request.form:
        Entry.create(content=request.form['entry'], user=user).save()
        return jsonify(success=True)
    else:
        return jsonify(success=False), 500
