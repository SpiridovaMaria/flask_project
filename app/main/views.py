import flask
from flask import render_template, redirect, url_for, session
from app.models import User,Product,Role
import os.path
from . import main
from .. import mail
from flask_mail import Message
from flask_login import login_required, current_user


@main.route("/")
@main.route("/index")
def index():
    user = {'username':"Maria"}
    return render_template("index.html", user = user,auth=session.get('auth'))


@main.route("/products/<id_product>")
def show_product(id_product):
    product =  Product.query.filter_by(prod_article=id_product).first()
    if product == None:
        flask.abort(404)
    return render_template("show_product.html", product=product)


@main.route("/products/<id_product>/edit")
def edit_product_panel(id_product):
    user = {'username':"Maria", 'user_role':"user"}
    product = "Product "+id_product
    if user['user_role'] == "admin":
        return render_template("edit_product.html", product = product)
    else:
        flask.abort(403)

@main.route('/profile')
@login_required
def showProfile():
    user = current_user
    if user.confirmed:
        user={'name':user.user_name, 'surname':user.user_surname, 'gender':user.user_gender,'email':user.user_email}
        return render_template("profile.html",user = user,auth = session.get('auth'))
    else:
        return redirect(url_for('auth.unconfirmed'))
@main.route("/secret")
@login_required
def secret():
    return "Only for loginned users"
