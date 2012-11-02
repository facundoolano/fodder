from flask.templating import render_template
from fodder.app import app


@app.route('/')
def home():
    return render_template('base.html')


def get_entries():
    #TODO
    pass


def post_entry():
    #TODO
    pass
