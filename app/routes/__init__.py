# app/routes/__init__.py
from flask import app
from .main import main
from .admin import admin
from ..routes.cart import cart
from ..routes.payments import payments
app.register_blueprint(main)
app.register_blueprint(cart)
app.register_blueprint(payments)

__all__ = ['main', 'admin']