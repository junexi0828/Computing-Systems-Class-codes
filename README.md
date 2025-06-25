# 📌 TodoFlow - 통합 Todo List 플랫폼

## 서비스 개요
- **서비스명**: TodoFlow
- **목적**: 실무형 Todo 관리, 태그/우선순위/통계/검색 등 고도화 기능 제공
- **주요 기능**: JWT 인증, 태그 시스템, 통계, 검색, 반응형 UI, Docker 자동화, CI/CD
- **기술 스택**: React(Vite) + Flask + MySQL + Docker + Nginx + GitHub Actions

---

# 🧱 시스템 아키텍처
- **전체 구조**: Frontend(React) ↔ Nginx(프록시) ↔ Backend(Flask) ↔ DB(MySQL)
- **계층별 설명**:
  - Presentation: React SPA (frontend/src/)
  - API Gateway: Nginx (frontend/nginx.conf)
  - Application: Flask REST API (todo-app/routes/)
  - Data: MySQL (db/init.sql)
- **서비스 흐름**: 클라이언트 → Nginx → /api는 Flask, 그 외는 정적 파일 → DB
- ![시스템 아키텍처](docs/system_architecture.png)
- 🔗 매핑: [`frontend/src/`](frontend/src/), [`todo-app/routes/`](todo-app/routes/), [`docker-compose.yml`](docker-compose.yml)
- 🖼️ **원본(drawio)**: [docs/system_architecture.drawio](docs/system_architecture.drawio)

---

# 🗃️ ERD (데이터 모델)
- **주요 테이블**: User, Todo, Tag, TodoTag
- **관계**: User-1:N-Todo, Todo-N:M-Tag (TodoTag)
- **PK/FK/속성**: id, email, username, password_hash, created_at 등
- ![ERD](docs/erd.png)
- 🔗 매핑: [`todo-app/models/`](todo-app/models/), [`db/init.sql`](db/init.sql)
- 🖼️ **원본(drawio)**: [docs/erd.drawio](docs/erd.drawio)

---

# 🔄 API 흐름도
- **로그인 → JWT 발급 → 인증 → Todo 처리**
- **API 요청/응답 구조**: HTTP Method + 경로 + JWT 인증
- **인증/인가**: JWT 토큰, Interceptor, 미인증 시 401 반환
- ![API 흐름도](docs/api_flow.png)
- 🔗 매핑: [`todo-app/routes/`](todo-app/routes/), [`frontend/src/services/api.ts`](frontend/src/services/api.ts)
- 🖼️ **원본(drawio)**: [docs/api_flow.drawio](docs/api_flow.drawio)

---

# ⚙️ CI/CD 파이프라인
- **GitHub Actions**: push → build → test → docker image → deploy
- **단계**: 자동 빌드/테스트, 병렬 처리, 승인 필요 시 manual trigger
- ![CI/CD 파이프라인](docs/cicd_pipeline.png)
- 🔗 매핑: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), [`Dockerfile`](todo-app/Dockerfile)

---

# 🌐 네트워크 구성도
- **도커 내부망**: frontend(3000), backend(5000), db(3306)
- **프록시 구조**: Nginx가 /api는 Flask로, 나머지는 React로 전달
- ![네트워크 구성도](docs/network.png)
- 🔗 매핑: [`docker-compose.yml`](docker-compose.yml), [`frontend/nginx.conf`](frontend/nginx.conf)
- 🖼️ **원본(drawio)**: [docs/network.drawio](docs/network.drawio)

---

# 🧪 테스트 & 보안
- **JWT 인증**: 모든 API에 적용, 미인증 시 401 반환
- **API 보호**: 사용자별 데이터 분리, 태그/할 일 접근 제한
- **자동화 테스트**: Docker 기반 setup.sh, healthcheck, API 테스트 스크립트
- **보안**: 비밀번호 해싱(bcrypt), 환경변수 관리, CORS 제한

---

# 📦 실행 방법
```bash
git clone https://github.com/your-repo.git
cd todo-app
bash scripts/setup.sh
```

---

# 🧩 프로젝트 구조
```
todo-app/
├── models/           # 데이터베이스 모델
├── routes/           # API 라우트
├── frontend/         # React + Vite + Nginx
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src/
├── db/               # 초기 SQL 스크립트
├── scripts/          # 자동화 셸 스크립트
├── docs/             # 기술 문서 및 다이어그램
├── docker-compose.yml
├── README.md
```

---

# 📁 문서 매핑 푸터

⸻

📎 **관련 문서 링크**
- 🧱 시스템 아키텍처: [docs/system_architecture.png](docs/system_architecture.png)
- 🗃️ 데이터 모델(ERD): [docs/erd.png](docs/erd.png)
- 🔄 API 흐름도: [docs/api_flow.png](docs/api_flow.png)
- ⚙️ CI/CD 파이프라인: [docs/cicd_pipeline.png](docs/cicd_pipeline.png)
- 🌐 네트워크 구성도: [docs/network.png](docs/network.png)

⸻

📌 **모든 다이어그램은 draw.io 또는 PNG로 작성하여 docs/ 디렉토리에 포함**
📌 **실제 코드 파일 경로와 다이어그램 내용을 정확히 매핑하여 체계적인 문서화를 달성**
📌 **이 README는 과제 제출 시 "설계 → 구현 → 테스트 → 배포"의 전체 흐름을 시각적으로 보여주는 중심 문서로 활용됨**

---

# ✅ 구현된 추가/고도화 기능
- JWT 기반 사용자 인증 및 권한 분리
- 태그 시스템 (사용자별 태그, 색상, 중복 방지)
- 통계/검색/우선순위/카테고리/마감일/완료 토글 등 고급 Todo 관리
- API/단위 테스트 자동화, healthcheck, setup.sh 완전 자동화
- Docker Compose 기반 완전 자동화 배포
- React + TypeScript + Vite + Tailwind CSS 프론트엔드
- Nginx SPA 라우팅 및 API 프록시, CORS 보안
- CI/CD 파이프라인 (GitHub Actions)
- 코드 품질 관리(모듈화, 예외처리, 환경변수, 보안)

---

# 📎 프로젝트 푸터

- **프로젝트명**: TodoFlow
- **버전**: 1.0.0
- **저작권**: © 2024 TodoFlow Team. All rights reserved.
- **라이선스**: MIT License
- **문의**: juns@example.com (팀장/담당자)
- **기여 가이드**: [CONTRIBUTING.md](CONTRIBUTING.md) (오픈소스/팀 협업 시)
- **문서/다이어그램**: docs/ 디렉토리 내 drawio 및 PNG 파일 참조
- **최종 빌드/배포일**: 2024-06-25
- **GitHub**: https://github.com/your-repo

---

> 본 문서는 과제 제출 및 실무/포트폴리오/팀 협업/오픈소스 배포 등 다양한 목적에 맞춰 체계적으로 작성되었습니다.
>
> 모든 기술 문서, 다이어그램, 코드 품질 관리, 자동화 요소가 실제 구현과 1:1로 매핑되어 있습니다.
>
> 추가 문의/기여/협업 제안은 언제든 연락 바랍니다.