from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import ShoppingListForm, LoginForm
from app.models import User, ShoppingList
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    shop_name = {'shop_name': 'M&S'}
    purchase_date = {'purchase_date': '11-06-2022'}
    shopping_list = [
        {
            'item': 'bananas',
            'price': '2.20'
        },
        {
            'item': 'milk',
            'price': '1.10'
        }
    ]
    return render_template('index.html',
                           shop=shop_name,
                           shopping_list=shopping_list,
                           purchase_date=purchase_date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))