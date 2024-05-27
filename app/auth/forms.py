from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    name = StringField("Имя:",validators=[DataRequired()])
    surname = StringField("Фамилия:", validators=[DataRequired()])
    gender = SelectField("Пол:", choices=[("0", 'мужской'), ("1", 'женский')],validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    password_check = PasswordField("Повторите пароль:", validators=[DataRequired(),EqualTo('password', message='Wrong password')])
    submit = SubmitField("Зарегистрироваться", validators=[DataRequired()])
    def validate_email(self,field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError("User with this email has already existed")

class LoginForm(FlaskForm):
    email = EmailField("Email:", validators=[DataRequired(), Length(1,64),Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Войти", validators=[DataRequired()])
