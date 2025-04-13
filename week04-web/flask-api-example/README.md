# Flask API 예제

이 프로젝트는 Flask를 사용한 간단한 REST API 예제입니다. 도서 정보를 관리하는 API를 제공합니다.

## 기능

- 도서 목록 조회
- 특정 도서 정보 조회
- 새로운 도서 추가

## API 엔드포인트

### 1. 도서 목록 조회
```
GET /api/books
```

응답 예시:
```json
[
    {
        "id": 1,
        "title": "파이썬 프로그래밍",
        "author": "홍길동",
        "year": 2020
    },
    {
        "id": 2,
        "title": "웹 개발의 기초",
        "author": "김철수",
        "year": 2021
    }
]
```

### 2. 특정 도서 조회
```
GET /api/books/<book_id>
```

응답 예시:
```json
{
    "id": 1,
    "title": "파이썬 프로그래밍",
    "author": "홍길동",
    "year": 2020
}
```

오류 응답 (도서를 찾을 수 없는 경우):
```json
{
    "error": "도서를 찾을 수 없습니다."
}
```

### 3. 새 도서 추가
```
POST /api/books
Content-Type: application/json

{
    "title": "새로운 도서",
    "author": "이철수",
    "year": 2024
}
```

응답 예시:
```json
{
    "id": 3,
    "title": "새로운 도서",
    "author": "이철수",
    "year": 2024
}
```

오류 응답 (제목이 없는 경우):
```json
{
    "error": "제목이 필요합니다."
}
```

## API 테스트 방법

### curl 사용

1. 도서 목록 조회:
```bash
curl http://localhost:5000/api/books
```

2. 특정 도서 조회:
```bash
curl http://localhost:5000/api/books/1
```

3. 새 도서 추가:
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"새로운 도서\",\"author\":\"이철수\",\"year\":2024}" http://localhost:5000/api/books
```

### Python requests 사용

```python
import requests

# API 기본 URL
BASE_URL = 'http://localhost:5000/api'

# 도서 목록 조회
response = requests.get(f'{BASE_URL}/books')
print(response.json())

# 특정 도서 조회
response = requests.get(f'{BASE_URL}/books/1')
print(response.json())

# 새 도서 추가
new_book = {
    'title': '새로운 도서',
    'author': '이철수',
    'year': 2024
}
response = requests.post(f'{BASE_URL}/books', json=new_book)
print(response.json())
```

## 실행 방법

### Docker 사용
1. Docker 이미지 빌드:
```bash
docker build -t flask-api-example .
```

2. 컨테이너 실행:
```bash
docker run -p 5000:5000 flask-api-example
```

### 직접 실행
1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 애플리케이션 실행:
```bash
python app.py
```

## 주의사항

- 이 API는 메모리에 데이터를 저장하므로 서버가 재시작되면 데이터가 초기화됩니다.
- 실제 프로덕션 환경에서는 데이터베이스를 사용하는 것이 좋습니다.
- CORS가 활성화되어 있어 모든 도메인에서 API에 접근할 수 있습니다. 