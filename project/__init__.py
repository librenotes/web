from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import Config as conf

app = Flask(__name__)
app.config.from_object(conf)

db = SQLAlchemy(app)

from project import controller
