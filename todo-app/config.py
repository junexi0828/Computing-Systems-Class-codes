import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://user:password@db:3306/todo_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'

    # JWT 설정
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1시간
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))  # 7일

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}