import numpy as np
from application.data.database import db
from application.data.models import User, Admin, Category, Product, Order, Cart, Offers
import logging 

logger1 = logging.getLogger('file1')
logger1.setLevel(logging.DEBUG)

file_handler1 = logging.FileHandler('logs/discount.log')
file_handler1.setLevel(logging.DEBUG) 

formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler1.setFormatter(formatter)

logger1.addHandler(file_handler1)

class Discount :
    def find_discount_product(self) : 
        """
        if a product quantity is greater than avg product quantity in the category then give discount 
            * <5% more --> 5% discount
            * <25% more --> 10% discount
            * <50% more --> 15% discount
            * else 25% discount
        """
        all_product = Product.query.all()
        category_quantity = {}
        for product in all_product :
            if product.category not in category_quantity : 
                category_quantity[product.category] = [product.quantity]
            else :
                category_quantity[product.category].append(product.quantity)

        catgory_avg = {}
        for category in category_quantity :
            catgory_avg[category] = np.mean(category_quantity[category])

        product_discount = {}
        for product in all_product : 
            if product.quantity > catgory_avg[product.category] : 
                if ((product.quantity - catgory_avg[product.category])/catgory_avg[product.category])*100 <= 5 : 
                    product_discount[product.name] = {
                        'category' : product.category, 
                        'discount' : 5
                    }
                elif ((product.quantity - catgory_avg[product.category])/catgory_avg[product.category])*100 <= 25 : 
                    product_discount[product.name] = {
                        'category' : product.category, 
                        'discount' : 10
                    }
                elif ((product.quantity - catgory_avg[product.category])/catgory_avg[product.category])*100 <= 50 : 
                    product_discount[product.name] = {
                        'category' : product.category, 
                        'discount' : 15
                    }
                else : 
                    product_discount[product.name] = {
                        'category' : product.category, 
                        'discount' : 25
                    }

        return product_discount

    def ingest_in_database(self) : 
        # each_category can have 1 product for offer  
        discount_product = self.find_discount_product()
        new_discount_category = []
        for product in discount_product : 
            if discount_product[product]['category'] not in new_discount_category : 
                new_discount_category.append(discount_product[product]['category']) 

        logger1.info('filtered products for discount' + str(discount_product))
        inserted_category = []
        for product in discount_product : 
            if discount_product[product]['category'] not in inserted_category :
                existing_offer = Offers.query.filter_by(product_name = product).first()
                if not existing_offer : 
                    new_offer = Offers(
                        product_name = product, 
                        category_name = discount_product[product]['category'], 
                        discount = discount_product[product]['discount']
                    )
                    logger1.info('product name --> ', product, 'discount --> ',discount_product[product]['discount'])
                    old_product = Product.query.filter_by(name = product).first()
                    old_product.price = int(old_product.price * (100 - discount_product[product]['discount'])/100)
                    
                    Offers.query.filter_by(category_name = discount_product[product]['category']).delete()
                    
                    db.session.add(new_offer)
                    db.session.add(old_product)
                    inserted_category.append(discount_product[product]['category'])
                else : 
                    inserted_category.append(discount_product[product]['category'])
                

        db.session.commit()