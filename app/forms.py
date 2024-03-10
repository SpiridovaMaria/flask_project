from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, email, EqualTo


class SimpleForm(FlaskForm):
    name = StringField("Имя:",validators=[DataRequired()])
    surname = StringField("Фамилия:", validators=[DataRequired()])
    gender = SelectField("Пол:", choices=[('m','мужской'),('f','женский')],validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired(),validators.Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    password_check = PasswordField("Повторите пароль:", validators=[DataRequired(),EqualTo('password', message='Wrong password')])
    submit = SubmitField("Зарегистрироваться", validators=[DataRequired()])