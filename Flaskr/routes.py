from flask import Blueprint, request, redirect, url_for, render_template, session

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")


@main.route('/product/')
@main.route('/product/<productId>')
def product(productId=None):
    return render_template('product.html', product=productId)
