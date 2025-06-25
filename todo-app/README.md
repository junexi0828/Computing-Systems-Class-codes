# 🚀 Flask Todo App with JWT Authentication & Tag System

Flask 기반의 고도화된 Todo 애플리케이션으로, JWT 인증과 태그 시스템을 포함한 완전한 기능을 제공합니다.

## ✨ 주요 기능

### 🔐 사용자 인증
- JWT 기반 사용자 인증
- 회원가입/로그인/로그아웃
- 비밀번호 해싱 (bcrypt)
- 토큰 기반 세션 관리

### 📝 할 일 관리
- CRUD 작업 (생성, 조회, 수정, 삭제)
- 우선순위 설정 (높음/중간/낮음)
- 카테고리 분류 (개인/업무/학습)
- 마감일 설정
- 완료 상태 토글
- 서브태스크 지원
- 공개/비공개 설정

### 🏷️ 태그 시스템
- 사용자별 태그 생성 및 관리
- 태그 색상 커스터마이징
- 할 일에 다중 태그 연결 (Many-to-Many)
- 태그별 할 일 필터링
- 태그 사용 통계

### 🔍 고급 기능
- 할 일 검색 (제목, 설명, 카테고리)
- 통계 대시보드
- 마감일 기반 정렬
- 우선순위별 필터링

## 🛠️ 기술 스택

- **Backend**: Flask, SQLAlchemy, JWT
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Containerization**: Docker & Docker Compose
- **API**: RESTful API

## 📁 프로젝트 구조

```
todo-app/
├── app.py                 # 메인 애플리케이션
├── config.py             # 설정 파일
├── requirements.txt      # Python 의존성
├── Dockerfile           # Docker 이미지 설정
├── docker-compose.yml   # Docker Compose 설정
├── .env                 # 환경 변수
├── .env.example         # 환경 변수 예시
├── models/              # 데이터 모델
│   ├── user.py         # 사용자 모델
│   ├── todo.py         # 할 일 모델
│   ├── tag.py          # 태그 모델
│   └── todo_tag.py     # 할 일-태그 연결 모델
├── routes/              # API 라우트
│   ├── auth_routes.py  # 인증 라우트
│   ├── todo_routes.py  # 할 일 라우트
│   └── tag_routes.py   # 태그 라우트
├── services/            # 비즈니스 로직
│   ├── auth_service.py # 인증 서비스
│   ├── todo_service.py # 할 일 서비스
│   └── tag_service.py  # 태그 서비스
├── middleware/          # 미들웨어
│   └── auth_middleware.py # JWT 인증 미들웨어
├── exceptions/          # 예외 처리
│   └── error_handlers.py # 에러 핸들러
├── db/                  # 데이터베이스
│   └── init.sql        # 초기 스키마 및 샘플 데이터
└── docs/               # 문서
    └── API_TEST.md     # API 테스트 가이드
```

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone <repository-url>
cd todo-app
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정을 변경
```

### 3. Docker Compose로 실행
```bash
docker-compose up -d
```

### 4. 애플리케이션 접속
- API 서버: http://localhost:5000
- MySQL: localhost:3306

## 📚 API 문서

### 인증 API
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃

### 할 일 API
- `GET /api/todos` - 할 일 목록 조회
- `POST /api/todos` - 할 일 생성
- `GET /api/todos/<id>` - 할 일 상세 조회
- `PUT /api/todos/<id>` - 할 일 수정
- `DELETE /api/todos/<id>` - 할 일 삭제
- `PATCH /api/todos/<id>/toggle` - 완료 상태 토글
- `GET /api/todos/search` - 할 일 검색
- `GET /api/todos/stats` - 통계 조회

### 태그 API
- `GET /api/tags` - 태그 목록 조회
- `POST /api/tags` - 태그 생성
- `PUT /api/tags/<id>` - 태그 수정
- `DELETE /api/tags/<id>` - 태그 삭제
- `POST /api/todos/<todo_id>/tags` - 할 일에 태그 추가
- `DELETE /api/todos/<todo_id>/tags/<tag_id>` - 할 일에서 태그 제거
- `GET /api/tags/<tag_id>/todos` - 태그별 할 일 조회
- `GET /api/todos/<todo_id>/tags` - 할 일의 태그 조회

## 🔐 샘플 계정

애플리케이션 실행 시 다음 샘플 계정이 자동으로 생성됩니다:

| 사용자명 | 이메일 | 비밀번호 | 역할 |
|---------|--------|----------|------|
| admin | admin@example.com | password123 | 관리자 |
| user1 | user1@example.com | password123 | 일반 사용자 |
| user2 | user2@example.com | password123 | 일반 사용자 |

## 🧪 API 테스트

자세한 API 테스트 방법은 [API_TEST.md](docs/API_TEST.md)를 참조하세요.

### 빠른 테스트 예시
```bash
# 1. 로그인하여 토큰 획득
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'

# 2. 태그 생성
curl -X POST http://localhost:5000/api/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "중요", "color": "#ff0000"}'

# 3. 할 일 생성
curl -X POST http://localhost:5000/api/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "새 할 일", "description": "설명"}'

# 4. 할 일에 태그 추가
curl -X POST http://localhost:5000/api/todos/1/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tag_id": 1}'
```

## 🔧 개발 환경 설정

### 로컬 개발
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export FLASK_APP=app.py
export FLASK_ENV=development

# 애플리케이션 실행
flask run
```

### 데이터베이스 마이그레이션
```bash
# 마이그레이션 초기화
flask db init

# 마이그레이션 생성
flask db migrate -m "Initial migration"

# 마이그레이션 적용
flask db upgrade
```

## 🏗️ 데이터베이스 스키마

### 사용자 테이블 (users)
- id, username, email, password_hash, full_name, avatar_url, is_active, role, created_at, updated_at

### 할 일 테이블 (todos)
- id, user_id, title, description, priority, category, due_date, completed, completed_at, is_public, parent_id, created_at, updated_at

### 태그 테이블 (tags)
- id, user_id, name, color, created_at

### 할 일-태그 연결 테이블 (todo_tags)
- id, todo_id, tag_id, created_at

## 🔒 보안 기능

- JWT 토큰 기반 인증
- 비밀번호 bcrypt 해싱
- 사용자별 데이터 격리
- SQL 인젝션 방지 (SQLAlchemy ORM)
- CORS 설정
- 입력 데이터 검증

## 🚀 배포

### Docker 배포
```bash
# 프로덕션 빌드
docker-compose -f docker-compose.prod.yml up -d

# 로그 확인
docker-compose logs -f
```

### 환경 변수 설정
프로덕션 환경에서는 다음 환경 변수를 설정하세요:
- `SECRET_KEY`: 강력한 시크릿 키
- `JWT_SECRET_KEY`: JWT 서명용 키
- `DATABASE_URL`: 프로덕션 데이터베이스 URL

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 문제 해결

### 일반적인 문제들

1. **데이터베이스 연결 오류**
   - Docker 컨테이너가 실행 중인지 확인
   - 환경 변수 설정 확인

2. **JWT 토큰 오류**
   - 토큰이 만료되었는지 확인
   - 올바른 Authorization 헤더 형식 사용

3. **태그 중복 오류**
   - 같은 사용자가 동일한 이름의 태그를 생성할 수 없음
   - 태그명 변경 후 재시도

4. **태그 삭제 오류**
   - 할 일에 연결된 태그는 먼저 연결을 해제해야 함

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.