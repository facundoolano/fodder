from flask import Flask
from flask_peewee.db import Database

app = Flask(__name__)
app.config.from_object('fodder.settings')
db = Database(app)

if __name__ == '__main__':
    app.run()
