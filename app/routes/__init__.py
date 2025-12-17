# app/routes/__init__.py  ← CORRECT — ONLY EXPORTS BLUEPRINTS
# DO NOT register blueprints here!

from .main import main
from .admin import admin
# from .cart import cart  # add later when you create it
# from .payments import payments  # add later

__all__ = ['main', 'admin']