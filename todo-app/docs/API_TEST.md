# API 테스트 가이드

## 기본 설정

### 1. 서버 실행
```bash
docker-compose up --build
```

### 2. 기본 URL
```
http://localhost:15000
```

## 인증 API 테스트

### 1. 회원가입
```bash
curl -X POST http://localhost:15000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "테스트 사용자"
  }'
```

**응답 예시:**
```json
{
  "message": "회원가입이 완료되었습니다",
  "user": {
    "id": 4,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "테스트 사용자",
    "avatar_url": null,
    "role": "user",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 2. 로그인
```bash
curl -X POST http://localhost:15000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

**응답 예시:**
```json
{
  "message": "로그인이 완료되었습니다",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 4,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "테스트 사용자",
    "avatar_url": null,
    "role": "user",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 3. 프로필 조회
```bash
curl -X GET http://localhost:15000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 할 일 관리 API 테스트

### 1. 할 일 목록 조회
```bash
curl -X GET http://localhost:15000/api/todos \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. 할 일 생성
```bash
curl -X POST http://localhost:15000/api/todos \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "새로운 할 일",
    "description": "이것은 테스트 할 일입니다",
    "priority": "높음",
    "category": "업무",
    "due_date": "2024-12-31T23:59:59Z"
  }'
```

### 3. 할 일 수정
```bash
curl -X PUT http://localhost:15000/api/todos/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "수정된 할 일",
    "priority": "중간"
  }'
```

### 4. 할 일 완료 토글
```bash
curl -X PATCH http://localhost:15000/api/todos/1/complete \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. 할 일 삭제
```bash
curl -X DELETE http://localhost:15000/api/todos/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. 통계 조회
```bash
curl -X GET http://localhost:15000/api/todos/statistics \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 고급 필터링 테스트

### 1. 검색 기능
```bash
curl -X GET "http://localhost:15000/api/todos?search=프로젝트" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. 우선순위 필터
```bash
curl -X GET "http://localhost:15000/api/todos?priority=높음" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. 카테고리 필터
```bash
curl -X GET "http://localhost:15000/api/todos?category=업무" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. 완료 상태 필터
```bash
curl -X GET "http://localhost:15000/api/todos?completed=false" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. 정렬
```bash
curl -X GET "http://localhost:15000/api/todos?sort_by=due_date&order=asc" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 샘플 계정으로 테스트

### 1. user1 계정으로 로그인
```bash
curl -X POST http://localhost:15000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "password123"
  }'
```

### 2. user2 계정으로 로그인
```bash
curl -X POST http://localhost:15000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user2",
    "password": "password123"
  }'
```

## 에러 테스트

### 1. 잘못된 토큰
```bash
curl -X GET http://localhost:15000/api/todos \
  -H "Authorization: Bearer invalid-token"
```

### 2. 토큰 없이 접근
```bash
curl -X GET http://localhost:15000/api/todos
```

### 3. 잘못된 비밀번호
```bash
curl -X POST http://localhost:15000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "wrongpassword"
  }'
```

### 4. 중복 사용자명
```bash
curl -X POST http://localhost:15000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "duplicate@example.com",
    "password": "password123"
  }'
```

## Postman 컬렉션

Postman을 사용하는 경우 다음 환경 변수를 설정하세요:

### 환경 변수
- `base_url`: `http://localhost:15000`
- `access_token`: 로그인 후 받은 액세스 토큰
- `refresh_token`: 로그인 후 받은 리프레시 토큰

### 헤더 설정
- `Content-Type`: `application/json`
- `Authorization`: `Bearer {{access_token}}`

## 테스트 시나리오

### 1. 전체 플로우 테스트
1. 회원가입
2. 로그인
3. 할 일 생성
4. 할 일 목록 조회
5. 할 일 수정
6. 할 일 완료 토글
7. 통계 조회
8. 할 일 삭제

### 2. 보안 테스트
1. 토큰 없이 API 접근
2. 잘못된 토큰으로 API 접근
3. 만료된 토큰으로 API 접근
4. 다른 사용자의 할 일 접근 시도

### 3. 데이터 검증 테스트
1. 필수 필드 누락
2. 잘못된 이메일 형식
3. 짧은 비밀번호
4. 중복 사용자명/이메일

## 🔐 인증

### 1. 로그인하여 JWT 토큰 획득
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "password123"
  }'
```

응답에서 `access_token`을 복사하여 다음 요청에 사용하세요.

## 📝 할 일 (Todo) API

### 1. 할 일 목록 조회
```bash
curl -X GET http://localhost:5000/api/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. 할 일 생성
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "새로운 할 일",
    "description": "할 일 설명",
    "priority": "높음",
    "category": "업무",
    "due_date": "2024-12-31T23:59:59"
  }'
```

### 3. 할 일 수정
```bash
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "수정된 할 일",
    "completed": true
  }'
```

### 4. 할 일 삭제
```bash
curl -X DELETE http://localhost:5000/api/todos/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. 할 일 완료 토글
```bash
curl -X PATCH http://localhost:5000/api/todos/1/toggle \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. 할 일 검색
```bash
curl -X GET "http://localhost:5000/api/todos/search?q=프로젝트&priority=높음&category=업무" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 7. 할 일 통계
```bash
curl -X GET http://localhost:5000/api/todos/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🏷️ 태그 (Tag) API

### 1. 태그 목록 조회
```bash
curl -X GET http://localhost:5000/api/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. 태그 생성
```bash
curl -X POST http://localhost:5000/api/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "중요",
    "color": "#ff0000"
  }'
```

### 3. 태그 수정
```bash
curl -X PUT http://localhost:5000/api/tags/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "매우 중요",
    "color": "#ff6600"
  }'
```

### 4. 태그 삭제
```bash
curl -X DELETE http://localhost:5000/api/tags/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. 할 일에 태그 추가
```bash
curl -X POST http://localhost:5000/api/todos/1/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_id": 1
  }'
```

### 6. 할 일에서 태그 제거
```bash
curl -X DELETE http://localhost:5000/api/todos/1/tags/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 7. 특정 태그가 연결된 할 일 목록 조회
```bash
curl -X GET http://localhost:5000/api/tags/1/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 8. 특정 할 일에 연결된 태그 목록 조회
```bash
curl -X GET http://localhost:5000/api/todos/1/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔍 샘플 테스트 시나리오

### 시나리오 1: 태그 시스템 전체 플로우
```bash
# 1. 로그인
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}' | jq -r '.access_token')

# 2. 태그 생성
curl -X POST http://localhost:5000/api/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "프로젝트", "color": "#28a745"}'

# 3. 할 일 생성
curl -X POST http://localhost:5000/api/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "새 프로젝트 시작", "description": "새로운 프로젝트를 시작합니다"}'

# 4. 할 일에 태그 추가
curl -X POST http://localhost:5000/api/todos/1/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tag_id": 1}'

# 5. 할 일 조회 (태그 포함)
curl -X GET http://localhost:5000/api/todos \
  -H "Authorization: Bearer $TOKEN"
```

### 시나리오 2: 태그별 할 일 필터링
```bash
# 1. 여러 태그 생성
curl -X POST http://localhost:5000/api/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "긴급", "color": "#ff6600"}'

curl -X POST http://localhost:5000/api/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "개인", "color": "#007bff"}'

# 2. 여러 할 일 생성 및 태그 연결
# ... (할 일 생성 및 태그 연결)

# 3. 특정 태그의 할 일만 조회
curl -X GET http://localhost:5000/api/tags/1/todos \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 응답 예시

### 태그 목록 조회 응답
```json
[
  {
    "id": 1,
    "user_id": 2,
    "name": "중요",
    "color": "#ff0000",
    "created_at": "2024-01-01T00:00:00",
    "todo_count": 2
  },
  {
    "id": 2,
    "user_id": 2,
    "name": "업무",
    "color": "#28a745",
    "created_at": "2024-01-01T00:00:00",
    "todo_count": 1
  }
]
```

### 할 일 조회 응답 (태그 포함)
```json
[
  {
    "id": 1,
    "user_id": 2,
    "title": "프로젝트 완료",
    "description": "중요한 프로젝트를 완료해야 합니다",
    "priority": "높음",
    "category": "업무",
    "due_date": "2024-12-31T23:59:59",
    "completed": false,
    "completed_at": null,
    "is_public": false,
    "parent_id": null,
    "tags": [
      {
        "id": 1,
        "name": "중요",
        "color": "#ff0000"
      },
      {
        "id": 2,
        "name": "업무",
        "color": "#28a745"
      }
    ],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

## ⚠️ 주의사항

1. **JWT 토큰**: 모든 API 요청에 유효한 JWT 토큰이 필요합니다.
2. **사용자별 데이터**: 각 사용자는 자신의 태그와 할 일만 접근할 수 있습니다.
3. **태그 중복**: 같은 사용자가 동일한 이름의 태그를 생성할 수 없습니다.
4. **태그 삭제**: 할 일에 연결된 태그는 삭제할 수 없습니다. 먼저 할 일에서 태그를 제거해야 합니다.
5. **색상 코드**: 태그 색상은 HEX 형식(#RRGGBB)으로 입력해야 합니다.

## 🧪 테스트 도구

- **curl**: 명령줄에서 API 테스트
- **Postman**: GUI 기반 API 테스트 도구
- **jq**: JSON 응답 파싱 (예: `curl ... | jq '.'`)