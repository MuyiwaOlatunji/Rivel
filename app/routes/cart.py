# app/routes/cart.py
from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from flask_login import current_user
from ..models import Product, db
import os

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            items.append({'product': product, 'quantity': qty})
            total += product.price * qty
    return render_template('cart.html', items=items, total=total)

@cart.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock < 1:
        return jsonify({'success': False, 'message': 'Out of stock'})
    
    cart = session.get('cart', {})
    current_qty = cart.get(str(product_id), 0)
    if current_qty + 1 > product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock'})
    
    cart[str(product_id)] = current_qty + 1
    session['cart'] = cart
    
    return jsonify({
        'success': True, 
        'message': 'Added to cart!',
        'cart_count': len(cart),
        'total_items': sum(cart.values())
    })

@cart.route('/cart-count')
def cart_count():
    cart = session.get('cart', {})
    count = sum(cart.values())
    return jsonify({'count': count})

@cart.route('/clear-cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return '', 204

@cart.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            items.append({'product': product, 'quantity': qty})
            total += product.price * qty
    if total == 0:
        return redirect('/cart')
    return render_template('checkout.html', items=items, total=total)