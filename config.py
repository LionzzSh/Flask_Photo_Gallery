
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SENDER_EMAIL') 
    MAIL_PASSWORD = os.environ.get('GOOGLE_APP_PASSWORD') 
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY') or 'AKIAQ4NSBOVJCJPR5PE4'
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY') or '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'
    AWS_BUCKET_NAME = 'lionzzgallery'
    AWS_REGION = 'eu-north-1'
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')