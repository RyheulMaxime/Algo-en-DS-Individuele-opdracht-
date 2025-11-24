from flask import Blueprint, request, redirect, url_for, render_template, session, logging
from .db import *
from logging.config import dictConfig
from flask import current_app
from flask_socketio import emit # <-- Only import emit
from . import socketio   # import socketio from the app package


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index(productId=None):
    products = Products.query.all()
    sorting_system = request.args.get('sort').lower()
    print("************************** sorting system: ", sorting_system)
    if sorting_system is None:
        sorting_system = "Category"

    if products is not None:
        sorted_products = None
        if sorting_system == "category":
            sorted_products = sort_by_category(products)
            print(sorted_products)
            # sorted_products = sorted(products, key=lambda p: p.category)
        elif sorting_system == "price low-high":
            sorted_products = sorted(products, key=lambda p: p.price)
        elif sorting_system == "price high-low":
            sorted_products = sorted(products, key=lambda p: p.price, reverse=True)
        elif sorting_system == "a-z":
            sorted_products = sorted(products, key=lambda p: p.productname)
        elif sorting_system == "z-a":
            sorted_products = sorted(products, key=lambda p: p.productname, reverse=True)
        # print(products)
        # sorted_products = []
        # sorted_products = sorted(products, key=lambda p: p.productname)
        # for product in sorted_products:
        #     print(product.productname)
        # current_app.logger.info(products) # Used for logging server side
        if sorted_products is not None:
            return render_template('index.html', products=sorted_products, sorting_system=sorting_system)
        return render_template('index.html', products=products, sorting_system=sorting_system)
    # current_app.logger.info("Products not found") # Used for logging server side
    return render_template('index.html', products=None)

# not sure if needed
def sort_alphabetically(products, sorting_system):
    pass

# not sure if needed
def sort_by_price(products, sorting_system):
    pass


def sort_by_category(products):
    categorties = Categories.query.all()
    sorted_products = {}
    for category in categorties:
        sorted_products[category.categoryname] = []    
    for product in products:
        for category in categorties:
            if product.categoryid == category.categoryid:
                sorted_products[category.categoryname].append(product)
    # print(sorted_products)
    return sorted_products

# @main.route('/product/')
# @main.route('/product/<productId>')
# def product(productId=None):
#     return render_template('product.html', product=productId)


# Test database and check connection
@main.route('/database/', methods=['GET'])
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
        suppliers = Suppliers.query.all()
        return {"suppliers": [s.to_dict() for s in suppliers]}
    # elif table == 'users':
    #     users = User.query.all()
    #     return {"users": [u.to_dict() for u in users]}
    # elif table == 'all':
    #     return {"users": [u.username for u in User.query.all()], "products": [p.productname for p in Products.query.all()]}    
 

# Socket.IO event inside the blueprint
# @socketio.on("connect")
# def connected():
#     print(f"Client connected: {request.sid}")
#     emit("log", {"msg": "Client connected!"})

# Send message to console of the client
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

# @socketio.on('sort')
# def sort_products(data):
#     print("sort_products")
#     print('received message: ' + data)

# @socketio.on('search')
# def search_products(data):
#     print("search_products")
#     print('received message: ' + data)

# @socketio.on('update_list_from_server')
# def update_list_from_server(data):
#     pass

@socketio.on("disconnect")
def disconnected():
    print(f"Client disconnected: {request.sid}")
    emit("log", {"msg": "Client disconnected!"})
