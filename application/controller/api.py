from flask_restful import Resource 
from flask import request, jsonify
from application.data.database import db 
from flask_restful import fields, marshal_with, reqparse
from application.data.models import User, Product, Cart, Category, Order, Offers, ProductSearch, AdminApproval, ManagerApproval, AddCategoryApproval, EditCategoryApproval, ProductSearchNew
from application.utils.validations import NotFoundError, BusinessValidationError, ProductNotFoundError
from application.utils.discount import Discount
from application.data import data_access

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
                'product_id' : product.product_id,
                'name' : product.name, 
                'category' : product.category, 
                'price' : product.price, 
                'quantity' : product.quantity, 
                'unit' : product.unit
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

class CartAPI(Resource) : 
    def get(self, username) : 
        all_products = Cart.query.filter_by(username = username).all()
        print(all_products, username)
        list_of_items = {
            'total_price' : 0, 
            "cart" : {

            }
        }
        counter = 0
        for record in all_products : 
            product_details = Product.query.filter_by(name = record.product_name.strip()).first()
            print(record.product_name)
            list_of_items["cart"][counter] = {
                'product_name' : record.product_name, 
                'quantity' : min(int(record.quantity), int(product_details.quantity)),
                'price' : record.price,
                'cart_id' : int(record.cart_id),
                'max_quantity' : int(product_details.quantity)
            }
            list_of_items['total_price'] += min(int(record.quantity), int(product_details.quantity))*record.price
            counter += 1 


        return list_of_items
    
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass
    
class AdminDashboarAPI(Resource) :
    def get(self, username) : 
        all_category = Category.query.all()
        
        # landing page additional info 
        total_sales = sum([int(order.total_price) for order in Order.query.all()])
        total_inventory = sum([int(product.price) * int(product.quantity) for product in Product.query.all()])
        total_items = sum([int(product.quantity) for product in Product.query.all()])
    
        category_product_mapping = {}
        for category in all_category : 
            product_list = Product.query.filter_by(category = category.name).all()
            category_product_mapping[category.name] = []
            for product in product_list : 
                category_product_mapping[category.name].append({
                    'product-name' : product.name, 
                    'product-quantity' : product.quantity
                })
            

        return {
            "catgoryList" : category_product_mapping, 
            'sales' : total_sales, 
            'inventory' : total_inventory, 
            'items' : total_items
        }
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass
    

class ProductPageAPI(Resource) :
    def get(self, username) :
        obj = Discount()
        obj.ingest_in_database()
        
        # filter products 
        category_product_maping = {}
        all_category = Category.query.all()
        for category in all_category : 
            category_product_maping[category.name.strip()] = []
            all_product = Product.query.filter_by(category = category.name).all()
            for product in all_product : 
                category_product_maping[category.name.strip()].append({
                    'name' : product.name.strip(), 
                    'price' : product.price, 
                    'quantity' : product.quantity})

        return category_product_maping
    
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass

class OffersAPI(Resource) :
    def get(self, username) :
        obj = Discount()
        obj.ingest_in_database()

        all_offer = Offers.query.all()
        offer_product, counter = {}, 0
        
        for offer in all_offer :
            product_name = offer.product_name 
            product_details = Product.query.filter_by(name = product_name).first()

            offer_product[counter] = {
                "product_name" : product_name, 
                "price" : product_details.price, 
                "category" : product_details.category, 
                "discount" : offer.discount
            }
            counter += 1 

        return offer_product
    
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass
    
class SearchResult(Resource) :
    def get(self, username) :
        query = request.args.get('q', '')    
        query_results = ProductSearchNew.query.filter(ProductSearchNew.name.op("MATCH")(query + '*') | ProductSearchNew.category.op("MATCH")(query + '*') | ProductSearchNew.price.op("MATCH")(query + '*')).all()
        final_result = {}
        for result in query_results : 
            if result.category.strip() != "category" :
                if result.category not in final_result :
                    final_result[result.category] = []
                final_result[result.category].append({
                    "name" : result.name, 
                    "price" : None, 
                    "quantity" : None
                })

        for category in final_result :
            for product in final_result[category] : 
                product_name = product["name"]
                product_details = Product.query.filter_by(name = product_name.strip()).first()
                product["price"] = product_details.price
                product["quantity"] = product_details.quantity
    
        return jsonify(final_result)
    
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass

class pendingAdminApproval(Resource) :
    def get(self, username) : 
        all_pending = AdminApproval.query.filter_by(status = 1).all()
        all_pending_manager_id = [pending.manager_id for pending in all_pending]

        return {"manager_id" : all_pending_manager_id}
    
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass
    
class pendingManagerApproval(Resource) :
    def get(self, username) : 
        all_pending = ManagerApproval.query.all()
        # all_pending = data_access.get_all_manager_approval()
        result = []
        for pending in all_pending : 
            result.append({
                "name" : pending.category_name, 
                "id" : pending.category_id
            })

        return result

    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass

class pendingAddCategoryApproval(Resource) :
    def get(self, username) : 
        all_pending = AddCategoryApproval.query.all()
        # all_pending = data_access.get_all_add_category_approval()
        result = []
        for pending in all_pending : 
            result.append({
                "name" : pending.category_name,
                "id" : pending.id
            })

        return result 
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass

class pendingEditCategoryApproval(Resource) :
    def get(self, username) : 
        all_pending = EditCategoryApproval.query.all()
        # all_pending = data_access.get_all_edit_category_approval()
        result = []
        for pending in all_pending : 
            result.append({
                "old_name" : pending.old_name, 
                "new_name" : pending.new_name,
                "category_id" : pending.category_id, 
                "id" : pending.id
            })

        return result
    def put(self, username) : 
        pass 
    def delete(self, username) : 
        pass 
    def post(self, username) :
        pass