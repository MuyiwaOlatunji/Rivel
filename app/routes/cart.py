# app/routes/cart.py
from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from ..models import Product, CartItem, db
import os

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def view_cart():
    # For now, simple guest cart using session
    cart_items = []  # We'll expand this later
    total = 0
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock < 1:
        return jsonify({'status': 'error', 'message': 'Out of stock'})
    
    # Simple session cart for now
    session_cart = request.session.get('cart', {})
    session_cart[str(product_id)] = session_cart.get(str(product_id), 0) + 1
    request.session['cart'] = session_cart

    return jsonify({'status': 'success', 'message': 'Added to cart!', 'cart_count': len(session_cart)})