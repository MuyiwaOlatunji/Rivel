# app/routes/payments.py
from flask import Blueprint

payments = Blueprint('payments', __name__)

@payments.route('/payment-success')
def success():
    return "<h1>Payment Successful! Thank you for shopping with YourStore</h1>"

@payments.route('/payment-cancel')
def cancel():
    return "<h1>Payment Cancelled</h1>"