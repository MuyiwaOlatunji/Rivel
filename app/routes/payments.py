# app/routes/payments.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from ..models import CartItem, Product, Order, db
import requests
import os
from dotenv import load_dotenv

load_dotenv()

payments = Blueprint('payments', __name__)

@payments.route('/checkout')
def checkout():
    items = get_cart_items()
    total = sum(item.product.price * item.quantity for item in items)
    if total == 0:
        return redirect('/cart')
    return render_template('checkout.html', total=total, items=items)

@payments.route('/pay', methods=['POST'])
def pay():
    items = get_cart_items()
    total = sum(item.product.price * item.quantity for item in items)
    email = request.form['email']
    phone = request.form['phone']
    tx_ref = 'yourstore-' + os.urandom(8).hex()

    payload = {
        "tx_ref": tx_ref,
        "amount": total,
        "currency": "GHS",
        "redirect_url": "http://127.0.0.1:5000/payment-callback",
        "payment_options": "card, mobilemoneyghana, banktransfer",
        "customer": {
            "email": email,
            "phone_number": phone,
            "name": request.form.get('name', 'Customer')
        },
        "customizations": {
            "title": "YourStore Payment",
            "description": "Payment for items in cart",
            "logo": "https://your-logo-url.com"
        },
        "meta": {
            "user_id": current_user.id if current_user.is_authenticated else "guest"
        }
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('FLW_SECRET_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
    data = response.json()
    if data['status'] == 'success':
        return redirect(data['data']['link'])
    return jsonify({'error': 'Payment initiation failed'})

@payments.route('/payment-callback')
def payment_callback():
    status = request.args.get('status')
    tx_ref = request.args.get('tx_ref')
    transaction_id = request.args.get('transaction_id')

    if status == 'successful':
        # Verify payment
        headers = {"Authorization": f"Bearer {os.getenv('FLW_SECRET_KEY')}"}
        verify = requests.get(f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify", headers=headers).json()
        if verify['status'] == 'success':
            # Create order, clear cart
            items = get_cart_items()
            total = sum(item.product.price * item.quantity for item in items)
            order = Order(total=total, tx_ref=tx_ref, status='paid', user_id=current_user.id if current_user.is_authenticated else None)
            db.session.add(order)
            # Reduce stock
            for item in items:
                item.product.stock -= item.quantity
                db.session.delete(item)
            db.session.commit()
            return render_template('payment_success.html', order=order)
    return render_template('payment_failed.html')

def get_cart_items():
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).all()
    return CartItem.query.filter_by(session_id=requests.session.get('session_id')).all()