# app/__init__.py — FINAL NO CIRCULAR IMPORT
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'store.db')
    
    app.config['SECRET_KEY'] = 'your-secret-key-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'admin.login'

    from .routes.main import main
    from .routes.admin import admin
    from .routes.cart import cart
    from .routes.payments import payments

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(cart)
    app.register_blueprint(payments)

    with app.app_context():
        db.create_all()
        from .models import User
        if not User.query.filter_by(email='admin@yourstore.com').first():
            hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(email='admin@yourstore.com', password=hashed, is_admin=True, name='Boss')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin created: admin@yourstore.com / admin123")

    return app