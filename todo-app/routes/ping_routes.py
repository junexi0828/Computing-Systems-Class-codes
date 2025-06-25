from flask import Blueprint, jsonify

ping_bp = Blueprint('ping', __name__)

@ping_bp.route('/ping')
def ping():
    """Ping 엔드포인트 - 서비스 상태 확인"""
    return jsonify({'message': 'pong'})