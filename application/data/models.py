from .database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table(
    'roles_users', 
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
)

class UserRole(db.Model):
    __tablename__ = 'roles_users'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

class User(db.Model, UserMixin) : 
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255))
    roles = db.relationship("Role", secondary = roles_users, backref = db.backref('users', lazy = 'dynamic'))

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

class Offers(db.Model) : 
    __tablename__ = 'offers'
    offer_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_name = db.Column(db.String)
    category_name = db.Column(db.String)
    discount = db.Column(db.Integer)

class Role(db.Model, RoleMixin) :
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))

class ProductSearch(db.Model) : 
    __tablename__ = 'product_search'
    rowid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    category = db.Column(db.String)

class AdminApproval(db.Model) : 
    __tablename__ = "admin_approval"
    id = db.Column(db.Integer, primary_key = True)
    manager_id = db.Column(db.Integer)
    status = db.Column(db.Boolean())

class ManagerApproval(db.Model) : 
    __tablename__ = "manager_approval"
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String)
    category_id = db.Column(db.Integer)

class AddCategoryApproval(db.Model) : 
    __tablename__ = "add_category_approval"
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String)

class EditCategoryApproval(db.Model) :
    __tablename__ = "edit_category_approval"
    id = db.Column(db.Integer, primary_key = True)
    old_name = db.Column(db.String)
    new_name = db.Column(db.String)
    category_id = db.Column(db.Integer)

class ProductSearchNew(db.Model) : 
    __tablename__ = 'product_search_new'
    rowid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Integer)