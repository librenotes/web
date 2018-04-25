from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config as conf
from flask_cache import Cache
from flask_login import LoginManager
from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object(conf)
pagedown = PageDown(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
login_manager.init_app(app=app)
db = SQLAlchemy(app)

from project import controller
