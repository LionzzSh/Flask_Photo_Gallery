from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import boto3
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
s3 = None  # Define globally, initialize in create_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = 'Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки.' 
    login_manager.login_message_category = 'error'  
    mail.init_app(app)
    bcrypt.init_app(app)

    # AWS S3 client
    global s3
    s3 = boto3.client(
        's3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=app.config['AWS_SECRET_KEY'],
        region_name=app.config['AWS_REGION']
    )

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import here to avoid circular import
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.gallery import gallery_bp
    from app.routes.folder import folder_bp
    from app.routes.photo import photo_bp
    from app.routes.shares import shares_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(folder_bp)
    app.register_blueprint(photo_bp)
    app.register_blueprint(shares_bp)

    return app