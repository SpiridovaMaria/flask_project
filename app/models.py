from . import db
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User',backref = 'role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_surname = db.Column(db.String(50))
    user_name = db.Column(db.String(50), index=True)
    user_gender = db.Column(db.Boolean)
    user_email = db.Column(db.String(50),unique = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.user_name

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