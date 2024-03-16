import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = "hard to unlock"
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/my_shop'
flask_app.config['SQLALCHEMY-TRACK-MODIFICATIONS'] = False


bootstrap = Bootstrap5(flask_app)
db = SQLAlchemy(flask_app)

from app import routes
from models import *
migrate=Migrate(flask_app,db)