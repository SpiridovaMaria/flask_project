from flask_admin import Admin, AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_bootstrap import Bootstrap5
from flask_mail import Mail

from config import config
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

bootstrap = Bootstrap5()
db = SQLAlchemy()
mail = Mail()
oauth = OAuth()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view='auth.login'
class CustomAdminIndexView(AdminIndexView):
   def is_accessible(self):
    return current_user.is_authenticated and current_user.role_id == 3

admin = Admin(name="My Shop", index_view = CustomAdminIndexView())

def create_app(config_name="default"):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])
    config[config_name].init_app(flask_app)
    login_manager.init_app(flask_app)
    bootstrap.init_app(flask_app)
    mail.init_app(flask_app)
    db.init_app(flask_app)
    migrate.init_app(flask_app,db)
    oauth.init_app(flask_app)
    admin.init_app(flask_app)


    from .main import main as main_blueprint
    flask_app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return flask_app

