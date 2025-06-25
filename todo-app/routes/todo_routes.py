from flask import Blueprint, request, jsonify
from services.todo_service import TodoService
from middleware.auth_middleware import jwt_required, get_current_user
from exceptions.error_handlers import handle_error
from schemas.todo_schemas import (
    TodoCreateSchema, TodoUpdateSchema, TodoResponseSchema,
    TodoListResponseSchema, TodoFilterSchema
)
from marshmallow import ValidationError

todo_bp = Blueprint('todos', __name__)

# 스키마 인스턴스 생성
todo_create_schema = TodoCreateSchema()
todo_update_schema = TodoUpdateSchema()
todo_response_schema = TodoResponseSchema()
todo_list_response_schema = TodoListResponseSchema()
todo_filter_schema = TodoFilterSchema()

@todo_bp.route('/todos', methods=['GET'])
@jwt_required
@handle_error
def get_todos():
    user = get_current_user()

    # 필터 파라미터 검증
    try:
        filters = todo_filter_schema.load(request.args)
    except ValidationError as err:
        return jsonify({'error': '필터 파라미터 오류', 'details': err.messages}), 400

    todos = TodoService.get_all_todos(filters, user.id)

    # 응답 스키마 적용
    response_data = {
        'todos': [todo.to_dict() for todo in todos],
        'total': len(todos),
        'page': filters.get('page', 1),
        'per_page': filters.get('per_page', 20)
    }

    return jsonify(response_data)

@todo_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required
@handle_error
def get_todo(todo_id):
    user = get_current_user()
    todo = TodoService.get_todo_by_id(todo_id, user.id)
    return jsonify(todo.to_dict())

@todo_bp.route('/todos', methods=['POST'])
@jwt_required
@handle_error
def create_todo():
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    # 요청 데이터 검증
    try:
        validated_data = todo_create_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': '데이터 검증 오류', 'details': err.messages}), 400

    todo = TodoService.create_todo(validated_data, user.id)
    return jsonify(todo.to_dict()), 201

@todo_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required
@handle_error
def update_todo(todo_id):
    user = get_current_user()
    data = request.get_json()

    if not data:
        return jsonify({'error': '수정할 데이터가 없습니다'}), 400

    # 요청 데이터 검증
    try:
        validated_data = todo_update_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': '데이터 검증 오류', 'details': err.messages}), 400

    todo = TodoService.update_todo(todo_id, validated_data, user.id)
    return jsonify(todo.to_dict())

@todo_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required
@handle_error
def delete_todo(todo_id):
    user = get_current_user()
    TodoService.delete_todo(todo_id, user.id)
    return '', 204

@todo_bp.route('/todos/<int:todo_id>/complete', methods=['PATCH'])
@jwt_required
@handle_error
def toggle_complete(todo_id):
    user = get_current_user()
    todo = TodoService.toggle_complete(todo_id, user.id)
    return jsonify(todo.to_dict())

@todo_bp.route('/todos/statistics', methods=['GET'])
@jwt_required
@handle_error
def get_statistics():
    user = get_current_user()
    stats = TodoService.get_statistics(user.id)
    return jsonify(stats)