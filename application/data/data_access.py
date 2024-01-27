from application.data.models import User, Admin, Category, Product, Order, Cart, Offers, ProductSearch, UserRole, ManagerApproval, AddCategoryApproval, EditCategoryApproval, AdminApproval
from main import cache 

@cache.memoize(50)
def get_all_product_by_product_name(product_name) : 
    all_product = Product.query.filter_by(name=product_name.strip()).first()
    return all_product

@cache.memoize(50)
def get_all_category_by_name(category_name) : 
    all_category = Category.query.filter_by(name=category_name.strip()).first()
    return all_category

@cache.memoize(50)
def get_all_product_by_productname_category(product_name, category_name) : 
    all_product = Product.query.filter_by(name=product_name.strip(), category = category_name).first()
    return all_product

@cache.cached(timeout=50, key_prefix="get_all_category")
def get_all_category() : 
    all_category = Category.query.all()
    return all_category

@cache.cached(timeout=50, key_prefix="get_all_order")
def get_all_order() : 
    all_order = Order.query.all()
    return all_order

@cache.cached(timeout=50, key_prefix="get_all_offer")
def get_all_offer() : 
    all_offers = Offers.query.all()
    return all_offers

@cache.cached(timeout=50, key_prefix="get_all_manager_approval")
def get_all_manager_approval() : 
    all_approval = ManagerApproval.query.all()
    return all_approval

@cache.cached(timeout=50, key_prefix="get_all_manager_approval")
def get_all_admin_approval() : 
    all_approval = AdminApproval.query.filter_by(status=1).all()
    return all_approval

@cache.cached(timeout=50, key_prefix="get_all_add_category_approval")
def get_all_add_category_approval() : 
    all_approval = AddCategoryApproval.query.all()
    return all_approval

@cache.cached(timeout=50, key_prefix="get_all_edit_category_approval")
def get_all_edit_category_approval() : 
    all_approval = EditCategoryApproval.query.all()
    return all_approval