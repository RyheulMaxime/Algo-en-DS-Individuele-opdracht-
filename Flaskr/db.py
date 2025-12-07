from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     # print("User created")

#     # def __repr__(self):
#     #     return f'<User {self.username}>'

#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Products(db.Model):
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(100), nullable=False)
    supplierid = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    createdat = db.Column(db.String(100), nullable=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Categories(db.Model):
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(100), primary_key=False)
    description = db.Column(db.String(256), primary_key=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Customers(UserMixin, db.Model):
    customerid = db.Column(db.Integer, primary_key=True)
    customername = db.Column(db.String(100), primary_key=False)
    contactname = db.Column(db.String(100), primary_key=False)
    address = db.Column(db.String(100), primary_key=False)
    city = db.Column(db.String(100), primary_key=False)
    postalcode = db.Column(db.String(100), primary_key=False)
    country = db.Column(db.String(100), primary_key=False)
    password = db.Column(db.String(100), primary_key=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def get_id(self):
        return self.customerid
    
class Suppliers(db.Model):
    supplierid = db.Column(db.Integer, primary_key=True)
    suppliername = db.Column(db.String(100), primary_key=False)
    contactname = db.Column(db.String(100), primary_key=False)
    address = db.Column(db.String(100), primary_key=False)
    city = db.Column(db.String(100), primary_key=False)
    postalcode = db.Column(db.String(100), primary_key=False)
    country = db.Column(db.String(100), primary_key=False)
    latitude = db.Column(db.Float, primary_key=False)
    longitude = db.Column(db.Float, primary_key=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Orders(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, primary_key=False)
    employeeid = db.Column(db.Integer, primary_key=False)
    orderdate = db.Column(db.String(100), primary_key=False)
    shipperid = db.Column(db.Integer, primary_key=False)
    delivered = db.Column(db.Boolean, primary_key=False)
    createdat = db.Column(db.Date, primary_key=False)
    
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class OrderDetails(db.Model):
    orderdetailid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, primary_key=False)
    productid = db.Column(db.Integer, primary_key=False)
    quantity = db.Column(db.Integer, primary_key=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
