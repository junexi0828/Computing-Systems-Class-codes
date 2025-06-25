# Docker 기반 TODO List 웹 애플리케이션 개발 가이드라인

## 과제 목표
Docker 컨테이너 환경에서 Flask와 MySQL을 활용하여 TODO List 웹 애플리케이션을 개발하는 것입니다. 이 과제를 통해 컨테이너 기반 개발 환경 구축, 웹 프레임워크 활용, 데이터베이스 연동 등 실무에서 필요한 핵심 기술을 학습합니다.

## 필수 요구사항

### 기술 스택
- **컨테이너**: Docker, Docker Compose
- **웹 프레임워크**: Flask (Python)
- **데이터베이스**: MySQL
- **프론트엔드**: HTML, CSS, JavaScript (프레임워크 사용 가능)

### 구현해야 할 기능

#### 할 일 관리 기본 기능
- **할 일 추가**: 제목, 설명, 마감일 입력
- **할 일 목록 조회**: 전체 목록을 테이블 형태로 표시
- **할 일 수정**: 기존 항목의 정보 수정
- **할 일 삭제**: 선택한 항목 삭제
- **완료 상태 변경**: 체크박스로 완료/미완료 토글

#### 추가 기능
- **우선순위 설정** (높음/중간/낮음)
- **카테고리 분류** (개인/업무/학습 등)
- **마감일 기준 정렬**
- **검색 기능** (제목 또는 설명에서 키워드 검색)

### 데이터베이스 설계

#### todos 테이블 필수 컬럼:
- `id` (Primary Key, Auto Increment)
- `title` (VARCHAR, NOT NULL)
- `description` (TEXT)
- `priority` (INT)
- `due_date` (DATETIME)
- `is_completed` (BOOLEAN, DEFAULT FALSE)
- `category` (VARCHAR)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

## 개발 가이드라인

### 1. 프로젝트 구조
```
todo-app/
├── docker-compose.yml      # Docker 서비스 정의
├── Dockerfile             # Flask 앱 컨테이너 설정
├── requirements.txt       # Python 패키지 목록
├── app.py                # Flask 메인 애플리케이션
├── config.py             # 설정 파일 (DB 연결 정보 등)
├── models/               # 데이터베이스 모델
│   └── todo.py
├── routes/               # API 라우트
│   └── todo_routes.py
├── templates/            # HTML 템플릿
│   ├── base.html
│   └── index.html
└── static/              # CSS, JS 파일
    ├── css/
    └── js/
```

### 2. Docker 설정
- **docker-compose.yml 작성**
  - Flask 웹 서버와 MySQL 데이터베이스를 별도 컨테이너로 구성
  - 네트워크를 통해 두 컨테이너가 통신하도록 설정
  - 볼륨 마운트로 데이터 영속성 보장
  - 환경 변수로 데이터베이스 연결 정보 관리

### 3. API 엔드포인트 설계
- `GET    /todos`          # 전체 할 일 목록 조회
- `GET    /todos/<id>`     # 특정 할 일 조회
- `POST   /todos`          # 새 할 일 추가
- `PUT    /todos/<id>`     # 할 일 수정
- `DELETE /todos/<id>`     # 할 일 삭제
- `PATCH  /todos/<id>/complete`  # 완료 상태 토글

### 4. 프론트엔드 구현 (AI로만 구현할 것)
- 반응형 디자인으로 모바일 환경 고려
- AJAX를 활용한 비동기 통신
- 사용자 친화적인 UI/UX 설계
- 입력 유효성 검증 (클라이언트 + 서버 양쪽)

## 평가 기준

### 기능 완성도 (40%)
- 모든 CRUD 기능이 정상 작동하는가
- 추가 기능들이 제대로 구현되었는가

### 코드 품질 (25%)
- 코드가 읽기 쉽고 구조화되어 있는가
- 에러 처리가 적절히 되어 있는가
- 보안 취약점이 없는가

### Docker 활용 (20%)
- Docker Compose로 전체 환경이 한 번에 실행되는가
- 컨테이너 간 통신이 올바르게 설정되었는가

### 데이터베이스 설계 (15%)
- 테이블 구조가 효율적인가
- 인덱스가 적절히 설정되었는가

## 제출 사항

### 소스 코드
- 압축 파일

### README.md 파일 (본 제출 코드 기반으로 평가할 예정)
- 프로젝트 설명
- 실행 방법 (docker-compose up 명령어 등)
- 환경 변수 설정 방법
- API 문서

### 스크린샷
- 애플리케이션 실행 화면
- 주요 기능 동작 화면

## 개발 팁

1. **먼저 Docker 없이 로컬에서 Flask 앱을 개발하고 테스트한 후 Docker화하는 것이 효율적입니다.**

2. **데이터베이스 초기 스키마는 SQL 파일로 작성하여 컨테이너 시작 시 자동으로 실행되도록 설정하세요.**

3. **개발 중에는 Flask의 디버그 모드를 활용하되, 최종 제출 시에는 프로덕션 설정으로 변경하세요.**

4. **환경 변수는 .env 파일로 관리하고, .env.example 파일을 제공하여 설정 방법을 안내하세요.**

## 현재 구현 상태

### ✅ 완료된 기능
- [x] Docker 및 Docker Compose 환경 구축
- [x] Flask 백엔드 기본 구조
- [x] MySQL 데이터베이스 연동
- [x] JWT 기반 사용자 인증 시스템
- [x] Todo CRUD API 구현
- [x] 태그 시스템 구현
- [x] 기본 에러 처리 및 검증
- [x] 단위 테스트 및 API 테스트
- [x] React + TypeScript 프론트엔드 기본 구조

### 🔄 진행 중인 기능
- [ ] 프론트엔드-백엔드 연동
- [ ] UI/UX 개선
- [ ] 추가 기능 구현 (알림, 공유, 캐싱 등)

### 📋 남은 작업
- [ ] 프론트엔드 완성 및 연동
- [ ] 최종 테스트 및 버그 수정
- [ ] 문서화 완성
- [ ] 배포 준비