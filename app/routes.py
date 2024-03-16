import flask
from app import flask_app
from flask import render_template, redirect, url_for, session
from app.forms import *
from models import Role,User,Product

@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {'username':"Maria"}
    return render_template("index.html", user = user,auth = session.get('auth'))
@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@flask_app.route("/products/<id_product>")
def show_product(id_product):
    product =  Product.query.filter_by(prod_article=id_product).first()
    if product == None:
        flask.abort(404)
    return render_template("show_product.html", product=product)

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
    if session.get('auth'):
        user = User.query.filter_by(user_email=session.get('email')).first()
        user={'name':user.user_name, 'surname':user.user_surname, 'gender':user.user_gender,'email':user.user_email}
        return render_template("profile.html",user = user,auth = session.get('auth'))
    else:
        flask.abort(403)

@flask_app.route('/registration',methods=['GET','POST'])
def registrForm():
    if not session.get('auth'):
        text = None
        form = RegistrationForm()
        if form.validate_on_submit():
            session['name'] = form.name.data
            session['surname'] = form.surname.data
            session['gender'] = form.gender.data
            session['email'] = form.email.data
            return redirect(url_for('showProfile'))
        return render_template('formsTemplate.html', form=form)
    else:
        return redirect(url_for('showProfile'))


@flask_app.route('/login',methods=['GET','POST'])
def loginForm():
    if not session.get('auth'):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(user_email=form.email.data).first()
            if user is not None:
                session['email'] = form.email.data
                session['auth'] = True
            else:
                session['auth'] = False
            return redirect(url_for('showProfile'))
        return render_template('loginForm.html', form=form)
    else:
        return redirect(url_for('showProfile'))

@flask_app.route('/logout')
def logout():
    if session.get('auth'):
        session['auth'] = False
    return redirect(url_for('index'))