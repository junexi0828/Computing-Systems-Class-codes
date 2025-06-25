# 확장된 TODO 애플리케이션 백엔드 아키텍처

## 🏗️ 전체 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Load Balancer │
│   (React/Vue)   │◄──►│   (Nginx)       │◄──►│   (HAProxy)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Application Layer                      │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Auth Module   │   Todo Module   │   Tag Module    │   Stats   │
│   (JWT)         │   (CRUD)        │   (Management)  │   (Analytics)│
└─────────────────┴─────────────────┴─────────────────┴───────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer                                │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│  AuthService    │  TodoService    │  TagService     │  NotificationService │
│  UserService    │  ShareService   │  HistoryService │  StatisticsService   │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Access Layer                            │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   SQLAlchemy    │   Redis Cache   │   File Storage  │   External APIs │
│   (MySQL)       │   (Session)     │   (Images)      │   (Email/SMS)   │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

## 📁 프로젝트 구조 (확장)

```
todo-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── README.md
├── docs/
│   ├── ERD.md
│   ├── API_SPEC.md
│   ├── ARCHITECTURE.md
│   └── DEPLOYMENT.md
├── app.py                          # Flask 애플리케이션 팩토리
├── config.py                       # 설정 관리
├── manage.py                       # CLI 관리 명령
├── migrations/                     # 데이터베이스 마이그레이션
├── tests/                          # 테스트 코드
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── models/                         # 데이터 모델
│   ├── __init__.py
│   ├── user.py
│   ├── todo.py
│   ├── tag.py
│   ├── todo_share.py
│   ├── todo_history.py
│   ├── notification.py
│   └── user_setting.py
├── routes/                         # API 라우트
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── todo_routes.py
│   ├── tag_routes.py
│   ├── share_routes.py
│   ├── notification_routes.py
│   ├── statistics_routes.py
│   ├── settings_routes.py
│   └── search_routes.py
├── services/                       # 비즈니스 로직
│   ├── __init__.py
│   ├── auth_service.py
│   ├── user_service.py
│   ├── todo_service.py
│   ├── tag_service.py
│   ├── share_service.py
│   ├── notification_service.py
│   ├── statistics_service.py
│   └── history_service.py
├── middleware/                     # 미들웨어
│   ├── __init__.py
│   ├── auth_middleware.py
│   ├── rate_limit.py
│   ├── cors.py
│   └── logging.py
├── utils/                          # 유틸리티
│   ├── __init__.py
│   ├── validators.py
│   ├── helpers.py
│   ├── decorators.py
│   └── constants.py
├── exceptions/                     # 예외 처리
│   ├── __init__.py
│   ├── error_handlers.py
│   └── custom_exceptions.py
├── schemas/                        # 요청/응답 스키마
│   ├── __init__.py
│   ├── auth_schemas.py
│   ├── todo_schemas.py
│   ├── tag_schemas.py
│   └── common_schemas.py
├── tasks/                          # 백그라운드 작업
│   ├── __init__.py
│   ├── notification_tasks.py
│   └── cleanup_tasks.py
├── db/                             # 데이터베이스
│   ├── init.sql
│   └── seeds/
├── static/                         # 정적 파일
└── templates/                      # 템플릿 (관리자용)
```

## 🔧 핵심 컴포넌트 설계

### 1. 인증 시스템 (Auth Module)

```python
# middleware/auth_middleware.py
class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # JWT 토큰 검증 로직
        pass

# services/auth_service.py
class AuthService:
    @staticmethod
    def register_user(data):
        # 회원가입 로직
        pass

    @staticmethod
    def authenticate_user(username, password):
        # 로그인 로직
        pass

    @staticmethod
    def refresh_token(refresh_token):
        # 토큰 갱신 로직
        pass
```

### 2. 할 일 관리 시스템 (Todo Module)

```python
# services/todo_service.py
class TodoService:
    @staticmethod
    def get_todos_with_filters(user_id, filters):
        # 고급 필터링 로직
        pass

    @staticmethod
    def create_todo_with_tags(user_id, data):
        # 태그와 함께 할 일 생성
        pass

    @staticmethod
    def share_todo(todo_id, user_id, share_data):
        # 할 일 공유 로직
        pass
```

### 3. 태그 관리 시스템 (Tag Module)

```python
# services/tag_service.py
class TagService:
    @staticmethod
    def get_user_tags(user_id):
        # 사용자 태그 조회
        pass

    @staticmethod
    def create_tag(user_id, data):
        # 태그 생성
        pass

    @staticmethod
    def get_todos_by_tag(user_id, tag_id):
        # 태그별 할 일 조회
        pass
```

### 4. 알림 시스템 (Notification Module)

```python
# services/notification_service.py
class NotificationService:
    @staticmethod
    def create_due_soon_notification(todo_id):
        # 마감일 임박 알림 생성
        pass

    @staticmethod
    def send_notification(user_id, notification_data):
        # 알림 전송 (이메일, 푸시)
        pass

    @staticmethod
    def mark_as_read(notification_id):
        # 알림 읽음 처리
        pass
```

### 5. 통계 시스템 (Statistics Module)

```python
# services/statistics_service.py
class StatisticsService:
    @staticmethod
    def get_dashboard_stats(user_id):
        # 대시보드 통계
        pass

    @staticmethod
    def get_period_stats(user_id, start_date, end_date):
        # 기간별 통계
        pass

    @staticmethod
    def get_productivity_score(user_id):
        # 생산성 점수 계산
        pass
```

## 🔄 데이터 플로우

### 1. 할 일 생성 플로우
```
1. 클라이언트 → POST /api/todos
2. AuthMiddleware → JWT 검증
3. TodoRoutes → 요청 검증
4. TodoService → 비즈니스 로직
5. TagService → 태그 처리
6. ShareService → 공유 설정
7. NotificationService → 알림 생성
8. Database → 저장
9. Response → 클라이언트
```

### 2. 알림 처리 플로우
```
1. Background Task → 주기적 실행
2. NotificationService → 마감일 체크
3. EmailService → 이메일 전송
4. PushService → 푸시 알림
5. Database → 알림 상태 업데이트
```

## 🛡️ 보안 설계

### 1. 인증 및 권한
- JWT 토큰 기반 인증
- Role-based Access Control (RBAC)
- API Rate Limiting
- CORS 설정

### 2. 데이터 보안
- SQL Injection 방지 (SQLAlchemy ORM)
- XSS 방지 (입력 검증)
- CSRF 토큰
- 비밀번호 해싱 (bcrypt)

### 3. API 보안
- HTTPS 강제
- API 버전 관리
- 요청/응답 로깅
- 에러 정보 숨김

## 📊 성능 최적화

### 1. 데이터베이스 최적화
- 적절한 인덱스 설정
- 쿼리 최적화
- Connection Pooling
- Read Replica 분리

### 2. 캐싱 전략
- Redis를 활용한 세션 캐싱
- API 응답 캐싱
- 데이터베이스 쿼리 캐싱

### 3. 비동기 처리
- Celery를 활용한 백그라운드 작업
- 알림 전송 비동기화
- 대용량 데이터 처리

## 🔍 모니터링 및 로깅

### 1. 로깅 시스템
```python
# utils/logging.py
import logging
from flask import request

def setup_logging(app):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 요청 로깅
    @app.before_request
    def log_request():
        logging.info(f"Request: {request.method} {request.path}")

    # 에러 로깅
    @app.errorhandler(Exception)
    def log_error(error):
        logging.error(f"Error: {str(error)}")
```

### 2. 성능 모니터링
- API 응답 시간 측정
- 데이터베이스 쿼리 성능
- 메모리 사용량 모니터링
- 에러율 추적

## 🚀 배포 아키텍처

### 1. 개발 환경
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Flask     │    │   MySQL     │
│   (Dev)     │◄──►│   (Dev)     │◄──►│   (Dev)     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2. 프로덕션 환경
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CDN       │    │   Load      │    │   Redis     │
│   (Static)  │    │   Balancer  │    │   (Cache)   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                    ┌─────────────┐
                    │   Nginx     │
                    │   (Proxy)   │
                    └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Flask     │    │   Flask     │    │   MySQL     │
│   (App 1)   │    │   (App 2)   │    │   (Master)  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                  │
                    ┌─────────────┐    ┌─────────────┐
                    │   Celery    │    │   MySQL     │
                    │   (Worker)  │    │   (Slave)   │
                    └─────────────┘    └─────────────┘
```

## 📈 확장성 고려사항

### 1. 수평 확장
- 무상태(Stateless) 설계
- 세션 외부 저장 (Redis)
- 로드 밸런서 활용

### 2. 데이터베이스 확장
- Read Replica 분리
- 샤딩 전략
- 마이크로서비스 분리

### 3. 캐싱 전략
- CDN 활용
- Redis Cluster
- 분산 캐싱

이러한 아키텍처를 통해 확장 가능하고 유지보수가 용이한 백엔드 시스템을 구축할 수 있습니다.