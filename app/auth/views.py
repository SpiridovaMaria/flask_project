import flask
from flask import render_template, request, url_for, redirect, flash
from . import auth
from app.auth.forms import *
from ..models import *
from flask_login import login_user, login_required, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for("main.showProfile"))

        flash('Вы ввели неправильный пароль.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        gen = int(form.gender.data)
        if gen==0:
            gen = False
        else:
            gen = True
        user = User(user_name=form.name.data, user_surname=form.surname.data, user_gender=gen, user_email=form.email.data)
        db.session.add(user)
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
