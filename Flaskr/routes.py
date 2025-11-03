from flask import Blueprint, request, redirect, url_for, render_template, session
from .db import db, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print("Session:", session)
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        print("User:", user)
        return render_template('index.html', username=user.username)
    return render_template('index.html', username=None)


@main.route('/product/')
@main.route('/product/<productId>')
def product(productId=None):
    return render_template('product.html', product=productId)

@main.route('/database/')
def database(productId=None):
    users = User.query.all()
    print(users)
    return {"users": [u.username for u in users]}
