from flask import Flask, jsonify
from flask_cors import CORS
from extensions import init_extensions, db
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
from routes.tag_routes import tag_bp
from models.user import User
from models.todo import Todo
from models.tag import Tag

def create_app(db_uri=None):
    """Flask 앱 팩토리 함수"""
    app = Flask(__name__)

    # 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'mysql://user:password@db:3306/todo_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1시간
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800  # 7일

    # 확장 초기화
    init_extensions(app)

    # CORS 설정 - 프론트엔드 개발 서버 허용
    CORS(app,
         origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])

    # 블루프린트 등록
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todo_bp, url_prefix='/api/todos')
    app.register_blueprint(tag_bp, url_prefix='/api/tags')

    # 기본 라우트
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Todo App API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'todos': '/api/todos',
                'tags': '/api/tags',
                'health': '/health',
                'ping': '/ping'
            }
        })

    @app.route('/ping')
    def ping():
        return jsonify({'message': 'pong'})

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})

    return app

# gunicorn을 위한 앱 인스턴스 생성
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)