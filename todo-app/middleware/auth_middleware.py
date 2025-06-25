from functools import wraps
from flask import request, jsonify, g
from services.auth_service import AuthService

def jwt_required(f):
    """JWT 토큰이 필요한 엔드포인트를 위한 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({
                    'error': '인증 토큰이 올바르지 않습니다',
                    'message': 'Authorization 헤더 형식: Bearer <token>'
                }), 401

        if not token:
            return jsonify({
                'error': '인증 토큰이 필요합니다',
                'message': 'Authorization 헤더에 Bearer 토큰을 포함해주세요'
            }), 401

        try:
            # 토큰 검증
            payload = AuthService.verify_token(token)

            # 토큰 타입 확인
            if payload.get('type') != 'access':
                return jsonify({
                    'error': '유효하지 않은 토큰입니다',
                    'message': '액세스 토큰이 아닙니다'
                }), 401

            # 사용자 조회
            user = AuthService.get_user_by_id(payload['user_id'])
            if not user:
                return jsonify({
                    'error': '사용자를 찾을 수 없습니다',
                    'message': '토큰에 해당하는 사용자가 존재하지 않습니다'
                }), 401

            # 전역 변수에 사용자 정보 저장
            g.current_user = user

            return f(*args, **kwargs)

        except ValueError as e:
            return jsonify({
                'error': '인증 실패',
                'message': str(e)
            }), 401
        except Exception as e:
            return jsonify({
                'error': '토큰 검증 중 오류가 발생했습니다',
                'message': str(e)
            }), 500

    return decorated_function

def optional_jwt(f):
    """JWT 토큰이 선택적인 엔드포인트를 위한 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                pass

        if token:
            try:
                # 토큰 검증
                payload = AuthService.verify_token(token)

                if payload.get('type') == 'access':
                    # 사용자 조회
                    user = AuthService.get_user_by_id(payload['user_id'])
                    if user:
                        g.current_user = user

            except (ValueError, Exception):
                # 토큰이 유효하지 않아도 계속 진행
                pass

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    """관리자 권한이 필요한 엔드포인트를 위한 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 먼저 JWT 인증 확인
        if not hasattr(g, 'current_user'):
            return jsonify({
                'error': '인증이 필요합니다',
                'message': '로그인이 필요합니다'
            }), 401

        # 관리자 권한 확인
        if g.current_user.role != 'admin':
            return jsonify({
                'error': '권한이 없습니다',
                'message': '관리자 권한이 필요합니다'
            }), 403

        return f(*args, **kwargs)

    return decorated_function

def get_current_user():
    """현재 인증된 사용자 반환"""
    return getattr(g, 'current_user', None)

def require_current_user():
    """현재 사용자가 없으면 401 에러 반환"""
    user = get_current_user()
    if not user:
        return jsonify({
            'error': '인증이 필요합니다',
            'message': '로그인이 필요합니다'
        }), 401
    return user