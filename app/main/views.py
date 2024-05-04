import flask
from flask import render_template, redirect, url_for, session
from app.models import User,Product,Role, Permission
from . import main
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required


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
    print(user.role_id)
    if user.confirmed:
        user={'name':user.user_name, 'surname':user.user_surname, 'gender':user.user_gender,'email':user.user_email}
        return render_template("profile.html", user=user, auth=session.get('auth'))
    else:
        return redirect(url_for('auth.unconfirmed'))

@main.route("/admin")
@login_required
@admin_required
def admin_panel():
    return 'Admin Panel'

@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def moderator_panel():
    return 'Moderator Panel'