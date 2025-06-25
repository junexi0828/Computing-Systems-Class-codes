from sqlalchemy.exc import IntegrityError
from models.tag import Tag, db
from models.todo_tag import TodoTag
from models.todo import Todo

class TagService:
    @staticmethod
    def get_user_tags(user_id):
        """사용자의 모든 태그 조회"""
        return Tag.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_tag_by_id(tag_id, user_id=None):
        """태그 ID로 태그 조회 (사용자별 필터링)"""
        query = Tag.query.filter_by(id=tag_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.first()

    @staticmethod
    def create_tag(user_id, data):
        """태그 생성"""
        # 필수 필드 검증
        if not data.get('name'):
            raise ValueError('태그명은 필수입니다')

        # 태그명 길이 검증
        if len(data['name']) > 50:
            raise ValueError('태그명은 50자 이하여야 합니다')

        # 색상 코드 검증
        color = data.get('color', '#007bff')
        if not color.startswith('#') or len(color) != 7:
            raise ValueError('올바른 색상 코드를 입력해주세요 (예: #007bff)')

        # 중복 태그명 검사
        existing_tag = Tag.query.filter_by(user_id=user_id, name=data['name']).first()
        if existing_tag:
            raise ValueError('이미 존재하는 태그명입니다')

        # 태그 생성
        tag = Tag(
            user_id=user_id,
            name=data['name'],
            color=color
        )

        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except IntegrityError:
            db.session.rollback()
            raise ValueError('태그 생성 중 오류가 발생했습니다')

    @staticmethod
    def update_tag(tag_id, user_id, data):
        """태그 수정"""
        tag = TagService.get_tag_by_id(tag_id, user_id)
        if not tag:
            raise ValueError('태그를 찾을 수 없습니다')

        # 수정 가능한 필드들
        if 'name' in data:
            if len(data['name']) > 50:
                raise ValueError('태그명은 50자 이하여야 합니다')

            # 중복 태그명 검사 (자신 제외)
            existing_tag = Tag.query.filter(
                Tag.user_id == user_id,
                Tag.name == data['name'],
                Tag.id != tag_id
            ).first()
            if existing_tag:
                raise ValueError('이미 존재하는 태그명입니다')

            tag.name = data['name']

        if 'color' in data:
            color = data['color']
            if not color.startswith('#') or len(color) != 7:
                raise ValueError('올바른 색상 코드를 입력해주세요 (예: #007bff)')
            tag.color = color

        try:
            db.session.commit()
            return tag
        except IntegrityError:
            db.session.rollback()
            raise ValueError('태그 수정 중 오류가 발생했습니다')

    @staticmethod
    def delete_tag(tag_id, user_id):
        """태그 삭제"""
        tag = TagService.get_tag_by_id(tag_id, user_id)
        if not tag:
            raise ValueError('태그를 찾을 수 없습니다')

        # 태그가 연결된 할 일이 있는지 확인
        if tag.todos:
            raise ValueError('할 일에 연결된 태그는 삭제할 수 없습니다. 먼저 할 일에서 태그를 제거해주세요.')

        try:
            db.session.delete(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'태그 삭제 중 오류가 발생했습니다: {str(e)}')

    @staticmethod
    def add_tag_to_todo(todo_id, tag_id, user_id):
        """할 일에 태그 추가"""
        # 할 일 조회 (사용자별 필터링)
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            raise ValueError('할 일을 찾을 수 없습니다')

        # 태그 조회 (사용자별 필터링)
        tag = TagService.get_tag_by_id(tag_id, user_id)
        if not tag:
            raise ValueError('태그를 찾을 수 없습니다')

        # 이미 연결되어 있는지 확인
        existing_connection = TodoTag.query.filter_by(todo_id=todo_id, tag_id=tag_id).first()
        if existing_connection:
            raise ValueError('이미 연결된 태그입니다')

        # 연결 생성
        todo_tag = TodoTag(todo_id=todo_id, tag_id=tag_id)

        try:
            db.session.add(todo_tag)
            db.session.commit()
            return todo_tag
        except IntegrityError:
            db.session.rollback()
            raise ValueError('태그 연결 중 오류가 발생했습니다')

    @staticmethod
    def remove_tag_from_todo(todo_id, tag_id, user_id):
        """할 일에서 태그 제거"""
        # 할 일 조회 (사용자별 필터링)
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            raise ValueError('할 일을 찾을 수 없습니다')

        # 태그 조회 (사용자별 필터링)
        tag = TagService.get_tag_by_id(tag_id, user_id)
        if not tag:
            raise ValueError('태그를 찾을 수 없습니다')

        # 연결 조회
        todo_tag = TodoTag.query.filter_by(todo_id=todo_id, tag_id=tag_id).first()
        if not todo_tag:
            raise ValueError('연결된 태그가 없습니다')

        try:
            db.session.delete(todo_tag)
            db.session.commit()
            return todo_tag
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'태그 제거 중 오류가 발생했습니다: {str(e)}')

    @staticmethod
    def get_todos_by_tag(tag_id, user_id):
        """특정 태그가 연결된 할 일 목록 조회"""
        tag = TagService.get_tag_by_id(tag_id, user_id)
        if not tag:
            raise ValueError('태그를 찾을 수 없습니다')

        return tag.todos

    @staticmethod
    def get_tags_by_todo(todo_id, user_id):
        """특정 할 일에 연결된 태그 목록 조회"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            raise ValueError('할 일을 찾을 수 없습니다')

        return todo.tags