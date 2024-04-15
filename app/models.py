from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

from . import db
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User',backref = 'role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_surname = db.Column(db.String(50))
    user_name = db.Column(db.String(50), index=True)
    user_gender = db.Column(db.Boolean)
    user_email = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('Password not enable to read')
    def set_password(self,password):
        self.password_hash = generate_password_hash(password,method="pbkdf2:sha256")
    def password_verify(self,password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User %r>' % self.user_name
    def get_id(self):
        return (self.user_id)

class Product(db.Model):
    __tablename__ = 'products'
    prod_article = db.Column(db.String(50), primary_key=True)
    prod_name = db.Column(db.String(100))
    prod_category = db.Column(db.String(100))
    prod_description = db.Column(db.String(200))
    in_stock = db.Column(db.Boolean)
    prod_price = db.Column(db.Float)
    def __repr__(self):
        return '<Product %r>' % self.prod_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

