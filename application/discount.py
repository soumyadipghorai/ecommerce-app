import numpy as np
from application.models import User, Admin, Category, Product, Order, Cart, Offers


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
                    product_discount[product.name] = 5
                elif ((product.quantity - catgory_avg[product.category])/catgory_avg[product.category])*100 <= 25 : 
                    product_discount[product.name] = 10
                elif ((product.quantity - catgory_avg[product.category])/catgory_avg[product.category])*100 <= 50 : 
                    product_discount[product.name] = 15
                else : 
                    product_discount[product.name] = 25

        return product_discount

    def ingest_in_database(self, product_discount_dict: dict) : 
        all_offer 