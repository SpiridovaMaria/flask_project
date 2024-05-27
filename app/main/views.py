import flask
from flask import render_template, redirect, url_for, session, flash
from flask_admin.contrib.sqla import ModelView

from app.models import *
from . import main
from flask_login import login_required, current_user

from .forms import *
from .. import db, models, admin
from ..decorators import admin_required, permission_required

"""
    Adding views for admin panel
"""
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Size_in_stock, db.session))
admin.add_view(ModelView(Basket, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))


@main.route("/")
@main.route("/index")
def index():
    """
        function for main page
        it gets list of products that should be in carousel and in sale section and list of categories from models
        :return template of main page
    """
    product_carousel = db.session.query(Product, Category).filter(Product.in_carousel).filter(Product.cat_id == Category.id).all()
    best_products = db.session.query(Product, Category).filter(Product.sale).filter(Product.cat_id == Category.id).all()
    categories = Category.query.all()
    return render_template("index.html", auth=session.get('auth'), product_carousel=product_carousel,
                           best_products=best_products, categories=categories)


@main.route("/products/<id_product>", methods=['GET', 'POST'])
def show_product(id_product):
    """
        Function showing all information of one product and adding it to the shopping basket
        :param id_product: article of product that will be shown
        :return if product doesn't exist - 404 error, if the button 'В корзину' is pushed - redirect to main.add_product_to_basket()
        else - template of all information of the product
    """
    product = db.session.query(Product, Category).filter(Product.cat_id == Category.id, Product.prod_article == id_product).first()
    if product == None:
        flask.abort(404)
    available_size = Size_in_stock.query.filter_by(prod_id=id_product).all()
    sizes = [(i.id, i.size) for i in available_size]
    form = AddToBasketForm()
    form.size.choices = sizes
    if form.validate_on_submit():
        id_size = form.size.data
        return redirect(url_for("main.add_product_to_basket", id_product=id_product, id_size=id_size))
    return render_template("show_product.html", product=product, size=available_size, form=form)

@main.route("/products/category/<id_category>")
def show_all_products(id_category):
    """
           Function showing a list of all products of one category
           :param id_category: the id of the category of all products
           :return if category doesn't exist - 404 error, if id_category == 6 - render template with products of all categories,
           else - template of all products of one category
    """
    if id_category == '6':
        products = Product.query.all()
        category = Category.query.all()
    else:
        products = Product.query.filter_by(cat_id=id_category).all()
        category = Category.query.filter_by(id=id_category).all()
    if len(products)==0:
        return flask.abort(404)
    return render_template("show_products.html", products=products, category=category)


@main.route('/profile')
@login_required
def showProfile():
    """
           Function showing profile of user and user's basket
           :return if current user haven't confirmed his email - redirect to auth.unconfirmed,
           else - template of all information of user and his basket
    """
    user = current_user
    if user.confirmed:
        user = {'name': user.user_name, 'surname': user.user_surname, 'gender': user.user_gender, 'email': user.user_email, 'role':user.role_id}
        products = db.session.query(Basket, Product, Category, Size_in_stock).filter(Product.prod_article == Basket.prod_id).filter(Product.cat_id == Category.id).filter(Size_in_stock.id == Basket.size).all()
        total = 0
        orders = db.session.query(Order, Product, Size_in_stock,Category,Department).filter(Order.user_id == current_user.user_id).\
            filter(Order.size == Size_in_stock.id).filter(Order.prod_id == Product.prod_article).filter(Product.cat_id == Category.id).\
            filter(Order.address == Department.id).all()
        for i in products:
            total += i.Product.prod_price*i.Basket.quantity
        return render_template("profile.html", user=user, auth=session.get('auth'), basket=products, total=total, orders=orders)
    else:
        return redirect(url_for('auth.unconfirmed'))

@main.route("/products/<id_product>/<id_size>")
@login_required
def add_product_to_basket(id_product, id_size):
    """
        Function for adding a product to shopping basket
        :param id_product: id of the product that is wanted to be added to basket
        :param id_size: the chosen size of the product
        :return if current user haven't confirmed his email - redirect to auth.unconfirmed, if product with this id and size is already
        in the basket - it increases quantity and redirects to showProfile(), elseif the product with this id and size exists -
        it is added to the basket, else - 404 error
    """
    user = current_user
    if user.confirmed:
        existed = Basket.query.filter_by(user_id=user.user_id, prod_id=id_product, size=id_size).first()
        if existed:
            if existed.add_product(id_product):
                db.session.commit()
                return redirect(url_for('main.showProfile'))
            else:
                flash('Ваша ссылка не валидна или истекла!')
        else:
            product = Size_in_stock.query.filter_by(prod_id=id_product, id=id_size)
            if product:
                prod = Basket(user_id=user.user_id, prod_id=id_product, quantity=1, size=id_size)
                db.session.add(prod)
                db.session.commit()
                return redirect(url_for('main.showProfile'))
            else:
                return flask.abort(404)
    else:
        return redirect(url_for('auth.unconfirmed'))

@main.route("/products/<id_product>/<id_size>/<quantity>/>removefrombasket")
@login_required
def delete_product_from_basket(id_product, id_size, quantity):
    """
            Function for deleting product from basket
            :param id_product: id of the product that is wanted to be deleted from basket
            :param id_size: the chosen size of the product
            :param quantity: number of products that should be deleted
            :return if current user haven't confirmed his email - redirect to auth.unconfirmed, if product with this id and size doesn't exist
            in the basket - 404 error, elseif the quantity == "all" - it deletes this product from the basket and redirects to showProfile()
            else - it decreases the quantity
        """
    user = current_user
    if user.confirmed:
        existed = Basket.query.filter_by(user_id=user.user_id, prod_id=id_product, size=id_size).first()
        if existed:
            if quantity == '1':
                if existed.remove_product(id_product):
                    db.session.commit()
            if quantity == "all" or existed.quantity <= 0:
                Basket.query.filter_by(user_id=user.user_id, prod_id=id_product, size=id_size).delete()
                db.session.commit()
            return redirect(url_for('main.showProfile'))
        else:
            return flask.abort(404)

@main.route("/buy/<id_product>/<id_basket>", methods=['GET', 'POST'])
@login_required
def order_product(id_product, id_basket):
    """
        Function for ordering the product
        :param id_product: id of the product that is wanted to be ordered
        :param id_basket: id of this product in the basket
        :return if current user haven't confirmed his email - redirect to auth.unconfirmed, if the product doesn't exist
        in the basket - 404 error, elseif form of order is submitted - redirect to register_order(), else - template of making order
    """
    user = current_user
    if user.confirmed:
        existed = db.session.query(Basket, Size_in_stock).filter(Basket.id == id_basket).filter(Basket.size == Size_in_stock.id).first()
        if existed:
            product = db.session.query(Product, Category).filter(Product.prod_article == id_product).filter(Product.cat_id == Category.id).first()
            departments = [(i.id, i.address) for i in Department.query.all()]
            form = OrderProductForm()
            form.department_address.choices = departments
            if form.validate_on_submit():
                id_address = form.department_address.data
                return redirect(url_for("main.register_order", id_product=id_product, id_address=id_address, id_basket=existed.Basket.id))
            return render_template('order.html', basket=existed, product=product, form=form)
        else:
            return flask.abort(404)

@main.route("/order/<id_product>/<id_address>/<id_basket>")
@login_required
def register_order(id_product, id_address, id_basket):
    """
        Function for adding order to model Order
        :param id_product: id of the product that is wanted to be ordered
        :param id_address: the chosen address of the department
        :param id_basket: id of this product in the basket
        :return if current user haven't confirmed his email - redirect to auth.unconfirmed, if product exists and is in
        the basket - added to model Order and redirect to delete_product_from_basket(), else - 403 error
    """
    user = current_user
    if user.confirmed:
            product = Product.query.filter_by(prod_article=id_product).first()
            basket = db.session.query(Basket, Size_in_stock).filter(Basket.id == id_basket).filter(Basket.size == Size_in_stock.id).first()
            if product and basket:
                order = Order(user_id=user.user_id, prod_id=id_product, size=basket.Size_in_stock.id,
                              quantity=basket.Basket.quantity, total_price=basket.Basket.quantity * product.prod_price, address=id_address)
                db.session.add(order)
                db.session.commit()
                return redirect(url_for('main.delete_product_from_basket',id_product=product.prod_article, id_size=basket.Size_in_stock.id, quantity='all'))
            else:
                return flask.abort(403)


@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def moderator_panel():
    return 'Moderator Panel'