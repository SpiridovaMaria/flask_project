import flask
from flask import render_template, request, url_for, redirect, flash
from . import auth
from app.auth.forms import *
from ..models import *
from flask_login import login_user, login_required, logout_user, current_user
from app import mail
from flask_mail import Message
from threading import Thread

@auth.before_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint!='auth'\
            and request.endpoint!='static':
        return redirect(url_for('auth.unconfirmed'))
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user, form.remember_me.data)
            if not user.confirmed:
                return redirect(url_for("auth.unconfirmed"))
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
        user.set_password = form.password.data
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html", form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.showProfile'))
    if current_user.confirm(token):
        db.session.commit()
        return redirect(url_for('main.showProfile'))
    else:
        flash('Ваша ссылка не валидна или истекла!')
    return redirect(url_for('main.index'))
def send_confirm(user,token):
    send_mail(user.user_email, "Confirm your account", "auth/confirm", user=user, token=token.decode('utf-8'))
    redirect(url_for("main.index"))
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  sender='spiridonovaemailforhomework@gmail.com',
                  recipients=[to])
    try:
        msg.html = render_template(template + ".html", **kwargs)
    except:
        msg.body = render_template(template + ".txt", **kwargs)
    from app_file import flask_app
    thread = Thread(target=send_asyns_email,args=[flask_app,msg])
    thread.start()
    return thread

def send_asyns_email(app,msg):
    with app.app_context():
        mail.send(msg)
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous:
        return redirect(url_for('main.index'))
    elif current_user.confirmed:
        return redirect(url_for('main.showProfile'))
    else:
        return render_template("auth/unconfirmed.html")



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



