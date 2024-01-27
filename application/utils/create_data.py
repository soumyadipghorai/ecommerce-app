import pandas as pd 
from application.data.models import Order

def create_data() : 
    output = []
    all_orders = Order.query.all()
    for order in all_orders : 
        output.append([
            order.order_id, order.username, order.category, 
            order.product_name,order.price, order.quantity,             
            order.date, order.total_price
            ])

    data = pd.DataFrame(output, columns = [
        'order_id', 'username', 'category', 'product_name', 
        'price', 'quantity', 'order_date', 'total_price'
    ])

    data.to_csv('static/data/order_data.csv', encoding = 'utf-8', index = False)