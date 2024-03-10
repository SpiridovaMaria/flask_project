import flask
from app import flask_app
from flask import render_template, redirect, url_for, session
from app.forms import SimpleForm

class Product:
    def __init__(self,id_product, name):
        self.id_product = id_product
        self.name = name

def load_product(id_product):
    if int(id_product)<=10 and int(id_product)>0:
        name = "Товар "+id_product
        return Product(int(id_product), name)

@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {'username':"Maria"}
    return render_template("index.html", user = user)
@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@flask_app.route("/products/<id_product>")
def show_product(id_product):
    product = load_product(id_product)
    if product == None:
        flask.abort(404)
    return '<h1 style ="color: green; text-align:center">Самый лучший {} у нас!'.format(product.name)

@flask_app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"),403

@flask_app.route("/products/<id_product>/edit")
def edit_product_panel(id_product):
    user = {'username':"Maria", 'user_role':"user"}
    product = "Product "+id_product
    if user['user_role'] == "admin":
        return render_template("edit_product.html", product = product)
    else:
        flask.abort(403)

@flask_app.route('/profile')
def showProfile():
    user={'name':session.get('name'), 'surname':session.get('surname'), 'gender': session.get('gender'),'email':session.get('email')}
    return render_template("profile.html",user = user)

@flask_app.route('/registration',methods=['GET','POST'])
def registrForm():
    text = None
    form = SimpleForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['surname']=form.surname.data
        session['gender'] = form.gender.data
        session['email'] = form.email.data
        return redirect(url_for('showProfile'))
    return render_template('formsTemplate.html', form=form)
