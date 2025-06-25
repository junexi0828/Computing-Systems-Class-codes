import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app
from models.user import User
from extensions import db
from sqlalchemy.exc import IntegrityError

class AuthService:
    @staticmethod
    def hash_password(password):
        """비밀번호를 bcrypt로 해시화"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash):
        """비밀번호 검증"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def generate_tokens(user_id):
        """JWT 액세스 토큰과 리프레시 토큰 생성"""
        now = datetime.utcnow()

        # 액세스 토큰 (짧은 만료 시간)
        access_token_payload = {
            'user_id': user_id,
            'exp': now + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
            'iat': now,
            'type': 'access'
        }
        access_token = jwt.encode(
            access_token_payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

        # 리프레시 토큰 (긴 만료 시간)
        refresh_token_payload = {
            'user_id': user_id,
            'exp': now + timedelta(seconds=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']),
            'iat': now,
            'type': 'refresh'
        }
        refresh_token = jwt.encode(
            refresh_token_payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

        return access_token, refresh_token

    @staticmethod
    def verify_token(token):
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError('토큰이 만료되었습니다')
        except jwt.InvalidTokenError:
            raise ValueError('유효하지 않은 토큰입니다')

    @staticmethod
    def register_user(data):
        """사용자 회원가입"""
        # 필수 필드 검증
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'{field}는 필수입니다')

        # 이메일 형식 검증
        if '@' not in data['email']:
            raise ValueError('유효한 이메일 주소를 입력해주세요')

        # 비밀번호 길이 검증
        if len(data['password']) < 6:
            raise ValueError('비밀번호는 최소 6자 이상이어야 합니다')

        # 중복 검사
        if User.query.filter_by(username=data['username']).first():
            raise ValueError('이미 사용 중인 사용자명입니다')

        if User.query.filter_by(email=data['email']).first():
            raise ValueError('이미 사용 중인 이메일입니다')

        # 비밀번호 해시화
        password_hash = AuthService.hash_password(data['password'])

        # 사용자 생성
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            full_name=data.get('full_name', ''),
            avatar_url=data.get('avatar_url', '')
        )

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError('사용자 생성 중 오류가 발생했습니다')

    @staticmethod
    def authenticate_user(username, password):
        """사용자 인증 (로그인)"""
        if not username or not password:
            raise ValueError('사용자명과 비밀번호를 입력해주세요')

        # 사용자 조회 (사용자명 또는 이메일로)
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).filter_by(is_active=True).first()

        if not user:
            raise ValueError('사용자를 찾을 수 없습니다')

        # 비밀번호 검증
        if not AuthService.verify_password(password, user.password_hash):
            raise ValueError('비밀번호가 일치하지 않습니다')

        return user

    @staticmethod
    def get_user_by_id(user_id):
        """사용자 ID로 사용자 조회"""
        return User.query.filter_by(id=user_id, is_active=True).first()

    @staticmethod
    def refresh_access_token(refresh_token):
        """리프레시 토큰으로 액세스 토큰 갱신"""
        try:
            payload = AuthService.verify_token(refresh_token)

            if payload.get('type') != 'refresh':
                raise ValueError('리프레시 토큰이 아닙니다')

            user = AuthService.get_user_by_id(payload['user_id'])
            if not user:
                raise ValueError('사용자를 찾을 수 없습니다')

            # 새로운 액세스 토큰 생성
            now = datetime.utcnow()
            access_token_payload = {
                'user_id': user.id,
                'exp': now + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
                'iat': now,
                'type': 'access'
            }
            access_token = jwt.encode(
                access_token_payload,
                current_app.config['JWT_SECRET_KEY'],
                algorithm='HS256'
            )

            return access_token, user

        except Exception as e:
            raise ValueError(f'토큰 갱신 실패: {str(e)}')