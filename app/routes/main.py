# app/routes/main.py
from flask import Blueprint, render_template
from ..models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.filter_by(active=True).limit(12).all()
    return render_template('index.html', products=products)

@main.route('/shop')
def shop():
    products = Product.query.filter_by(active=True).all()
    return render_template('shop.html', products=products)

@main.route('/women')
def women():
    products = Product.query.filter_by(category='women', active=True).all()
    return render_template('women.html', products=products)

@main.route('/men')
def men():
    products = Product.query.filter_by(category='men', active=True).all()
    return render_template('men.html', products=products)

@main.route('/kids')
def kids():
    products = Product.query.filter_by(category='kids', active=True).all()
    return render_template('kids.html', products=products)

@main.route('/electronics')
def electronics():
    products = Product.query.filter_by(category='electronics', active=True).all()
    return render_template('electronics.html', products=products)