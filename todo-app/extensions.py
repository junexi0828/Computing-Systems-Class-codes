from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Flask 확장 인스턴스들
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def init_extensions(app):
    """Flask 확장들을 초기화"""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)