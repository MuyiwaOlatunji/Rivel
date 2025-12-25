# app/__init__.py — FINAL WITH AUTHLIB GOOGLE LOGIN + GEMINI CHAT (WORKING)
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
import os
import requests
import secrets

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
oauth = OAuth()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'store.db')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'admin.login'
    # Google OAuth with Authlib (FIXED NONCE + SMOOTH LOGIN)
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        authorize_params={
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'select_account'  # Shows account selector, no password if logged in
        },
        access_token_url='https://oauth2.googleapis.com/token',
        client_kwargs={'token_endpoint_auth_method': 'client_secret_basic'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )

    @app.route('/login/google')
    def login_google():
        # Generate nonce for security
        nonce = secrets.token_urlsafe(16)
        session['google_nonce'] = nonce
        
        redirect_uri = url_for('google_authorized', _external=True)
        return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

    @app.route('/login/google/authorized')
    def google_authorized():
        try:
            # Retrieve nonce from session
            nonce = session.pop('google_nonce', None)
            
            token = oauth.google.authorize_access_token()
            if token and 'id_token' in token:
                user_info = oauth.google.parse_id_token(token, nonce=nonce)
                session['user_email'] = user_info['email']
                print("Google login success:", user_info['email'])
            return redirect('/')
        except Exception as e:
            print("Google login error:", e)
            return 'Login failed. Try again.', 400
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        user_query = request.json.get('query')
        user_email = session.get('user_email', 'guest')
        
        payload = {
            "model": "gemma2:2b",  # or "llama3.1"
            "prompt": f"You are RIVEL AI, a friendly Ghanaian assistant for RIVEL e-commerce. User email: {user_email}. Be helpful, recommend products, and end with a question. Knowledge: Fashion, Electronics, Kids, Beauty. Shipping: 2-3 days nationwide, free over GHS 500. Payment: MoMo, Card, Bank Transfer.\n\nUser: {user_query}\nAssistant:",
            "stream": False
        }
        
        try:
            response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=60)
            if response.status_code == 404:
                return jsonify({'response': 'Ollama server not ready or model not loaded. Run "ollama serve" and "ollama pull gemma2:2b".'})
            response.raise_for_status()
            data = response.json()
            ai_response = data.get('response', 'No response')
            return jsonify({'response': ai_response.strip()})
        except Exception as e:
            print(f"Ollama error: {e}")
            return jsonify({'response': 'Sorry boss, my AI brain is warming up. Try again in a minute!'})

    # Register Blueprints
    from .routes.main import main
    from .routes.admin import admin
    from .routes.cart import cart
    from .routes.payments import payments

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(cart)
    app.register_blueprint(payments)

    # Create DB and admin
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