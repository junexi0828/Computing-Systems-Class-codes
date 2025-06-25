from flask import Blueprint, request, jsonify
from services.tag_service import TagService
from middleware.auth_middleware import jwt_required, get_current_user
from exceptions.error_handlers import handle_error

tag_bp = Blueprint('tags', __name__)

@tag_bp.route('/tags', methods=['GET'])
@jwt_required
@handle_error
def get_tags():
    """사용자의 모든 태그 조회"""
    user = get_current_user()
    tags = TagService.get_user_tags(user.id)
    return jsonify([tag.to_dict() for tag in tags])

@tag_bp.route('/tags', methods=['POST'])
@jwt_required
@handle_error
def create_tag():
    """태그 생성"""
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    try:
        tag = TagService.create_tag(user.id, data)
        return jsonify({
            'message': '태그가 생성되었습니다',
            'tag': tag.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({'error': '태그 생성 실패', 'message': str(e)}), 400

@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@jwt_required
@handle_error
def update_tag(tag_id):
    """태그 수정"""
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '수정할 데이터가 없습니다'}), 400

    try:
        tag = TagService.update_tag(tag_id, user.id, data)
        return jsonify({
            'message': '태그가 수정되었습니다',
            'tag': tag.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({'error': '태그 수정 실패', 'message': str(e)}), 400

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required
@handle_error
def delete_tag(tag_id):
    """태그 삭제"""
    user = get_current_user()

    try:
        tag = TagService.delete_tag(tag_id, user.id)
        return jsonify({
            'message': '태그가 삭제되었습니다',
            'tag': tag.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({'error': '태그 삭제 실패', 'message': str(e)}), 400

@tag_bp.route('/todos/<int:todo_id>/tags', methods=['POST'])
@jwt_required
@handle_error
def add_tag_to_todo(todo_id):
    """할 일에 태그 추가"""
    user = get_current_user()
    data = request.get_json()

    if not data or 'tag_id' not in data:
        return jsonify({'error': '태그 ID가 필요합니다'}), 400

    try:
        todo_tag = TagService.add_tag_to_todo(todo_id, data['tag_id'], user.id)
        return jsonify({
            'message': '태그가 할 일에 추가되었습니다',
            'todo_tag': todo_tag.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({'error': '태그 추가 실패', 'message': str(e)}), 400

@tag_bp.route('/todos/<int:todo_id>/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required
@handle_error
def remove_tag_from_todo(todo_id, tag_id):
    """할 일에서 태그 제거"""
    user = get_current_user()

    try:
        todo_tag = TagService.remove_tag_from_todo(todo_id, tag_id, user.id)
        return jsonify({
            'message': '태그가 할 일에서 제거되었습니다',
            'todo_tag': todo_tag.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({'error': '태그 제거 실패', 'message': str(e)}), 400

@tag_bp.route('/tags/<int:tag_id>/todos', methods=['GET'])
@jwt_required
@handle_error
def get_todos_by_tag(tag_id):
    """특정 태그가 연결된 할 일 목록 조회"""
    user = get_current_user()

    try:
        todos = TagService.get_todos_by_tag(tag_id, user.id)
        return jsonify([todo.to_dict() for todo in todos]), 200

    except ValueError as e:
        return jsonify({'error': '할 일 조회 실패', 'message': str(e)}), 400

@tag_bp.route('/todos/<int:todo_id>/tags', methods=['GET'])
@jwt_required
@handle_error
def get_tags_by_todo(todo_id):
    """특정 할 일에 연결된 태그 목록 조회"""
    user = get_current_user()

    try:
        tags = TagService.get_tags_by_todo(todo_id, user.id)
        return jsonify([tag.to_dict_simple() for tag in tags]), 200

    except ValueError as e:
        return jsonify({'error': '태그 조회 실패', 'message': str(e)}), 400