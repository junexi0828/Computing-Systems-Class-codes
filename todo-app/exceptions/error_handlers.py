from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

def handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            return jsonify({
                'error': '데이터베이스 오류가 발생했습니다',
                'message': str(e)
            }), 500
        except HTTPException as e:
            return jsonify({
                'error': e.name,
                'message': e.description
            }), e.code
        except Exception as e:
            return jsonify({
                'error': '서버 오류가 발생했습니다',
                'message': str(e)
            }), 500
    return decorated_function 