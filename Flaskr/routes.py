from flask import Blueprint, request, redirect, url_for, render_template, session
from .db import db, User, Products

main = Blueprint('main', __name__)

@main.route('/')
def index(productId=None):
    products = Products.query.all()
    # print(products)
    # return {"products": [p.productname for p in products]}
    # print("Session:", session)
    if products is not None:
        return render_template('index.html', products=products)
    # if 'id' in session:
    #     user = User.query.get(session['id'])
    #     print("User:", user)
    #     return render_template('index.html', username=user.username)
    return render_template('index.html', products=None)
    



# @main.route('/product/')
# @main.route('/product/<productId>')
# def product(productId=None):
#     return render_template('product.html', product=productId)

@main.route('/database/')
def database(productId=None):
    products = Products.query.all()
    # print(products)
    return {"products": [p.productname for p in products]}
