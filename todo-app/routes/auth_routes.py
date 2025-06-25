from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from middleware.auth_middleware import jwt_required, get_current_user
from exceptions.error_handlers import handle_error
from datetime import datetime
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@handle_error
def register():
    """사용자 회원가입"""
    data = request.get_json()

    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    try:
        user = AuthService.register_user(data)
        return jsonify({
            'message': '회원가입이 완료되었습니다',
            'user': user.to_dict_safe()
        }), 201

    except ValueError as e:
        return jsonify({'error': '회원가입 실패', 'message': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
@handle_error
def login():
    """사용자 로그인"""
    data = request.get_json()

    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '사용자명과 비밀번호를 입력해주세요'}), 400

    try:
        user = AuthService.authenticate_user(username, password)
        access_token, refresh_token = AuthService.generate_tokens(user.id)

        return jsonify({
            'message': '로그인이 완료되었습니다',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict_safe()
        }), 200

    except ValueError as e:
        return jsonify({'error': '로그인 실패', 'message': str(e)}), 401

@auth_bp.route('/refresh', methods=['POST'])
@handle_error
def refresh_token():
    """액세스 토큰 갱신"""
    data = request.get_json()

    if not data or not data.get('refresh_token'):
        return jsonify({'error': '리프레시 토큰이 필요합니다'}), 400

    try:
        access_token, user = AuthService.refresh_access_token(data['refresh_token'])

        return jsonify({
            'message': '토큰이 갱신되었습니다',
            'access_token': access_token,
            'user': user.to_dict_safe()
        }), 200

    except ValueError as e:
        return jsonify({'error': '토큰 갱신 실패', 'message': str(e)}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
@handle_error
def get_profile():
    """현재 사용자 프로필 조회"""
    user = get_current_user()
    return jsonify({
        'user': user.to_dict_safe()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
@handle_error
def update_profile():
    """현재 사용자 프로필 수정"""
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '수정할 데이터가 없습니다'}), 400

    # 수정 가능한 필드들
    allowed_fields = ['full_name', 'avatar_url']

    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])

    user.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({
            'message': '프로필이 수정되었습니다',
            'user': user.to_dict_safe()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '프로필 수정 실패', 'message': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required
@handle_error
def change_password():
    """비밀번호 변경"""
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': '현재 비밀번호와 새 비밀번호를 입력해주세요'}), 400

    # 새 비밀번호 길이 검증
    if len(new_password) < 6:
        return jsonify({'error': '새 비밀번호는 최소 6자 이상이어야 합니다'}), 400

    # 현재 비밀번호 검증
    if not AuthService.verify_password(current_password, user.password_hash):
        return jsonify({'error': '현재 비밀번호가 일치하지 않습니다'}), 400

    # 새 비밀번호 해시화
    new_password_hash = AuthService.hash_password(new_password)
    user.password_hash = new_password_hash
    user.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({'message': '비밀번호가 변경되었습니다'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '비밀번호 변경 실패', 'message': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
@handle_error
def logout():
    """로그아웃 (클라이언트에서 토큰 삭제)"""
    return jsonify({'message': '로그아웃되었습니다'}), 200