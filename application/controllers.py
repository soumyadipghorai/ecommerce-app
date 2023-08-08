from flask import Flask, request, render_template, redirect, url_for, session
from flask import current_app as app 
from application.models import User, Admin, Category, Product, Order, Cart
from application.database import db
from datetime import date 
import matplotlib.pyplot as plt


all_users = [user.username for user in User.query.all()]
all_admin = [user.username for user in Admin.query.all()]

@app.route('/', methods = ['GET', 'POST'])
def login() : 
    if request.method == 'GET' : 
        if session['user'] is None or session['user'] not in all_users: 
            return render_template('user_login.html', message = '')
        else : 
            name = session['user']

            return redirect(url_for('product_page', username = name))
    
    elif request.method == 'POST' : 
        user_email = request.form['email']
        user_password = request.form['Password']

        print(user_email, user_password)

        user = User.query.filter_by(email = user_email).first()

        if user : 
            print(user)
            if user.password == user_password : 
                session['user'] = user.username
                print(session)
                return redirect(url_for('product_page', username = user.username))
            else : 
                return render_template('user_login.html', message = 'Wrong password')
        else : 
            return render_template('user_login.html', message = 'Wrong email')


@app.route('/signin', methods = ['GET', 'POST'])
def signUp() : 
    if request.method == 'GET' :
        return render_template('signin.html', message = "")

    elif request.method == 'POST' : 
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['Password']

        print(user_name, user_email, user_password)

        user = User.query.filter_by(email = user_email).first()

        if user : 
            return render_template('signin.html', message = 'email already exists')
        
        else : 

            new_user = User(username = user_name, email = user_email, password = user_password)
            db.session.add(new_user)
            db.session.commit()

            session['user'] = user_name

            return redirect(url_for('product_page', username = user_name)) 


@app.route('/admin-login', methods = ['GET', 'POST'])
def admin_login() : 
    if request.method == 'GET' : 
        if session['user'] is None or session['user'] not in all_admin : 
            return render_template('admin_login.html', message = "")
        else : 
            name = session['user']
            return redirect(url_for('admin_dashboard', admin = name))
    
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


@app.route('/admin-dashboard/<admin>', methods = ['GET', 'POST'])
def admin_dashboard(admin) : 
    if request.method == 'GET' : 
        if session['user'] == admin : 
            all_category = Category.query.all()
            errorCode = request.args.get('error')
            if errorCode is None : 
                message = ""
            else : 
                message = "Can't delete category! Few products still available in the category"

            if len(all_category) == 0 :
                return render_template('admin_dashboard.html', catgoryList = all_category, admin = admin, message = message)
            else : 
                category_product_mapping = {}
                for category in all_category : 
                    product_list = Product.query.filter_by(category = category.name).all()
                    category_product_mapping[category.name] = []
                    for product in product_list : 
                        category_product_mapping[category.name].append(product.name)
                    

                return render_template('admin_dashboard.html', catgoryList = category_product_mapping, admin = admin, message = message)
        else : 
            return redirect(url_for('admin_login'))

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
                Category.query.filter_by(name=category_to_delete).delete()
                db.session.commit()
                return redirect(url_for('admin_dashboard', admin = admin))


@app.route('/dashboard/<admin>', methods = ['GET', 'POST'])
def dash_board(admin) : 
    if request.method == 'GET' : 
        if session['user'] == admin : 

            all_order = Order.query.all()
            category_wise_sale = {}

            for order in all_order : 
                if order.category not in category_wise_sale.keys() : 
                    category_wise_sale[order.category] = order.total_price
                else : 
                    category_wise_sale[order.category] += order.total_price

            
            x_axis = list(category_wise_sale.keys())
            y_axis = list(category_wise_sale.values())

            #tick_label does the some work as plt.xticks()
            plt.bar(range(len(category_wise_sale)), y_axis, tick_label=x_axis)
            plt.savefig('bar.png')
            return category_wise_sale
            return render_template('dashbord.html', admin = admin)

        else : 
            return redirect(url_for('admin_login'))

    elif request.method == 'POST' :

        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))


@app.route('/products/<username>', methods = ['GET', 'POST'])
def product_page(username) : 
    if request.method == 'GET' : 
        if session['user'] == username : 
            category_product_maping = {}
            all_category = Category.query.all()
            for category in all_category : 
                category_product_maping[category.name] = []
                all_product = Product.query.filter_by(category = category.name).all()
                for product in all_product : 
                    category_product_maping[category.name].append({
                        'name' : product.name, 
                        'price' : product.price, 
                        'quantity' : product.quantity})

            return render_template('products.html', name = username, prod_cat_dict = category_product_maping)
        else : 
            return redirect(url_for('login'))

    elif request.method == 'POST' : 
        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('login'))

        elif form_name == 'add_to_cart' : 
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
            
    else : 
        return render_template('error.html')


@app.route('/add-category/<admin>', methods = ['GET', 'POST'])
def add_category(admin) : 
    if request.method == 'GET' :
        if session['user'] == admin :
            args = request.args.get('message')
            if args is None : 
                args = ""
            return render_template('add_category.html', admin = admin, message = args)
        else : 
            return redirect(url_for('admin_login')) 
    
    elif request.method == 'POST' : 
        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('admin_login'))

        elif form_name == 'category-form' :
            category_name = request.form['categoryName']

            existing_category = Category.query.filter_by(name = category_name).first()

            print(url_for('add_category', admin = admin))
            if not existing_category : 
                new_category = Category(name = category_name)
                db.session.add(new_category)
                db.session.commit()

                return redirect(url_for('add_category', admin = admin, message = 'category added'))
                
            else : 
                return redirect(url_for('add_category', admin = admin, message = 'category already exists'))
        
    else : 
        return render_template('error.html')


@app.route('/add-product/<admin>', methods = ['GET', 'POST'])
def add_product(admin) : 
    if request.method == 'GET' : 
        if session['user'] == admin :
            category = request.args.get('category')
            return render_template('add_product.html', admin = admin, category = category)
        else : 
            return redirect(url_for('admin_login')) 

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
def buy_product(username) : 
    if request.method == 'GET' : 
        if session['user'] == username : 
            product_name = request.args.get('product-name')
            print(product_name)

            product_details = Product.query.filter_by(name = product_name).first()

            product_quantity = product_details.quantity 

            return render_template(
                'buy_product.html', product_name = product_name, 
                max_limit = product_quantity, product_price = product_details.price, total_price = 0, username = username)
        else : 
            return redirect(url_for('login'))

    elif request.method == 'POST' : 

        form_name = request.form['form_name']
        if form_name == 'logout-form' : 
            session['user'] = None
            return redirect(url_for('login'))

        elif form_name == 'buy-product' : 
            try : 
                product_name = request.args.get('product-name')
                product_details = Product.query.filter_by(name = product_name).first()

                quantity_ordered = request.form['quantity']


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

                old_product = Product.query.filter_by(name = product_name, category = order_category).first()

                print(old_product)
                old_product.quantity -= int(order_quantity)
                print(old_product.quantity)

                db.session.commit()

                return redirect(url_for('product_page', username = username))
            
            except : 
                db.session.rollback()
                return render_template('error.html')

    else : 
        return render_template('error.html')


@app.route('/cart/<username>', methods = ['GET', 'POST'])
def cart_page(username) : 
    if request.method == 'GET' : 
        if session['user'] : 

            all_products = Cart.query.filter_by(username = username).all()

            list_of_items, total_price = [], 0

            for record in all_products : 

                product_details = Product.query.filter_by(name = record.product_name.strip()).first()
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
        else : 
            return redirect(url_for('login'))

    elif request.method == 'POST' :
        
        form_name = request.form['form_name']

        if form_name == 'logout-form' : 
            session['user'] = None 
            return redirect(url_for('login'))

        elif form_name == 'update-quantity' : 
            quantity = request.form['quantity']
            ID = request.form['primary_key']

            old_record = Cart.query.filter_by(cart_id = ID).first()
            old_record.quantity = quantity 

            db.session.commit()

            return redirect(url_for('cart_page', username = username))

        elif form_name == 'buy-all-form' : 

            all_products = Cart.query.filter_by(username = username).all()

            list_of_items, total_price = [], 0

            for record in all_products : 

                product_details = Product.query.filter_by(name = record.product_name.strip()).first()
                
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