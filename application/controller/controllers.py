import logging
import pandas as pd 
from datetime import date 
import matplotlib.pyplot as plt
from flask import current_app as app 
from application.data.database import db
from application.utils.discount import Discount
from application.utils.create_data import create_data
from application.data.models import User, Admin, Category, Product, Order, Cart, ManagerApproval, AdminApproval, AddCategoryApproval, EditCategoryApproval
from application.data import data_access
from datetime import datetime
from main import cache 

from flask_security import roles_required, login_required, current_user
from flask import Flask, request, render_template, redirect, url_for, session

from application.jobs import tasks


all_users = [user.username for user in User.query.all()]
all_admin = [user.username for user in Admin.query.all()]

logger2 = logging.getLogger('file2')
logger2.setLevel(logging.DEBUG)

file_handler2 = logging.FileHandler('logs/controller.log')
file_handler2.setLevel(logging.DEBUG)  

formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler2.setFormatter(formatter)

logger2.addHandler(file_handler2)

# user login ==> main landing page 
@app.route('/', methods = ['GET', 'POST'])
@login_required
def index() : 
    if request.method == 'GET' : 
        return render_template('index.html', user_id = current_user.id)


@app.route('/admin-login', methods = ['GET', 'POST'])
def admin_login() : 
    if request.method == 'GET' : 
        try : 
            if session['user'] is None or session['user'] not in all_admin : 
                return render_template('admin_login.html', message = "")
            else : 
                name = session['user']
                return redirect(url_for('admin_dashboard', admin = name))
        except : 
            return render_template('admin_login.html', message = "")
    
    elif request.method == 'POST' : 
        admin_username = request.form['username']
        admin_password = request.form['Password']

        print(admin_username, admin_password)

        admin = Admin.query.filter_by(username = admin_username).first()

        if admin : 
            print(admin)
            if admin.password == admin_password : 
                session['user'] = admin_username
                return redirect(url_for('admin_dashboard', admin = admin_username))
            else : 
                return render_template('admin_login.html', message = 'Wrong password')
        else : 
            return render_template('admin_login.html', message = 'Wrong username')
    else : 
        return render_template('admin_login.html', message = '')

@app.route('/manager-dashboard/<manager>', methods = ["GET", 'POST'])
@login_required
@roles_required('manager')
def manager_dashboard(manager) : 
    if request.method == "GET" : 
        existing_request = AdminApproval.query.filter_by(manager_id = int(manager)).first()
        if not existing_request :
            new_request = AdminApproval(manager_id = int(manager), status = 1)
            db.session.add(new_request)
            db.session.commit() 
        elif existing_request.status == 0 :  
            return render_template("manager_dashboard.html", manager = manager)
        
        return redirect(url_for('index', user_id = manager))
    
    if request.method == 'POST' :
        form_name = request.form['form_name']
        if form_name == 'logout-form' :
            AdminApproval.query.filter_by(manager_id = int(manager)).delete()
            db.session.commit() 
            return redirect(url_for('index', user_id = manager)) 
        elif form_name == "delete-category" : 
            category_id = request.form['category-id']  
            Category.query.filter_by(category_id = int(category_id)).delete()
            ManagerApproval.query.filter_by(category_id = int(category_id)).delete()
            db.session.commit()
            return redirect(url_for('manager_dashboard', manager = manager))
        
        elif form_name == "add-category" : 
            new_category_name = request.form["category-name"]
            peding_id = request.form["pending-id"]
            new_category = Category(name = new_category_name)
            db.session.add(new_category)

            AddCategoryApproval.query.filter_by(id = int(peding_id)).delete()
            db.session.commit()
            return redirect(url_for('manager_dashboard', manager = manager))

        elif form_name == "edit-category" : 
            old_category_id = request.form["category-id"]
            pending_id = request.form["pending-id"]
            old_category_name = request.form["old-category-name"]
            new_category_name = request.form["new-category-name"]

            all_product_with_old_category_name = Product.query.filter_by(category = old_category_name).all()
            for product in all_product_with_old_category_name : 
                product.category = new_category_name

            existing_category_details = Category.query.filter_by(category_id = int(old_category_id)).first()
            existing_category_details.name = new_category_name

            EditCategoryApproval.query.filter_by(id = int(pending_id)).delete()
            db.session.commit()

            return redirect(url_for('manager_dashboard', manager = manager))

@app.route('/admin-dashboard/<admin>', methods = ['GET', 'POST'])
@login_required
@roles_required("admin")
def admin_dashboard(admin) : 
    if request.method == 'GET' : 
        
        # all_category = Category.query.all()

        all_category = data_access.get_all_category()

        errorCode = request.args.get('error')
        if errorCode is None : 
            message = ""
        elif int(errorCode) == 21 : 
            message = "Can't delete category! Few products still available in the category"
        elif int(errorCode) == 22 : 
            message = "Can't delete product! Few units still available for the product"
        elif int(errorCode) == 23 : 
            message = "Category dosen't exist"

        if len(all_category) == 0 :
            return render_template('admin_dashboard.html', catgoryList = all_category, admin = admin, message = message)
        else : 
            
            # landing page additional info 
            total_sales = sum([int(order.total_price) for order in Order.query.all()])
            total_inventory = sum([int(product.price) * int(product.quantity) for product in Product.query.all()])
            total_items = sum([int(product.quantity) for product in Product.query.all()])

            hero_data = {
                'sales' : total_sales, 
                'inventory' : total_inventory, 
                'items' : total_items
            }

            category_product_mapping = {}
            for category in all_category : 
                product_list = Product.query.filter_by(category = category.name).all()
                category_product_mapping[category.name] = []
                for product in product_list : 
                    category_product_mapping[category.name].append({
                        'product-name' : product.name, 
                        'product-quantity' : product.quantity
                    })
                

            return render_template(
                'admin_dashboard.html', catgoryList = category_product_mapping, 
                admin = admin, message = message, hero_data = hero_data
            )

    elif request.method == 'POST' : 
        # category = request.form['category']
        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))

        elif form_name == 'category-delete-form' :
            category_to_delete = request.form['category']

            availablity_check = Product.query.filter_by(category = category_to_delete).first()

            if availablity_check : 
                return redirect(url_for('admin_dashboard', admin = admin, error = 21))

            else : 
                # Category.query.filter_by(name=category_to_delete).delete()
                # db.session.commit()
                # category_details = Category.query.filter_by(name=category_to_delete).first()
                category_details = data_access.get_all_category_by_name(category_to_delete)
                new_request_for_manager = ManagerApproval(category_name = category_details.name, category_id = category_details.category_id)
                db.session.add(new_request_for_manager)
                db.session.commit()
                return redirect(url_for('admin_dashboard', admin = admin))

        elif form_name == 'category-edit-form' : 
            category_to_edit = request.form['category-to-edit']
            new_category_name = request.form['newCategoryName']

            category_availability_check = Category.query.filter_by(name = category_to_edit.strip()).first()

            if not category_availability_check : 
                return redirect(url_for('admin_dashboard', admin = admin, error = 23))
            else : 
                old_category_name = category_availability_check.name
                
                new_edit_request = EditCategoryApproval(old_name = old_category_name, new_name = new_category_name, category_id = category_availability_check.category_id)
                db.session.add(new_edit_request)
                db.session.commit()

                return redirect(url_for('admin_dashboard', admin = admin)) 
            
        elif form_name == 'admin-approval-form' : 
            manager_id = request.form['manager-id']

            manager_to_approve = AdminApproval.query.filter_by(manager_id = int(manager_id)).first()
            manager_to_approve.status = 0

            db.session.add(manager_to_approve)
            db.session.commit()
            return redirect(url_for('admin_dashboard', admin = admin))
 
        elif form_name == "product-delete-form" :
            product_to_delete = request.form['product']
            
            product_availability_check = Product.query.filter_by(name = product_to_delete.strip()).first()

            if product_availability_check.quantity != 0 : 
                return redirect(url_for('admin_dashboard', admin = admin, error = 22))
            else : 
                Product.query.filter_by(name= product_to_delete.strip()).delete()
                db.session.commit()
                return redirect(url_for('admin_dashboard', admin = admin))

    else: 
        return render_template('error.html')


@app.route('/dashboard/<admin>', methods = ['GET', 'POST'])
@login_required
@roles_required("admin")
def dash_board(admin) : 
    if request.method == 'GET' : 
        # all_order = Order.query.all()
        all_order = data_access.get_all_order()
        category_wise_sale = {}

        for order in all_order : 
            if order.category not in category_wise_sale.keys() : 
                category_wise_sale[order.category] = order.total_price
            else : 
                category_wise_sale[order.category] += order.total_price

        # all_category_value = Category.query.all()

        all_category_value = data_access.get_all_category()
        all_category = {}

        for category in all_category_value :
            all_category[category.name.strip()] = 0 

            all_product_from_same_category = Product.query.filter_by(category = category.name.strip()).all()
            for product in all_product_from_same_category : 
                all_category[category.name.strip()] += int(product.price) * int(product.quantity)


        
        category_name_sale = list(category_wise_sale.keys())
        total_sale = list(category_wise_sale.values())

        category_name_store = list(all_category.keys())
        total_value = list(all_category.values())

        # creating plots for summary dashboard 
        fig = plt.figure()
        plt.clf()
        plt.bar(category_name_sale, total_sale, tick_label = category_name_sale, color = 'green')
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.title("Categoy wise total Sales")
        plt.savefig('static/images/category-wise-sale.png')
        
        fig = plt.figure()
        plt.clf()
        plt.bar(category_name_store, total_value, tick_label = category_name_store, color ='blue')
        plt.xlabel("Category in Stock")
        plt.ylabel("Total value")
        plt.title("Categoy wise total Stock price")
        plt.savefig('static/images/category-wise-stock.png')
        
        job = tasks.create_summary_data_job.delay()
        result = job.wait()

        return render_template('dashbord.html', admin = admin)


    elif request.method == 'POST' :

        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))
 
 
@app.route('/products/<username>', methods = ['GET', 'POST'])
@login_required
def product_page(username) : 
    if request.method == 'GET' : 
        # update offer table 
        obj = Discount()
        obj.ingest_in_database()

        # filter products 
        category_product_maping = {}
        # all_category = Category.query.all()

        all_category = data_access.get_all_category()
        for category in all_category : 
            category_product_maping[category.name.strip()] = []
            all_product = Product.query.filter_by(category = category.name).all()
            for product in all_product : 
                category_product_maping[category.name.strip()].append({
                    'name' : product.name.strip(), 
                    'price' : product.price, 
                    'quantity' : product.quantity})


        # all_offer = Offers.query.all()
        all_offer = data_access.get_all_offer()
        offer_product = []
        logger2.info(str(all_offer))
        for offer in all_offer :
            product_name = offer.product_name 
            product_details = Product.query.filter_by(name = product_name).first()

            offer_product.append((product_name, product_details.price, product_details.category, offer.discount))

        return render_template('products.html', name = username, prod_cat_dict = category_product_maping, offer_details = offer_product)

    elif request.method == 'POST' : 
        form_name = request.form['form_name'] 
        if form_name == 'add_to_cart' : 
            product_name, product_category = request.form['product-name'].split('+')
            product_details = Product.query.filter_by(name = product_name.strip(), category = product_category.strip()).first()

            new_cart_item = Cart(
                username = username, 
                product_name = product_name, 
                quantity = 1, 
                price = int(product_details.price), 
                category = product_category
            )

            db.session.add(new_cart_item)

            db.session.commit()

            return redirect(url_for('product_page', username = username))
        elif form_name == 'search_product' : 
            query = request.form['querry']  
            return redirect(url_for('search', q = query, username = username))
    else : 
        return render_template('error.html')



@app.route('/add-category/<admin>', methods = ['GET', 'POST'])
@login_required
@roles_required("admin")
def add_category(admin) : 
    if request.method == 'GET' :
        args = request.args.get('message')
        if args is None : 
            args = ""
        return render_template('add_category.html', admin = admin, message = args)
    
    elif request.method == 'POST' : 
        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))

        elif form_name == 'category-form' :
            category_name = request.form['categoryName']
            print(category_name)
            # checking for existing category with same name 
            existing_category = Category.query.filter_by(name = category_name).first()

            print(url_for('add_category', admin = admin))
            if not existing_category : 
                # new_category = Category(name = category_name)
                # db.session.add(new_category)
                # db.session.commit()
                new_category_request = AddCategoryApproval(category_name = category_name)
                db.session.add(new_category_request)
                db.session.commit()

                return redirect(url_for('add_category', admin = admin, message = 'category added'))
                
            else : 
                return redirect(url_for('add_category', admin = admin, message = 'category already exists'))
        
    else : 
        return render_template('error.html')


@app.route('/add-product/<admin>', methods = ['GET', 'POST'])
@login_required
@roles_required("admin")
def add_product(admin) : 
    if request.method == 'GET' : 
        category = request.args.get('category')
        return render_template('add_product.html', admin = admin, category = category)

    elif request.method == 'POST' : 

        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))

        elif form_name == 'product-form' :
            product_name = request.form['productName']
            product_unit = request.form['unit']
            product_price = request.form['price']
            product_quantity = request.form['quantity']

            category = request.args.get('category')

            # if product with the same name exists then only update the info 
            # else add new product
            product = Product.query.filter_by(name = product_name).first()
            if product :
                product.unit = product_unit
                product.price = product_price 
                product.quantity = product_quantity

            else : 
                new_product = Product(
                    name = product_name, 
                    unit = product_unit, 
                    price = product_price, 
                    quantity = product_quantity, 
                    category = category
                )

                db.session.add(new_product)

            db.session.commit()

            return redirect(url_for('admin_dashboard', admin = admin))
    
    else : 
        return render_template('error.html')


@app.route('/buy-product/<username>', methods = ['GET', 'POST']) 
@login_required
def buy_product(username) : 
    if request.method == 'GET' : 
        product_name = request.args.get('product-name')
        print(product_name)

        # product_details = Product.query.filter_by(name = product_name.strip()).first()
        product_details = data_access.get_all_product_by_product_name(product_name)

        product_quantity = product_details.quantity 

        return render_template(
            'buy_product.html', product_name = product_name, 
            max_limit = product_quantity, product_price = product_details.price, total_price = 0, username = username)

    elif request.method == 'POST' : 

        form_name = request.form['form_name']
        if form_name == 'buy-product' : 
            try : 
                product_name = request.args.get('product-name')
                # product_details = Product.query.filter_by(name = product_name).first()
                product_details = data_access.get_all_product_by_product_name(product_name)

                quantity_ordered = request.form['quantity']

                # add all the order info to the orders table 
                order_username = username
                order_category = product_details.category
                order_product_name = product_name
                order_price = product_details.price 
                order_quantity = quantity_ordered
                order_date = date.today()
                order_total_price = int(quantity_ordered) * int(product_details.price)

                new_order = Order(
                    username = order_username, category = order_category, 
                    product_name = order_product_name, price = order_price, 
                    quantity = order_quantity, date = order_date, total_price = order_total_price
                )

                db.session.add(new_order)

                # old_product = Product.query.filter_by(name = product_name, category = order_category).first()
                old_product = data_access.get_all_product_by_productname_category(product_name, order_category)

                print(old_product)
                old_product.quantity -= int(order_quantity)
                print(old_product.quantity)

                db.session.commit()
                print("commit")

                return redirect(url_for('product_page', username = username))
        
            except : 
                db.session.rollback()
                return render_template('error.html')
            

@app.route('/cart/<username>', methods = ['GET', 'POST'])
@login_required
def cart_page(username) : 
    if request.method == 'GET' : 
        all_products = Cart.query.filter_by(username = username).all()

        list_of_items, total_price = [], 0

        for record in all_products : 
            print(record.product_name)

            product_details = Product.query.filter_by(name = record.product_name.strip()).first()

            # product_details = data_access.get_all_product_by_product_name(record.product_name)
            print(product_details)

            list_of_items.append({
                'product_name' : record.product_name, 
                'quantity' : min(int(record.quantity), int(product_details.quantity)),
                'price' : record.price,
                'cart_id' : int(record.cart_id),
                'max_quantity' : int(product_details.quantity)
            })

            total_price += int(record.quantity) * int(record.price)


        return render_template('cart.html', username = username, cart_data = list_of_items, total_price = total_price)
 
    elif request.method == 'POST' :
        
        form_name = request.form['form_name']

        if form_name == 'logout-form' : 
            session['user'] = None 
            return redirect(url_for('login'))

        # quantity update 
        elif form_name == 'update-quantity' : 
            quantity = request.form['quantity']
            ID = request.form['primary_key']

            old_record = Cart.query.filter_by(cart_id = ID).first()
            old_record.quantity = quantity 

            db.session.commit()

            return redirect(url_for('cart_page', username = username))

        elif form_name == 'buy-all-form' : 

            all_products = Cart.query.filter_by(username = username).all()

            print(all_products)
            list_of_items, total_price = [], 0

            # add all the records to the order table only if the product is available and buy quantity > 0 
            for record in all_products : 
                print(record)
                product_details = Product.query.filter_by(name = record.product_name.strip()).first()
                # product_details = data_access.get_all_product_by_product_name(record.product_name)
                print(record, product_details)
                if min(int(record.quantity), int(product_details.quantity)) > 0 :
                    new_order = Order(
                        username = username, category = product_details.category, 
                        product_name = record.product_name,
                        price = product_details.price, 
                        quantity = min(int(record.quantity), int(product_details.quantity)), 
                        date = date.today(), 
                        total_price = int(product_details.price) * min(int(record.quantity), int(product_details.quantity))
                    )

                    db.session.add(new_order)

                    Cart.query.filter_by(cart_id = record.cart_id).delete()

                    old_product = Product.query.filter_by(name = record.product_name.strip(), category = product_details.category.strip()).first()
                    old_product.quantity -= min(int(record.quantity), int(product_details.quantity))

                total_price += int(record.quantity) * int(record.price)

            db.session.commit()

            return redirect(url_for('product_page', username = username))
        
@app.route("/search_results/<username>", methods = ['GET', 'POST'])
def search(username) : 
    if request.method == 'GET' : 
        q = request.args.get('q') 
        return render_template('search_result.html', name = username, query = q)
    elif request.method == 'POST' : 
        form_name = request.form['form_name'] 
        if form_name == 'add_to_cart' : 
            product_name, product_category = request.form['product-name'].split('+')
            product_details = Product.query.filter_by(name = product_name.strip(), category = product_category.strip()).first()

            new_cart_item = Cart(
                username = username, 
                product_name = product_name, 
                quantity = 1, 
                price = int(product_details.price), 
                category = product_category
            )

            db.session.add(new_cart_item)

            db.session.commit()

            return redirect(url_for('product_page', username = username))
        elif form_name == 'search_product' : 
            query = request.form['querry']  
            return redirect(url_for('search', q = query, username = username))
    else : 
        return render_template('error.html')
    
@app.route("/hello/<username>", methods = ["GET", "POST"])
def hello(username) :  
    job = tasks.test_html_report_sender.delay()
    result = job.wait()

    return str(result), 200 