from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from config import config

bootstrap = Bootstrap5()
db = SQLAlchemy()
mail = Mail()

def create_app(config_name="default"):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])
    config[config_name].init_app(flask_app)
    bootstrap.init_app(flask_app)
    mail.init_app(flask_app)
    db.init_app(flask_app)

    from .main import main as main_blueprint
    flask_app.register_blueprint(main_blueprint)

    return flask_app

