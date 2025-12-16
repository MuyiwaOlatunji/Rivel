# app/routes/cart.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import current_user
from ..models import CartItem, Product, db

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def view_cart():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        items = CartItem.query.filter_by(session_id=session.get('session_id')).all()
    total = sum(item.product.price * item.quantity for item in items if item.product)
    return render_template('cart.html', items=items, total=total)

@cart.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock < 1:
        return jsonify({'error': 'Out of stock'}), 400

    if current_user.is_authenticated:
        item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    else:
        if 'session_id' not in session:
            session['session_id'] = os.urandom(24).hex()
        item = CartItem.query.filter_by(session_id=session['session_id'], product_id=product_id).first()

    if item:
        if item.quantity + 1 > product.stock:
            return jsonify({'error': 'Not enough stock'}), 400
        item.quantity += 1
    else:
        new_item = CartItem(
            user_id=current_user.id if current_user.is_authenticated else None,
            session_id=session.get('session_id'),
            product_id=product_id,
            quantity=1
        )
        db.session.add(new_item)
    db.session.commit()
    return jsonify({'success': 'Added to cart', 'cart_count': get_cart_count()})

def get_cart_count():
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).count()
    return CartItem.query.filter_by(session_id=session.get('session_id')).count()