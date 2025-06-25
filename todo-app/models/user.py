from datetime import datetime
from extensions import db
from sqlalchemy import Index

class User(db.Model):
    """사용자 모델"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 - backref 제거하여 충돌 방지
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', backref='user', lazy=True, cascade='all, delete-orphan')

    # 인덱스 생성
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
        Index('idx_users_is_active', 'is_active'),
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """사용자 정보를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def to_dict_public(self):
        """공개용 사용자 정보 (비밀번호 제외)"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'role': 'admin' if self.is_admin else 'user',
            'created_at': self.created_at.isoformat()
        }

    def to_dict_safe(self):
        """비밀번호 등 민감 정보 제외 안전 반환"""
        return self.to_dict_public()