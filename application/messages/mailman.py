import smtplib 
from email.message import EmailMessage
from email import encoders 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 


SENDER_EMAIL = "ghorai.soumyadip33@gmail.com"
SMTP_SERVER_HOST = "localhost" 
SMTP_SERVER_PORT = 8080 
SENDER_PASSWORD = "styq txns fyrp ftez"

def send_daily_email(receiver_email, subject, message) : 
    msg = MIMEMultipart()
    msg["from"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["subject"] = subject

    msg.attach(MIMEText(message, "plain"))
 
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Replace with your email and password
        server.send_message(msg)
        server.close() 

    return True

def send_monthy_report(receiver_email, subject, message) : 
    msg = MIMEMultipart()
    msg["from"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["subject"] = subject

    msg.attach(MIMEText(message, "html"))
 
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Replace with your email and password
        server.send_message(msg)
        server.close() 

    return True