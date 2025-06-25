from datetime import datetime
from extensions import db
from sqlalchemy import Index, ForeignKey

# 할 일-태그 연결 테이블
todo_tags = db.Table('todo_tags',
    db.Column('todo_id', db.Integer, db.ForeignKey('todos.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Todo(db.Model):
    """할 일 모델"""
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='중간')  # 높음, 중간, 낮음
    category = db.Column(db.String(50), default='개인')  # 개인, 업무, 학습
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('todos.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    tags = db.relationship('Tag', secondary=todo_tags, backref=db.backref('todos', lazy='dynamic'))
    subtasks = db.relationship('Todo', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<Todo {self.title}>'

    def to_dict(self):
        """할 일 정보를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_public': self.is_public,
            'parent_id': self.parent_id,
            'tags': [tag.to_dict() for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def toggle_complete(self):
        """완료 상태 토글"""
        self.completed = not self.completed
        self.completed_at = datetime.utcnow() if self.completed else None
        return self.completed

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority', '중간'),
            category=data.get('category', '개인'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            completed=data.get('completed', False),
            is_public=data.get('is_public', False),
            parent_id=data.get('parent_id')
        )

    # 인덱스 생성
    __table_args__ = (
        Index('idx_todos_user_id', 'user_id'),
        Index('idx_todos_priority', 'priority'),
        Index('idx_todos_category', 'category'),
        Index('idx_todos_completed', 'completed'),
        Index('idx_todos_due_date', 'due_date'),
        Index('idx_todos_is_public', 'is_public'),
        Index('idx_todos_parent_id', 'parent_id'),
    )