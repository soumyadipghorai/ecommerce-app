from flask_restful import Resource 
from application.database import db 
from flask_restful import fields, marshal_with, reqparse
from application.models import User, Product 
from application.validations import NotFoundError, BusinessValidationError, ProductNotFoundError

# it helps in formatting if you don't want any fields 
# then directly delete it from here and it would be reflected in the output
output_fields = {
    'user_id' : fields.Integer, 
    'username' : fields.String, 
    'email' : fields.String
}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')

create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument('name')
create_product_parser.add_argument('category')
create_product_parser.add_argument('unit')
create_product_parser.add_argument('price')
create_product_parser.add_argument('quantity')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('email')
update_user_parser.add_argument('password')

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument('name')
update_product_parser.add_argument('category')

class UserAPI(Resource) :
    def get(self, username): 

        user = db.session.query(User).filter(User.username == username).first()
        if user: 
            return {
                'user_id' : user.user_id,
                'username' : user.username, 
                'email' : user.email
                }
        else : 
            raise NotFoundError(status_code = 400, error_code= 'BE101') 

    def put(self, username): 

        args = update_user_parser.parse_args()
        email = args.get('email', None)
        password = args .get('password', None)
        print(args)

        if password is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1005', error_message = 'password is required')
        elif len(password) < 4 : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1007', error_message = 'enter strong password')

        if email is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1002', error_message = 'email is required')

        if "@" in email : 
            pass 
        else : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1003', error_message = 'invalid email')

        print(email)
        # enter both new email and password 
        anotherUser = db.session.query(User).filter(User.email == email).first()
        if anotherUser : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1006', error_message = 'duplicate email')

        user = db.session.query(User).filter(User.username == username).first()
        if user is None :
            raise NotFoundError(status_code = 404, error_code= 'BE101')

        user.email = email 
        user.password = password 
        db.session.add(user)
        db.session.commit()
        return {
                'user_id' : user.user_id,
                'username' : user.username, 
                'email' : user.email
                }

    def delete(self, username): 
        args = update_user_parser.parse_args()
        print(args)
        email = args.get('email', None)

        user = db.session.query(User).filter(User.email == email).first()
        if user is None :
            raise NotFoundError(status_code = 404, error_code= 'BE101') 

        db.session.delete(user)
        db.session.commit()

        return {
            'username' : user.username, 
            'eamil' : user.email
        } 

    def post(self): 
        args = create_user_parser.parse_args()
        print(args)
        username = args.get('username', None)
        email = args.get('email', None)
        password = args.get('password', None)

        print(password)

        if username is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1001', error_message = 'username is required')
        
        if email is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1002', error_message = 'email is required')

        if "@" in email : 
            pass 
        else : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1003', error_message = 'invalid email')

        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()

        if user : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1004', error_message = 'duplicate user')
        
        new_user = User(username = username, email = email, password = password)
        db.session.add(new_user)
        db.session.commit()
        return {
            'user_id' : new_user.user_id, 
            'username' : new_user.username, 
            'email' : new_user.email, 
            'password' : new_user.password

        }

class ProductAPI(Resource) : 
    def get(self, product) : 

        product = db.session.query(Product).filter(Product.name == product).first()
        
        if product: 
            return {
                'product_id' : product.product_id,
                'name' : product.name, 
                'category' : product.category, 
                'price' : product.price, 
                'quantity' : product.quantity, 
                'unit' : product.unit
                }
        else : 
            raise ProductNotFoundError(status_code = 400, error_code= 'BE102') 

    def put(self, product) : 
        
        args = update_product_parser.parse_args() 
        product = args.get('name', None)
        category = args.get('category', None)

        if product is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1008', error_message = 'Product name is required')

        if category is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1009', error_message = 'Category name is required')

        product_db = db.session.query(Product).filter(Product.name == product).first()

        if product_db is None : 
            raise ProductNotFoundError(status_code = 400, error_code= 'BE102')  

        product_db.category = category
        db.session.add(product_db)
        db.session.commit()
        return {
                'product_id' : product_db.product_id,
                'name' : product_db.name, 
                'category' : product_db.category, 
                'price' : product_db.price, 
                'quantity' : product_db.quantity, 
                'unit' : product_db.unit
                }
    
    def delete(self, product) : 
        args = update_product_parser.parse_args()
        product_name = args.get('name', None)

        if product_name is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1008', error_message = 'Product name is required')

        product = db.session.query(Product).filter(Product.name == product_name).first()

        if product is None : 
            raise ProductNotFoundError(status_code = 400, error_code= 'BE102')  

        db.session.delete(product)
        db.session.commit()
        return {
                'product_id' : product_db.product_id,
                'name' : product_db.name, 
                'category' : product_db.category, 
                'price' : product_db.price, 
                'quantity' : product_db.quantity, 
                'unit' : product_db.unit
                }


    def post(self) : 
        args = create_product_parser.parse_args()

        product_name = args.get('name', None) 
        product_category = args.get('category', None) 
        product_unit = args.get('unit', None) 
        product_price = args.get('price', None) 
        product_quantity = args.get('quantity', None) 

        if product_name is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1008', error_message = 'Product name is required')

        if product_category is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1009', error_message = 'Category name is required')

        if product_unit is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1010', error_message = 'unit is required')

        if product_price is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1011', error_message = 'price is required')

        if product_quantity is None : 
            raise BusinessValidationError(status_code = 400, error_code = 'BE1012', error_message = 'quantity is required')

        new_product = Product(
            name = product_name, category = product_category, 
            unit = product_unit, price = product_price, quantity = product_quantity
        )

        db.session.add(new_product)
        db.session.commit()

        return {
                'product_id' : new_product.product_id,
                'name' : new_product.name, 
                'category' : new_product.category, 
                'price' : new_product.price, 
                'quantity' : new_product.quantity, 
                'unit' : new_product.unit
            }