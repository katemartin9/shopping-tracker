from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, FloatField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class ShoppingListForm(FlaskForm):
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Correct')