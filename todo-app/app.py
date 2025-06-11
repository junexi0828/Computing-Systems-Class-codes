from flask import Flask, render_template
from models.todo import db
from routes.todo_routes import bp as todo_bp
from config import config
from exceptions.error_handlers import register_error_handlers

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # 블루프린트 등록
    app.register_blueprint(todo_bp)
    
    register_error_handlers(app)
    
    @app.route('/health')
    def health():
        return 'ok', 200
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0') 