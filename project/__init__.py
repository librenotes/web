from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config as conf
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object(conf)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = SQLAlchemy(app)

from project import controller
