from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     print("User created")

#     def __repr__(self):
#         return f'<User {self.username}>'
    
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        print(f'<User {self.username}>')
        return f'<User {self.username}>'
