from .database import db

class User(db.Model) : 
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

class Admin(db.Model) : 
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Category(db.Model) : 
    __tablename__ = 'category' 
    category_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True)
 
class Product(db.Model): 
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True)
    unit = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)

class Order(db.Model) : 
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String)
    category = db.Column(db.String)
    product_name = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    date = db.Column(db.String)
    total_price = db.Column(db.Integer)

class Cart(db.Model) : 
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String)
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    category = db.Column(db.String)