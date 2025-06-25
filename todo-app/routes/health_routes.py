from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """헬스체크 엔드포인트 - 서비스 상태 확인"""
    return jsonify({'status': 'healthy'})