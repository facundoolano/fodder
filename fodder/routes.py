from flask import request
from flask.templating import render_template
from fodder.app import app
from fodder.models import Entry, User
import json
from flask.helpers import jsonify


@app.route('/')
def home():
    return render_template('base.html')


def get_entries():
    #TODO
    pass


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
