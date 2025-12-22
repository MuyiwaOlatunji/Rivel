# app/models.py — FINAL CORRECT VERSION
from flask_login import UserMixin
from . import db  # <-- Import db from app/__init__.py
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(100))
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ViewHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)