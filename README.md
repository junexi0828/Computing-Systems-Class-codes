# 산업공학과 컴퓨터 시스템 실습 코드

이 저장소는 산업공학 전공 학생들을 위한 '컴퓨터 시스템' 15주 강의의 실습 자료와 예제 코드를 제공합니다. Python을 기반으로 컴퓨터 구조, 데이터베이스, 네트워크 프로그래밍, 웹 개발, 컨테이너 기술에 이르는 다양한 주제를 다룹니다.

## 강의 개요
- 대상: 산업공학과 학부생
- 기간: 15주 (주당 3시간 수업)
- 구성: 이론 강의 + Python 실습
- 평가: 이론(40%), 실습(40%), 프로젝트 및 과제(20%)

## 저장소 구조

### 주차별 학습 내용
- **week01-intro**: Python 기초 및 개발 환경 설정
  - examples/
    - hello_world.py: Python 기본 문법 예제
    - data_types.py: Python 데이터 타입 학습
  - assignments/: Python 기초 과제

- **week03-network**: 네트워크 프로그래밍
  - examples/
    - client.py: 클라이언트-서버 통신 예제
    - server.py: 기본 서버 구현
    - network_diagnostic.py: 네트워크 진단 도구
    - header_analyzer.py: HTTP 헤더 분석기
    - response_time_checker.py: 응답 시간 측정 도구
  - assignments/: 네트워크 프로그래밍 과제

- **week04-web**: 웹 개발 기초
  - flask-blog-example/: Flask를 이용한 블로그 예제
    - app.py: 메인 애플리케이션
    - templates/: HTML 템플릿
    - Dockerfile: 컨테이너 설정
    - requirements.txt: 의존성 목록
  - flask-api-example/: REST API 구현 예제
  - weather-api.py: 날씨 API 활용 예제
  - api-tester.py: API 테스트 도구

- **week05-mysql-northwind**: MySQL 데이터베이스 실습
  - northwind.sql: 데이터베이스 스키마
  - northwind-data.sql: 샘플 데이터
  - docker-compose.yml: Docker 환경 설정
  - run.bat: 실행 스크립트

## 개발 환경 설정

### 필수 도구
1. Python 3.x
2. Git
3. Docker (선택사항)
4. MySQL (또는 Docker)
5. Visual Studio Code (권장)

### 기본 설정
1. Git 설치: [다운로드 링크](https://git-scm.com/downloads)
2. GitHub 계정 생성: [GitHub 회원가입](https://github.com/join)
3. 이 저장소 포크하기: 우측 상단의 'Fork' 버튼 클릭
4. 로컬 컴퓨터에 클론하기: `git clone https://github.com/TEAMLAB-Lecture/Computing-Systems-Class-codes.git`

### 과제 제출 방법
1. 자신의 포크된 저장소에서 작업
2. 변경사항 커밋: `git commit -m "과제 1 완료"`
3. GitHub에 푸시: `git push origin main`
4. 필요시 Pull Request 생성하여 피드백 요청

## 참고 자료
- [Python 공식 문서](https://docs.python.org/3/)
- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [MySQL 공식 문서](https://dev.mysql.com/doc/)
- [Docker 공식 문서](https://docs.docker.com/) 