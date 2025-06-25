from datetime import datetime
from sqlalchemy import or_
from models.todo import Todo, db
from middleware.auth_middleware import get_current_user

class TodoService:
    @staticmethod
    def get_all_todos(filters=None, user_id=None):
        query = Todo.query

        # 사용자별 필터링 (인증된 사용자의 할 일만)
        if user_id:
            query = query.filter(Todo.user_id == user_id)

        if filters:
            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Todo.title.ilike(search_term),
                        Todo.description.ilike(search_term)
                    )
                )

            if filters.get('priority'):
                query = query.filter(Todo.priority == filters['priority'])

            if filters.get('category'):
                query = query.filter(Todo.category == filters['category'])

            if filters.get('completed') is not None:
                query = query.filter(Todo.completed == filters['completed'])

            if filters.get('due_date'):
                query = query.filter(Todo.due_date <= filters['due_date'])

            if filters.get('is_public') is not None:
                query = query.filter(Todo.is_public == filters['is_public'])

        # 정렬
        sort_by = filters.get('sort_by', 'created_at')
        order = filters.get('order', 'desc')

        if hasattr(Todo, sort_by):
            sort_column = getattr(Todo, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        return query.all()

    @staticmethod
    def get_todo_by_id(todo_id, user_id=None):
        query = Todo.query.filter_by(id=todo_id)

        # 사용자별 필터링
        if user_id:
            query = query.filter_by(user_id=user_id)

        return query.first_or_404()

    @staticmethod
    def create_todo(data, user_id):
        todo = Todo.from_dict(data)
        todo.user_id = user_id  # 사용자 ID 설정
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def update_todo(todo_id, data, user_id=None):
        todo = TodoService.get_todo_by_id(todo_id, user_id)

        for key, value in data.items():
            if hasattr(todo, key):
                if key == 'due_date' and value:
                    value = datetime.fromisoformat(value)
                setattr(todo, key, value)

        todo.updated_at = datetime.utcnow()
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id, user_id=None):
        todo = TodoService.get_todo_by_id(todo_id, user_id)
        db.session.delete(todo)
        db.session.commit()
        return todo

    @staticmethod
    def toggle_complete(todo_id, user_id=None):
        todo = TodoService.get_todo_by_id(todo_id, user_id)
        todo.completed = not todo.completed

        if todo.completed:
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None

        todo.updated_at = datetime.utcnow()
        db.session.commit()
        return todo

    @staticmethod
    def get_statistics(user_id=None):
        query = Todo.query

        # 사용자별 필터링
        if user_id:
            query = query.filter_by(user_id=user_id)

        total = query.count()
        completed = query.filter_by(completed=True).count()
        pending = total - completed

        # 우선순위별 통계
        priority_stats = {}
        for priority in ['높음', '중간', '낮음']:
            count_query = Todo.query.filter_by(priority=priority)
            if user_id:
                count_query = count_query.filter_by(user_id=user_id)
            priority_stats[priority] = count_query.count()

        # 카테고리별 통계
        category_stats = {}
        for category in ['개인', '업무', '학습']:
            count_query = Todo.query.filter_by(category=category)
            if user_id:
                count_query = count_query.filter_by(user_id=user_id)
            category_stats[category] = count_query.count()

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'priority_stats': priority_stats,
            'category_stats': category_stats
        }