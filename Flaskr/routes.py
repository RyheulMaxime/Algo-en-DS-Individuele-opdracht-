from flask import Blueprint, request, redirect, url_for, render_template, session, logging
from .db import *
from logging.config import dictConfig
from flask import current_app
from flask_socketio import emit # <-- Only import emit
from . import socketio, login_manager   # import socketio from the app package
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

main = Blueprint('main', __name__)

# Helper functions
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
    user = None
    if current_user.is_authenticated:
        # print("user logged in")
        user = current_user

    products = Products.query.all()
    sorting_system = request.args.get('sorting_system')
    if sorting_system is None:
        return render_template('index.html',customer=user, products=products, sorting_system=sorting_system)

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
            return render_template('index.html',customer=user, products=sorted_products, sorting_system=sorting_system)
        return render_template('index.html',customer=user, products=products, sorting_system=sorting_system)
    return render_template('index.html', customer=user, products=None)

@main.route('/product', methods=['GET', 'POST'])
# @main.route('/product', methods=['GET', 'POST'])
def product(product_id=None):
    
    product_id = request.args.get('id')
    supplier_id = request.args.get('supplierid')
    category_id = request.args.get('categoryid')
    
    if current_user.is_authenticated:
        user = current_user

    if request.method == "POST":
        quantity = request.form.get('quantity')

        if current_user.is_authenticated:
            print("place order")
            new_order_id = Orders.query.order_by(Orders.orderid.desc()).first().orderid + 1
            customer_id = current_user.customerid
            new_order = Orders(orderid = new_order_id, customerid=customer_id, employeeid=None, orderdate=datetime.date.today(), shipperid=None, delivered=False)
            db.session.add(new_order)
            # db.session.commit()
            print(quantity)

            new_order_details_id = OrderDetails.query.order_by(OrderDetails.orderdetailid.desc()).first().orderdetailid + 1
            new_order_details = OrderDetails(orderdetailid = new_order_details_id, orderid=new_order_id, productid=product_id, quantity=quantity)
            
            db.session.add(new_order_details)
            db.session.commit()
            return redirect(url_for('main.index'))

    
    if product_id is None or supplier_id is None or category_id is None:
        return render_template('product.html', product=None)
    product_info = Products.query.get((int(product_id), int(supplier_id), int(category_id)))
    supplier_info = Suppliers.query.get(int(supplier_id))
    category_info = Categories.query.get(int(category_id))
    return render_template('product.html', user=user, product=product_info, supplier = supplier_info, category = category_info)


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
            return redirect(url_for("main.index"))  
        elif customer and check_password_hash(customer.password, password):
            login_user(customer)
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

# Logout route
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route("/customer", methods=["GET"])
@login_required
def customer():
    customer = Customers.query.filter_by(customerid=current_user.customerid).first()
    orders = Orders.query.filter_by(customerid=current_user.customerid).all()

    ordered_products = {}
    for order in orders:
        order_details = OrderDetails.query.filter_by(orderid=order.orderid).all()
        for order_detail in order_details:
            product = Products.query.filter_by(productid=order_detail.productid).first()
            ordered_products[order_detail.orderdetailid] = {"productid": product.productid , "productname": product.productname,  "unitprice": product.price, "quantity": order_detail.quantity, "createdat": order_detail.createdat}

    return render_template("customer.html", customer=customer, orders=ordered_products)

@main.route("/customer/reset", methods=["POST"])
@login_required
def changePassword():
    customers = Customers.query.filter_by(customerid=current_user.customerid).first()
    previous_password = request.form.get('previous_password')
    new_password = request.form.get('new_password')
    if previous_password == '':
            previous_password = None

    if previous_password is None or check_password_hash(customers.password, previous_password):
        if new_password == '':
            customers.password = None
            db.session.commit()
            return redirect(url_for("main.index"))
        customers.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()
        return redirect(url_for("main.index"))
    else:
        return redirect(url_for("main.index"))

@main.route("/customer/edit", methods=["POST"])
@login_required
def editCustomer():
    customer = Customers.query.filter_by(customerid=current_user.customerid).first()
    new_name = request.form.get('new_name')
    new_contact = request.form.get('new_contact')
    new_address = request.form.get('new_address')
    new_postalcode = request.form.get('new_postalcode')
    new_city = request.form.get('new_city')
    new_country = request.form.get('new_country')
    
    if new_name != '':
        customer.customername = new_name
    else:
        customer.customername = None
    if new_contact != '':
        customer.contactname = new_contact
    else:
        customer.contactname = None
    if new_address != '':
        customer.address = new_address
    else:
        customer.address = None
    if new_postalcode != '':
        customer.postalcode = new_postalcode
    else:
        customer.postalcode = None
    if new_city != '':
        customer.city = new_city
    else:
        customer.city = None
    if new_country != '':
        customer.country = new_country
    else:
        customer.country = None

    db.session.commit()
    return redirect(url_for("main.customer"))

@main.route("/customer/delete/<order_detail_id>", methods=["POST"])
@login_required
def deleteOrder(order_detail_id):
    OrderDetails.query.filter(OrderDetails.orderdetailid == order_detail_id).delete()
    db.session.commit()
    return redirect(url_for("main.customer"))

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

# Socket.IO endpoints

# Send message to console of the client
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

