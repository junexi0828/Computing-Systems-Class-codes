# 🚀 프론트엔드-백엔드 연동 개발 환경 설정

## 📋 개요
React + Vite 프론트엔드와 Flask 백엔드 API를 연동하여 개발하는 환경 설정 가이드입니다.

## ⚙️ 설정 완료 사항

### 1. Vite 프록시 설정 ✅
- `frontend/vite.config.ts`에 Flask 백엔드 프록시 설정 추가
- `/api` 경로로 들어오는 모든 요청을 `http://localhost:5000`으로 전달
- 개발 서버 포트: 3000

### 2. Flask CORS 설정 ✅
- `app.py`에 구체적인 CORS 설정 추가
- 프론트엔드 개발 서버(`localhost:3000`)에서의 요청 허용
- JWT 토큰을 포함한 모든 HTTP 메서드 허용

## 🚀 개발 환경 실행 방법

### 백엔드 실행 (Flask)
```bash
# Docker Compose로 백엔드 실행
docker-compose up -d

# 또는 로컬에서 직접 실행
cd todo-app
python app.py
```

### 프론트엔드 실행 (React + Vite)
```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치 (최초 1회)
npm install

# 개발 서버 실행
npm run dev
```

## 🌐 접속 주소

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:5000
- **API 문서**: http://localhost:5000 (루트 경로)

## 🔧 프록시 설정 상세

### Vite 설정 (`frontend/vite.config.ts`)
```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path.replace(/^\/api/, '/api')
    }
  }
}
```

### Flask CORS 설정 (`app.py`)
```python
CORS(app,
     origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])
```

## 📡 API 연동 구조

### 프론트엔드 API 호출
```typescript
// frontend/src/services/api.ts
export const api = axios.create({
  baseURL: '/api',  // Vite 프록시를 통해 localhost:5000으로 전달
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 실제 요청 흐름
1. 프론트엔드에서 `GET /api/todos` 요청
2. Vite 개발 서버가 요청을 가로챔
3. 프록시 설정에 따라 `http://localhost:5000/api/todos`로 전달
4. Flask 백엔드에서 요청 처리 후 응답
5. Vite가 응답을 프론트엔드로 전달

## 🧪 테스트 방법

### 1. 백엔드 API 테스트
```bash
# 헬스체크
curl http://localhost:5000/health

# API 엔드포인트 확인
curl http://localhost:5000/
```

### 2. 프론트엔드-백엔드 연동 테스트
```bash
# 프론트엔드 개발 서버에서 API 호출 테스트
curl http://localhost:3000/api/health
```

### 3. 브라우저에서 테스트
1. http://localhost:3000 접속
2. 개발자 도구 → Network 탭 확인
3. API 요청이 정상적으로 전달되는지 확인

## 🔍 문제 해결

### 1. CORS 오류 발생 시
- Flask 서버가 실행 중인지 확인
- CORS 설정이 올바른지 확인
- 브라우저 캐시 삭제

### 2. 프록시 오류 발생 시
- Vite 개발 서버 재시작
- 백엔드 서버가 5000번 포트에서 실행 중인지 확인
- 방화벽 설정 확인

### 3. JWT 토큰 오류 시
- localStorage에서 토큰 확인
- 토큰 만료 여부 확인
- 백엔드 JWT 설정 확인

## 📝 개발 팁

1. **동시 실행**: 백엔드와 프론트엔드를 별도 터미널에서 동시 실행
2. **핫 리로드**: Vite의 핫 리로드 기능으로 프론트엔드 변경사항 즉시 반영
3. **API 테스트**: Postman이나 curl로 백엔드 API 직접 테스트 가능
4. **로그 확인**: Docker Compose 로그로 백엔드 상태 모니터링

## 🚀 프로덕션 배포

프로덕션 환경에서는:
1. 프론트엔드를 빌드하여 정적 파일 생성
2. Flask에서 정적 파일 서빙
3. 프록시 설정 제거 (불필요)
4. CORS 설정을 실제 도메인으로 변경