# app/routes/payments.py — FINAL WORKING FLUTTERWAVE
from flask import Blueprint, render_template, request, redirect, session, flash
from ..models import Product
import requests
import os
from dotenv import load_dotenv

load_dotenv()

payments = Blueprint('payments', __name__)

@payments.route('/pay', methods=['POST'])
def pay():
    session['user_email'] = request.form['email']  # Store email in session for recommendations
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty')
        return redirect('/cart')

    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            total += product.price * qty

    tx_ref = 'yourstore-' + os.urandom(8).hex()

    payload = {
        "tx_ref": tx_ref,
        "amount": str(total),
        "currency": "GHS",
        "redirect_url": "http://127.0.0.1:5000/payment-success",
        "payment_options": "card, mobilemoneyghana, banktransfer",
        "customer": {
            "email": request.form['email'],
            "phone_number": request.form['phone'],
            "name": request.form.get('name', 'Customer')
        },
        "customizations": {
            "title": "YourStore Ghana",
            "description": "Payment for your order",
            "logo": "https://your-logo.com/logo.png"  # optional
        }
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('FLW_SECRET_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
        data = response.json()
        if data.get('status') == 'success':
            return redirect(data['data']['link'])
        else:
            flash('Payment failed to start. Please try again.')
            return redirect('/checkout')
    except Exception as e:
        flash('Network error. Try again.')
        return redirect('/checkout')

@payments.route('/payment-success')
def payment_success():
    session.pop('cart', None)
    return render_template('payment_success.html')