from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from authlib.jose import JsonWebSignature

from . import db

class Permission:
    ADD_TO_BASKET = 1
    BUY = 2
    REVIEW = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy="dynamic")
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'Consumer': [Permission.ADD_TO_BASKET, Permission.BUY, Permission.REVIEW],
            'Moderator': [Permission.ADD_TO_BASKET, Permission.BUY, Permission.REVIEW, Permission.MODERATE],
            'Admin': [Permission.ADD_TO_BASKET, Permission.BUY, Permission.REVIEW, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'Consumer'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_surname = db.Column(db.String(50))
    user_name = db.Column(db.String(50), index=True)
    user_gender = db.Column(db.Boolean)
    user_email = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.user_email=="spiridonovaemailforhomework@gmail.com":
                self.role = Role.query.filter_by(name="Admin").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.user_id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self,token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.user_id):
            print("it's not your token")
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    @property
    def password(self):
        raise AttributeError('Password not enable to read')

    @password.setter
    def set_password(self,password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def password_verify(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def get_id(self):
        return (self.user_id)


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_admin(self):
        return False


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), unique=True)
    prod = db.relationship('Product', backref='cat', lazy="dynamic")
    cat_photo = db.Column(db.String(1000))


class Product(db.Model):
    __tablename__ = 'products'
    prod_article = db.Column(db.String(50), primary_key=True)
    prod_name = db.Column(db.String(100))
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    prod_description = db.Column(db.Text)
    in_stock = db.Column(db.Boolean)
    prod_old_price = db.Column(db.Numeric)
    prod_price = db.Column(db.Numeric)
    prod_color = db.Column(db.String(100))
    prod_material = db.Column(db.String(200))
    prod_country = db.Column(db.String(100))
    prod_photo = db.Column(db.String(1000))
    in_carousel = db.Column(db.Boolean)
    sale = db.Column(db.Boolean)
    sizes = db.relationship('Size_in_stock', backref='sizes', lazy="dynamic")
    baskets = db.relationship('Basket', backref='in_basket', lazy="dynamic")

class Basket(db.Model):
    __tablename__ = 'baskets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    prod_id = db.Column(db.String(50), db.ForeignKey('products.prod_article'))
    quantity = db.Column(db.Integer)
    size = db.Column(db.Integer, db.ForeignKey('sizes_in_stock.id'))


    def __repr__(self):
        return '<Basket %r>' % self.user_id + self.prod_id

    def add_product(self, id_product):
        self.quantity += 1
        db.session.add(self)
        return True

    def remove_product(self, id_product):
        self.quantity -= 1
        db.session.add(self)
        return True


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    prod_id = db.Column(db.String(50), db.ForeignKey('products.prod_article'))
    size = db.Column(db.Integer, db.ForeignKey('sizes_in_stock.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Numeric)
    address = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __repr__(self):
        return '<Order %r>' % self.id

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(1000))

    def __repr__(self):
        return '<Department %r>' % self.address

class Size_in_stock(db.Model):
    __tablename__ = 'sizes_in_stock'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.String(50), db.ForeignKey('products.prod_article'))
    size = db.Column(db.Numeric)


    def __repr__(self):
        return '<Size_in_stock %r>' % self.size


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser
