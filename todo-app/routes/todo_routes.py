from flask import Blueprint, request, jsonify
from services.todo_service import *
from models.todo import db
from datetime import datetime

bp = Blueprint('todos', __name__)

@bp.route('/todos', methods=['GET'])
def get_todos():
    todos = get_all_todos()
    return jsonify([todo.to_dict() for todo in todos])

@bp.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = get_todo_by_id(id)
    return jsonify(todo.to_dict())

@bp.route('/todos', methods=['POST'])
def create():
    data = request.get_json()
    # 입력 유효성 검증
    if not data.get('title'):
        return jsonify({'error': '제목은 필수입니다.'}), 400
    todo = create_todo(data)
    return jsonify(todo.to_dict()), 201

@bp.route('/todos/<int:id>', methods=['PUT'])
def update(id):
    todo = get_todo_by_id(id)
    data = request.get_json()
    todo = update_todo(todo, data)
    return jsonify(todo.to_dict())

@bp.route('/todos/<int:id>', methods=['DELETE'])
def delete(id):
    todo = get_todo_by_id(id)
    delete_todo(todo)
    return '', 204

@bp.route('/todos/<int:id>/complete', methods=['PATCH'])
def toggle_complete(id):
    todo = get_todo_by_id(id)
    todo.is_completed = not todo.is_completed
    db.session.commit()
    return jsonify(todo.to_dict()) 