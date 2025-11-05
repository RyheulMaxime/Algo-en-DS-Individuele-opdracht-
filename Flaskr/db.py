from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     print("User created")

#     def __repr__(self):
#         return f'<User {self.username}>'

# class User(db.Model):
#     __tablename__ = "user"
#     __table_args__ = {'schema': 'public'}

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         print(f'<User {self.username}>')
#         return f'<User {self.username}>'


class Products(db.Model):
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(100), nullable=False)
    supplierid = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    createdat = db.Column(db.String(100), nullable=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Products , ${self.productid}, ${self.productname}, ${self.price}>'
