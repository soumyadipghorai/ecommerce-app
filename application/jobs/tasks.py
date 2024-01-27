from application.controller.workers import celery
from datetime import datetime, date
from celery.schedules import crontab

from application.data.models import Order, User, UserRole
from application.messages.mailman import send_daily_email, send_monthy_report
from sqlalchemy import extract
from application.utils.create_data import create_data

import calendar

@celery.task(name="just_say_hello")
def just_say_hello(name) : 
    print('INSIDE TAKS')
    print("hello {}".format(name))

    return "hello {}".format(name)


@celery.task(name="print_current_time")
def print_current_time() : 
    print('START')
    now = datetime.now()
    print("now in task = ", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time = ", dt_string)
    print('COMPLETE')

    send_daily_email(
        receiver_email = "backup.soumyadipghorai@gmail.com", 
        subject ="random  text", 
        message = "random message", 
        content_type = "text"
    )

    print("message sent")

    return str(dt_string)

@celery.task(name="hello_world")
def hello_world(name) : 
    print("hello {}".format(name))

@celery.on_after_finalize.connect 
def setup_daily_reminder(sender, **kwargs) :
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    sender.add_periodic_task(
        crontab(hour=23, minute=34), send_email_checker.s(), 
        name = f'sending mail to the customers who has not made any transactions today --> {dt_string}'
    )

    sender.add_periodic_task(
        crontab(hour=23, minute=59, day_of_month='last'), monthly_report_sender_job.s(), 
        name = f'sending mail to the admins at the end of the month --> {dt_string}'
    )

    # sender.add_periodic_task(30.0, send_email_checker.s(), name = f'sending email at every 30secs {dt_string}')

@celery.task(name="send_email_checker")
def send_email_checker() : 

    today = date.today()
    today_order = Order.query.filter_by(date=today).all()

    today_customer = set()
    for order in today_order : 
        today_customer.add(int(order.username))

    all_customer = []
    all_customer_db = User.query.all()

    for customer in all_customer_db : 
        all_customer.append(int(customer.id))

    for id in all_customer : 
        if id not in today_customer : 
            customer_email = User.query.filter_by(id=id).first()

            send_daily_email(
                receiver_email = customer_email.email, 
                subject ="Reminder: Visit the Grocery Store Today", 
                message = f"""
                    Dear {customer_email.username}
                    We hope this email finds you well. We noticed that you haven't visited our grocery store today.
                    Don't miss out on the latest deals and fresh products. Visit us today and enjoy a great shopping experience!
                    Thank you for choosing our store.
                    Best regards,
                    Your Grocery Store Team
                    Today's Date: {today}
                """
            )

            print("message sent to ", customer_email.id)

    return "message sent"

@celery.task(name="monthly_report_sender_job")
def monthly_report_sender_job() : 
    all_order = Order.query.filter(extract('month', Order.date) == date.today().month).all()

    total_sales, total_quantity, unique_user = 0, 0, set()
    for order in all_order :  
        total_sales += order.total_price
        total_quantity += order.quantity
        if order.username not in unique_user :
            unique_user.add(order.username)

    day_active = len(all_order)
    total_unique_user = len(unique_user)

    month_name = calendar.month_name[date.today().month]

    html_content = f"""
    <html>
        <body>
            <h2>Monthly Report - {month_name}</h2>
            <p>Dear Manager,</p>
            <p>Here is the monthly report for {month_name}:</p>
            
            <ul>
                <li>Total Sales: ${total_sales}</li>
                <li>Total Quantity: {total_quantity}</li>
                <li>Days Active: {day_active}</li>
                <li>Total Unique Users: {total_unique_user}</li>
            </ul>
            
            <p>Thank you for your attention.</p>
            <p>Best regards,<br>Grocery Store</p>
        </body>
    </html>
    """
    all_user = UserRole.query.all()
    all_admin = []

    for user in all_user :
        if user.role_id == 2 : 
            all_admin.append(int(user.user_id))

    print(all_admin) 

    for admin in all_admin : 
        admin_email = User.query.filter_by(id = admin).first().email 
        send_monthy_report(
            receiver_email = admin_email, 
            subject ="Monthly report from grocery store", 
            message = html_content
        )

        print("message sent to ", admin_email)

@celery.task(name="create_summary_data_job")
def create_summary_data_job() :
    create_data() 
    print("summary data generated")
    return "success"


################################## testing section #################################
@celery.task(name="test_send_email")
def test_send_email() :
    today = date.today()
    send_daily_email(
        receiver_email = "backup.soumyadipghorai@gmail.com", 
        subject ="Reminder: Visit the Grocery Store Today", 
        message = f"""
            Dear ghorai
            We hope this email finds you well. We noticed that you haven't visited our grocery store today.
            Don't miss out on the latest deals and fresh products. Visit us today and enjoy a great shopping experience!
            Thank you for choosing our store.
            Best regards,
            Your Grocery Store Team
            Today's Date: {today}
        """
    )

    print("testing email sent")

    return "message sent"

@celery.task(name="test_html_report_sender")
def test_html_report_sender() : 
    all_order = Order.query.filter(extract('month', Order.date) == date.today().month).all()

    total_sales, total_quantity, unique_user = 0, 0, set()
    for order in all_order :  
        total_sales += order.total_price
        total_quantity += order.quantity
        if order.username not in unique_user :
            unique_user.add(order.username)

    day_active = len(all_order)
    total_unique_user = len(unique_user)

    month_name = calendar.month_name[date.today().month]

    html_content = f"""
    <html>
        <body>
            <h2>Monthly Report - {month_name}</h2>
            <p>Dear Manager,</p>
            <p>Here is the monthly report for {month_name}:</p>
            
            <ul>
                <li>Total Sales: ${total_sales}</li>
                <li>Total Quantity: {total_quantity}</li>
                <li>Days Active: {day_active}</li>
                <li>Total Unique Users: {total_unique_user}</li>
            </ul>
            
            <p>Thank you for your attention.</p>
            <p>Best regards,<br>Grocery Store</p>
        </body>
    </html>
    """

    send_monthy_report(
        receiver_email = "backup.soumyadipghorai@gmail.com", 
        subject ="Monthly report from grocery store", 
        message = html_content
    )

    print("report sent")
    return "report sent"