from flask import Flask
from flask_bootstrap import Bootstrap5

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = "hard to unlock"
bootstrap = Bootstrap5(flask_app)

from app import routes