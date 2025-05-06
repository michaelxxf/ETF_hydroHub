from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.routes import customer_routes


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    CSRFProtect(app)
    
    
    app.register_blueprint(customer_routes)

    
    return app