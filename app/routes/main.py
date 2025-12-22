# app/routes/main.py — FINAL WITH STYLE SCOUTS RECOMMENDATIONS
from flask import Blueprint, render_template, session
from ..models import Product, ViewHistory, db  # <-- All imports fixed

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get user email from session (set during checkout or login)
    user_email = session.get('user_email')

    recommended = []
    if user_email:
        # Find most viewed category by this email
        most_viewed_category = db.session.query(Product.category)\
            .join(ViewHistory, ViewHistory.product_id == Product.id)\
            .filter(ViewHistory.email == user_email)\
            .group_by(Product.category)\
            .order_by(db.func.count(Product.id).desc())\
            .first()
        
        if most_viewed_category:
            recommended = Product.query.filter_by(
                category=most_viewed_category[0], 
                active=True
            ).limit(8).all()

    # Fallback: newest products
    if not recommended:
        recommended = Product.query.filter_by(active=True)\
            .order_by(Product.created_at.desc())\
            .limit(8).all()

    # Regular featured products
    featured = Product.query.filter_by(active=True).limit(12).all()

    return render_template(
        'index.html', 
        recommended=recommended, 
        featured=featured
    )

# Track views in category pages
def track_views(products, email):
    if email:
        for product in products:
            view = ViewHistory(email=email, product_id=product.id)
            db.session.add(view)
        db.session.commit()

@main.route('/shop')
def shop():
    products = Product.query.filter_by(active=True).all()
    track_views(products, session.get('user_email'))
    return render_template('shop.html', products=products)

@main.route('/women')
def women():
    products = Product.query.filter_by(category='women', active=True).all()
    track_views(products, session.get('user_email'))
    return render_template('women.html', products=products)

@main.route('/men')
def men():
    products = Product.query.filter_by(category='men', active=True).all()
    track_views(products, session.get('user_email'))
    return render_template('men.html', products=products)

@main.route('/kids')
def kids():
    products = Product.query.filter_by(category='kids', active=True).all()
    track_views(products, session.get('user_email'))
    return render_template('kids.html', products=products)

@main.route('/electronics')
def electronics():
    products = Product.query.filter_by(category='electronics', active=True).all()
    track_views(products, session.get('user_email'))
    return render_template('electronics.html', products=products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Track view for recommendations
    user_email = session.get('user_email')
    if user_email:
        view = ViewHistory(email=user_email, product_id=product.id)
        db.session.add(view)
        db.session.commit()
    
    # Related products (same category)
    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.active == True
    ).limit(4).all()
    
    return render_template('product_detail.html', product=product, related=related)

@main.route('/sitemap.xml')
def sitemap():
    products = Product.query.filter_by(active=True).all()
    from flask import make_response
    xml = render_template('sitemap.xml', products=products)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response