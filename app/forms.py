from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, SubmitField, FloatField, \
    BooleanField, PasswordField, FieldList, FormField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class ShoppingListEntry(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])


class ShoppingListForm(FlaskForm):
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    shop_name = StringField('Shop Name', validators=[DataRequired()])
    items = FieldList(FormField(ShoppingListEntry), min_entries=1)
    submit = SubmitField('Correct')