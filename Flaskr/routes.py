from flask import Blueprint, request, redirect, url_for, render_template, session, logging
from .db import *
from logging.config import dictConfig
from flask import current_app
from flask_socketio import emit # <-- Only import emit
from . import socketio, login_manager   # import socketio from the app package
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

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

# Order functions
def place_order(product_id, quantity):
    order_success = False
    print("place_order")
    print(product_id, quantity)
    
    # ad logics to place an order

    if order_success:
        return "Order placed successfully"
    else:
        socketio.emit('order_failed', {'productid': product_id})
        return "Order failed"

# Account user functions
# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(int(user_id))

@main.route('/', methods=['GET'])
def index():
    products = Products.query.all()
    sorting_system = request.args.get('sorting_system')
    # print("************************** sorting system: ", sorting_system)
    if sorting_system is None:
        return render_template('index.html', products=products, sorting_system=sorting_system)
        # sorting_system = "Category"
    # print("************************** sorting system: ", sorting_system)

    if products is not None:
        sorted_products = None
        if sorting_system.lower() == "category":
            sorted_products = sort_by_category(products)
            # sorted_products = sorted(products, key=lambda p: p.category)
        elif sorting_system.lower() == "price_asc":
            sorted_products = sorted(products, key=lambda p: p.price)
        elif sorting_system.lower() == "price_desc":
            sorted_products = sorted(products, key=lambda p: p.price, reverse=True)
        elif sorting_system.lower() == "name_asc":
            sorted_products = sorted(products, key=lambda p: p.productname)
        elif sorting_system.lower() == "name_desc":
            sorted_products = sorted(products, key=lambda p: p.productname, reverse=True)
        if sorted_products is not None:
            # print(sorted_products)
            return render_template('index.html', products=sorted_products, sorting_system=sorting_system)
        return render_template('index.html', products=products, sorting_system=sorting_system)
    return render_template('index.html', products=None)

# @main.route('/product/<productId>', methods=['GET'])
@main.route('/product', methods=['GET', 'POST'])
def product(product_id=None):
    # try:
    #     product_id = request.args.get('id')
    # except Exception as e:
    #     print(e)
    product_id = request.args.get('id')
    supplier_id = request.args.get('supplierid')
    category_id = request.args.get('categoryid')
    
    if product_id is None or supplier_id is None or category_id is None:
        return render_template('product.html', product=None)
    product_info = Products.query.get((int(product_id), int(supplier_id), int(category_id)))
    supplier_info = Suppliers.query.get(int(supplier_id))
    category_info = Categories.query.get(int(category_id))
    print("product info: ", product_info)
    return render_template('product.html', product=product_info, supplier = supplier_info, category = category_info)

@main.route('/supplier', methods=['GET', 'POST'])
def supplier(supplier_id=None):
    supplier_id = request.args.get('id')
    # make funtion to return to previous page and give error message as popup
    if supplier_id is None:
        return render_template('supplier.html', supplier=None)
    
    supplier_info = Suppliers.query.get(int(supplier_id))
    supplier_products = Products.query.filter_by(supplierid=supplier_id).all()
    print("supplier info: ", supplier_info)
    print(supplier_info.longitude, supplier_info.latitude)
    return render_template('supplier.html', supplier=supplier_info, products=supplier_products)

# Register route
@main.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        customer_info = {"username": None, "password": None, "contact_name": None, "address": None, "city": None, "postal_code": None, "country": None}

        for key, value in customer_info.items():
            info = request.form.get(key)
            if info is None:
                pass
            elif info == "":
                customer_info[key] = None
            else:
                customer_info[key] = info
        # print(customer_info)

        if Customers.query.filter_by(customername=customer_info['username']).first():
            return render_template("sign_up.html", error="Username already taken!")
        
        customer_id = Customers.query.order_by(Customers.customerid.desc()).first().customerid + 1
        if customer_info['password'] is not None:
            hashed_password = generate_password_hash(customer_info['password'], method="pbkdf2:sha256")
            new_user = Customers(customerid=customer_id, customername=customer_info['username'], contactname=customer_info['contact_name'], address=customer_info['address'], city=customer_info['city'], postalcode=customer_info['postal_code'], country=customer_info['country'], password=hashed_password)
        else:
            new_user = Customers(customerid=customer_id, customername=customer_info['username'], contactname=customer_info['contact_name'], address=customer_info['address'], city=customer_info['city'], postalcode=customer_info['postal_code'], country=customer_info['country'], password=customer_info['password'])

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main.login"))
    
    return render_template("sign_up.html")

# Login route
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        customer = Customers.query.filter_by(customername=username).first()

        if password == '':
            password = None

        if customer and password == customer.password:
            login_user(customer)
            print("user logged in without password")    
        elif customer and check_password_hash(customer.password, password):
            login_user(customer)
            print("user logged in")
            return redirect(url_for("dashboard"))
        else:
            print("user not logged in")
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# Logout route
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# Test database and check connection
@main.route('/database/', methods=['GET'])
def database():
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

# Socket.IO endpoints

# Send message to console of the client
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('order')
def handle_message(data):
    
    place_order(data['productid'], data['quantity'])

@socketio.on('Login')
def handle_message(data):
    
    place_order(data['productid'], data['quantity'])