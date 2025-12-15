# app/routes/admin.py  ← CORRECT VERSION
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Product, db
from .. import bcrypt
import cloudinary.uploader

admin = Blueprint('admin', __name__)

# THESE ARE THE CORRECT ROUTES
@admin.route('/login', methods=['GET', 'POST'])          # → /admin/login
def login():
    if current_user.is_authenticated:
        return redirect('/admin/dashboard')
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/admin/dashboard')
        flash('Invalid email or password', 'danger')
    return render_template('admin_login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@admin.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect('/')
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@admin.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect('/')
    if request.method == 'POST':
        file = request.files['image']
        upload_result = cloudinary.uploader.upload(file)
        product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            image=upload_result['secure_url'],
            category=request.form['category'],
            subcategory=request.form['subcategory'] or None,
            description=request.form.get('description')
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect('/admin/dashboard')
    return render_template('admin_add.html')