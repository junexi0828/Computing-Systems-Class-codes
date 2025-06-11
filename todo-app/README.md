# Todo List 웹 애플리케이션

Docker 기반의 Flask와 MySQL을 활용한 Todo List 웹 애플리케이션입니다.

## 기능

- 할 일 추가, 조회, 수정, 삭제
- 우선순위 설정 (높음/중간/낮음)
- 카테고리 분류 (개인/업무/학습)
- 마감일 설정
- 완료 상태 토글
- 검색 기능

## 기술 스택

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: MySQL
- Container: Docker, Docker Compose

## 실행 방법

1. Docker와 Docker Compose가 설치되어 있어야 합니다.

2. 프로젝트 루트 디렉토리에서 다음 명령어를 실행합니다:
```bash
docker-compose up --build
```

3. 웹 브라우저에서 다음 주소로 접속합니다:
```
http://localhost:15000
```

4. MySQL DB에 접속하려면 (DBeaver, MySQL Workbench 등에서)
```
호스트: 127.0.0.1
포트: 13306
사용자: user
비밀번호: password
데이터베이스: todo_db
```

## API 엔드포인트

- GET    /todos          # 전체 할 일 목록 조회
- GET    /todos/<id>     # 특정 할 일 조회
- POST   /todos          # 새 할 일 추가
- PUT    /todos/<id>     # 할 일 수정
- DELETE /todos/<id>     # 할 일 삭제
- PATCH  /todos/<id>/complete  # 완료 상태 토글

## 환경 변수

- DATABASE_URL: MySQL 데이터베이스 연결 URL
- SECRET_KEY: Flask 애플리케이션 시크릿 키

## 프로젝트 구조

```
todo-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── app.py
├── config.py
├── manage.py                # 마이그레이션/seed/관리 명령
├── models/
│   └── todo.py
├── routes/
│   └── todo_routes.py
├── services/
│   └── todo_service.py
├── exceptions/
│   └── error_handlers.py
├── migrations/              # Flask-Migrate 자동 생성
├── db/
│   └── init.sql             # DB 초기 seed 데이터
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
``` 