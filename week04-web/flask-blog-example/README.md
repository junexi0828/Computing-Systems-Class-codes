# Flask 블로그 예제

이 프로젝트는 Flask를 사용하여 구현한 완전한 블로그 웹 애플리케이션입니다.

## 프로젝트 구조

```
flask-blog-example/
├── app.py                  # 메인 애플리케이션 파일
├── blog.db                 # SQLite 데이터베이스
├── templates/              # 템플릿 파일
│   ├── base.html           # 기본 레이아웃
│   ├── index.html          # 홈페이지 (최신 포스트 목록)
│   ├── register.html       # 회원가입 페이지
│   ├── login.html          # 로그인 페이지
│   ├── new_post.html       # 새 포스트 작성 페이지
│   ├── post_detail.html    # 포스트 상세 페이지
│   ├── edit_post.html      # 포스트 수정 페이지
│   ├── profile.html        # 사용자 프로필 페이지
│   └── search_results.html # 검색 결과 페이지
├── Dockerfile              # Docker 설정 파일
├── requirements.txt        # Python 패키지 의존성
└── README.md               # 프로젝트 설명서
```

## Docker로 실행하기

1. Docker 이미지 빌드:
```bash
docker build -t flask-blog-example .
```

2. 컨테이너 실행:
```bash
docker run -p 5000:5000 flask-blog-example
```

3. 웹 브라우저에서 접속:
- http://localhost:5000

## 주요 기능

### 사용자 관리
- 회원가입
- 로그인/로그아웃
- 사용자 프로필 조회

### 포스트 관리
- 포스트 작성
- 포스트 수정
- 포스트 삭제
- 포스트 상세 보기
- 모든 포스트 목록 보기

### 댓글 기능
- 댓글 작성
- 댓글 삭제

### 검색 기능
- 포스트 제목 및 내용 검색 