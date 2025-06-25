# 확장된 TODO 애플리케이션 API 명세서

## 🔐 인증 관련

### JWT 토큰 기반 인증
- 모든 API 요청 시 `Authorization: Bearer <token>` 헤더 필요
- 토큰 만료 시 401 Unauthorized 응답

---

## 👤 사용자 관리 API

### 1. 회원가입
```
POST /api/auth/register
Content-Type: application/json

Request Body:
{
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string"
}

Response (201):
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "full_name": "홍길동",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. 로그인
```
POST /api/auth/login
Content-Type: application/json

Request Body:
{
    "username": "string",
    "password": "string"
}

Response (200):
{
    "access_token": "jwt_token_here",
    "refresh_token": "refresh_token_here",
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "full_name": "홍길동"
    }
}
```

### 3. 프로필 조회
```
GET /api/auth/profile
Authorization: Bearer <token>

Response (200):
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "full_name": "홍길동",
    "avatar_url": "https://...",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 4. 프로필 수정
```
PUT /api/auth/profile
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "full_name": "string",
    "avatar_url": "string"
}

Response (200):
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "full_name": "수정된 이름",
    "avatar_url": "https://...",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## 📝 할 일 관리 API (확장)

### 1. 할 일 목록 조회 (고급 필터링)
```
GET /api/todos?search=검색어&priority=높음&category=업무&completed=false&due_date=2024-12-31&sort_by=due_date&order=asc&page=1&limit=20&include_subtasks=true&tags=중요,긴급
Authorization: Bearer <token>

Response (200):
{
    "todos": [
        {
            "id": 1,
            "title": "프로젝트 완료",
            "description": "중요한 프로젝트",
            "priority": "높음",
            "category": "업무",
            "due_date": "2024-12-31T23:59:59Z",
            "completed": false,
            "completed_at": null,
            "is_public": false,
            "parent_id": null,
            "tags": ["중요", "긴급"],
            "subtasks": [
                {
                    "id": 2,
                    "title": "서브태스크",
                    "completed": true
                }
            ],
            "shared_with": [
                {
                    "user_id": 2,
                    "username": "colleague",
                    "permission": "write"
                }
            ],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 100,
        "pages": 5
    }
}
```

### 2. 할 일 생성 (확장)
```
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "title": "string",
    "description": "string",
    "priority": "높음|중간|낮음",
    "category": "string",
    "due_date": "2024-12-31T23:59:59Z",
    "is_public": false,
    "parent_id": null,
    "tags": ["중요", "긴급"],
    "share_with": [
        {
            "user_id": 2,
            "permission": "write"
        }
    ]
}

Response (201):
{
    "id": 1,
    "title": "새 할 일",
    "description": "설명",
    "priority": "높음",
    "category": "업무",
    "due_date": "2024-12-31T23:59:59Z",
    "completed": false,
    "tags": ["중요", "긴급"],
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 3. 할 일 수정 (확장)
```
PUT /api/todos/{id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "title": "수정된 제목",
    "description": "수정된 설명",
    "priority": "중간",
    "category": "개인",
    "due_date": "2024-12-31T23:59:59Z",
    "tags": ["수정된태그"]
}

Response (200):
{
    "id": 1,
    "title": "수정된 제목",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### 4. 할 일 완료 토글
```
PATCH /api/todos/{id}/complete
Authorization: Bearer <token>

Response (200):
{
    "id": 1,
    "completed": true,
    "completed_at": "2024-01-01T00:00:00Z"
}
```

### 5. 할 일 삭제
```
DELETE /api/todos/{id}
Authorization: Bearer <token>

Response (204): No Content
```

---

## 🏷️ 태그 관리 API

### 1. 태그 목록 조회
```
GET /api/tags
Authorization: Bearer <token>

Response (200):
[
    {
        "id": 1,
        "name": "중요",
        "color": "#ff0000",
        "todo_count": 5,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### 2. 태그 생성
```
POST /api/tags
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "name": "긴급",
    "color": "#ff0000"
}

Response (201):
{
    "id": 2,
    "name": "긴급",
    "color": "#ff0000",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 3. 태그 수정
```
PUT /api/tags/{id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "name": "매우긴급",
    "color": "#cc0000"
}

Response (200):
{
    "id": 2,
    "name": "매우긴급",
    "color": "#cc0000",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### 4. 태그 삭제
```
DELETE /api/tags/{id}
Authorization: Bearer <token>

Response (204): No Content
```

---

## 🤝 공유 관리 API

### 1. 할 일 공유
```
POST /api/todos/{id}/share
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "user_id": 2,
    "permission": "write"
}

Response (201):
{
    "id": 1,
    "todo_id": 1,
    "shared_with": {
        "id": 2,
        "username": "colleague",
        "email": "colleague@example.com"
    },
    "permission": "write",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. 공유된 할 일 목록 조회
```
GET /api/todos/shared
Authorization: Bearer <token>

Response (200):
[
    {
        "id": 1,
        "title": "공유된 할 일",
        "shared_by": {
            "id": 2,
            "username": "colleague"
        },
        "permission": "write",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### 3. 공유 권한 수정
```
PUT /api/todos/{id}/share/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "permission": "admin"
}

Response (200):
{
    "permission": "admin",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### 4. 공유 해제
```
DELETE /api/todos/{id}/share/{user_id}
Authorization: Bearer <token>

Response (204): No Content
```

---

## 📊 통계 및 분석 API

### 1. 대시보드 통계
```
GET /api/statistics/dashboard
Authorization: Bearer <token>

Response (200):
{
    "overview": {
        "total_todos": 100,
        "completed_todos": 60,
        "pending_todos": 40,
        "overdue_todos": 5,
        "completion_rate": 60.0
    },
    "priority_stats": {
        "높음": {"total": 20, "completed": 10, "pending": 10},
        "중간": {"total": 50, "completed": 30, "pending": 20},
        "낮음": {"total": 30, "completed": 20, "pending": 10}
    },
    "category_stats": {
        "개인": {"total": 40, "completed": 25, "pending": 15},
        "업무": {"total": 35, "completed": 20, "pending": 15},
        "학습": {"total": 25, "completed": 15, "pending": 10}
    },
    "weekly_progress": [
        {"date": "2024-01-01", "completed": 5, "created": 3},
        {"date": "2024-01-02", "completed": 8, "created": 4}
    ]
}
```

### 2. 기간별 통계
```
GET /api/statistics/period?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer <token>

Response (200):
{
    "period": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
    },
    "completion_trend": [
        {"date": "2024-01-01", "completed": 5},
        {"date": "2024-01-02", "completed": 8}
    ],
    "productivity_score": 85.5,
    "most_productive_day": "2024-01-15",
    "category_distribution": {
        "개인": 40,
        "업무": 35,
        "학습": 25
    }
}
```

### 3. 태그별 통계
```
GET /api/statistics/tags
Authorization: Bearer <token>

Response (200):
[
    {
        "tag": "중요",
        "total_todos": 15,
        "completed_todos": 10,
        "completion_rate": 66.7,
        "avg_completion_time": "2.5 days"
    }
]
```

---

## 🔔 알림 관리 API

### 1. 알림 목록 조회
```
GET /api/notifications?is_read=false&type=due_soon&page=1&limit=20
Authorization: Bearer <token>

Response (200):
{
    "notifications": [
        {
            "id": 1,
            "type": "due_soon",
            "title": "마감일 임박",
            "message": "프로젝트 완료가 1일 남았습니다",
            "is_read": false,
            "todo_id": 1,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 50,
        "pages": 3
    }
}
```

### 2. 알림 읽음 처리
```
PATCH /api/notifications/{id}/read
Authorization: Bearer <token>

Response (200):
{
    "id": 1,
    "is_read": true,
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### 3. 모든 알림 읽음 처리
```
PATCH /api/notifications/read-all
Authorization: Bearer <token>

Response (200):
{
    "updated_count": 10
}
```

---

## ⚙️ 설정 관리 API

### 1. 사용자 설정 조회
```
GET /api/settings
Authorization: Bearer <token>

Response (200):
{
    "theme": "dark",
    "language": "ko",
    "timezone": "Asia/Seoul",
    "notification_email": true,
    "notification_push": true,
    "default_priority": "중간",
    "default_category": "개인"
}
```

### 2. 사용자 설정 수정
```
PUT /api/settings
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "theme": "dark",
    "language": "en",
    "timezone": "UTC",
    "notification_email": false,
    "default_priority": "높음"
}

Response (200):
{
    "theme": "dark",
    "language": "en",
    "timezone": "UTC",
    "notification_email": false,
    "default_priority": "높음",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## 📈 히스토리 및 감사 API

### 1. 할 일 변경 히스토리
```
GET /api/todos/{id}/history?page=1&limit=20
Authorization: Bearer <token>

Response (200):
{
    "history": [
        {
            "id": 1,
            "action": "updated",
            "old_values": {"title": "이전 제목"},
            "new_values": {"title": "새 제목"},
            "user": {
                "id": 1,
                "username": "user123"
            },
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 50,
        "pages": 3
    }
}
```

---

## 🔍 검색 API

### 1. 고급 검색
```
GET /api/search?q=검색어&type=todos&filters={"priority":"높음","completed":false}&sort_by=due_date&order=asc&page=1&limit=20
Authorization: Bearer <token>

Response (200):
{
    "results": [
        {
            "type": "todo",
            "id": 1,
            "title": "검색된 할 일",
            "description": "검색어가 포함된 설명",
            "priority": "높음",
            "category": "업무",
            "due_date": "2024-12-31T23:59:59Z",
            "completed": false,
            "tags": ["중요"],
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": 1,
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 1,
        "pages": 1
    }
}
```

---

## 📝 에러 응답 형식

모든 API에서 에러 발생 시:

```json
{
    "error": "에러 타입",
    "message": "상세 에러 메시지",
    "code": "ERROR_CODE",
    "timestamp": "2024-01-01T00:00:00Z",
    "details": {
        "field": "에러가 발생한 필드",
        "value": "문제가 된 값"
    }
}
```

### 주요 HTTP 상태 코드
- `200`: 성공
- `201`: 생성 성공
- `204`: 삭제 성공 (응답 본문 없음)
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `404`: 리소스 없음
- `422`: 유효성 검증 실패
- `500`: 서버 내부 오류