from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TodoTag(db.Model):
    __tablename__ = 'todo_tags'

    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 관계 정의
    todo = db.relationship('Todo', back_populates='todo_tags')
    tag = db.relationship('Tag', back_populates='todo_tags')

    # 중복 연결 방지
    __table_args__ = (
        db.UniqueConstraint('todo_id', 'tag_id', name='unique_todo_tag'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'todo_id': self.todo_id,
            'tag_id': self.tag_id,
            'created_at': self.created_at.isoformat()
        }