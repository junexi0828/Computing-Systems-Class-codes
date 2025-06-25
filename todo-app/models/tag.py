from datetime import datetime
from extensions import db
from sqlalchemy import Index

class Tag(db.Model):
    """태그 모델"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default='#007bff')  # HEX 색상 코드
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 인덱스 생성
    __table_args__ = (
        Index('idx_tags_user_id', 'user_id'),
        Index('idx_tags_name', 'name'),
        # 사용자별 태그명 중복 방지
        db.UniqueConstraint('user_id', 'name', name='unique_user_tag')
    )

    def __repr__(self):
        return f'<Tag {self.name}>'

    def to_dict(self):
        """태그 정보를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def to_dict_simple(self):
        """할 일에 연결할 때 사용하는 간단한 형태"""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }

    @classmethod
    def create_tag(cls, user_id, name, color='#007bff'):
        """태그 생성"""
        return cls(
            user_id=user_id,
            name=name,
            color=color
        )