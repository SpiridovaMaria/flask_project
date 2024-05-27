from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class AddToBasketForm(FlaskForm):
    size = SelectField("Размер:", coerce=int, validators=[DataRequired()])
    submit = SubmitField('В корзину')

class OrderProductForm(FlaskForm):
    department_address = SelectField("Выберите магазин для получения:", render_kw={'style':'outline: none;box-shadow: none;'}, validators=[DataRequired()])
    submit = SubmitField('Заказать', render_kw={'class':'btn-dark'})