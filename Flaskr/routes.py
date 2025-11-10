from flask import Blueprint, request, redirect, url_for, render_template, session
from .db import *

main = Blueprint('main', __name__)

@main.route('/')
def index(productId=None):
    products = Products.query.all()
    
    if products is not None:
        return render_template('index.html', products=products)
    
    return render_template('index.html', products=None)
    



# @main.route('/product/')
# @main.route('/product/<productId>')
# def product(productId=None):
#     return render_template('product.html', product=productId)


# Test database and check connection
@main.route('/database/')
def database(productId=None):
    table = request.args.get('table')
    if table is None:
        pass
    elif table == 'categories':
        categorties = Categories.query.all()
        return {"categories": [c.to_dict() for c in categorties]}
    elif table == 'customers':
        customers = Customers.query.all()
        return {"customers": [c.to_dict() for c in customers]}
    elif table == 'employees':
        pass
    elif table == 'orderdetails':
        order_details = OrderDetails.query.all()
        return {"order_details": [od.to_dict() for od in order_details]}
    elif table == 'orders':
        orders = Orders.query.all()
        return {"orders": [o.to_dict() for o in orders]}
    elif table == 'products':
        products = Products.query.all()
        # return {"products": [p.productname for p in products]}
        return {"products": [p.to_dict() for p in products]}
    elif table == 'shippers':
        pass
    elif table == 'suppliers':
        suppliers = Products.query.all()
        return {"suppliers": [s.to_dict() for s in suppliers]}
    elif table == 'users':
        users = User.query.all()
        return {"users": [u.to_dict() for u in users]}
    # elif table == 'all':
    #     return {"users": [u.username for u in User.query.all()], "products": [p.productname for p in Products.query.all()]}
    
    # products = Products.query.all()
    # print(products)
    # return {"products": [p.productname for p in products]}
    
