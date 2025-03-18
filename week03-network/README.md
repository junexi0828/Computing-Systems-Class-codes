# 3주차: 네트워크 통신 기초

## 학습 목표
- 네트워크 통신의 기본 개념 이해
- Python을 이용한 네트워크 프로그래밍 실습
- HTTP 통신과 소켓 프로그래밍 학습

## 실습 내용

### 1. 웹사이트 응답 시간 측정기 (response_time_checker.py)
- requests 라이브러리를 사용한 웹 요청
- 응답 시간 측정 및 시각화
- matplotlib을 이용한 데이터 시각화

### 2. 소켓 통신 채팅 프로그램 (server.py, client.py)
- 소켓 프로그래밍 기초
- 멀티스레딩을 이용한 동시 통신
- 클라이언트-서버 모델 이해

### 3. 네트워크 진단 도구 (network_diagnostic.py)
- DNS 조회 및 IP 주소 확인
- Ping 테스트 및 결과 분석
- 네트워크 경로 추적

### 4. 웹 헤더 분석기 (header_analyzer.py)
- HTTP 헤더 분석
- 웹 서버 보안 설정 확인
- 응답 헤더 정보 해석

## 준비사항
```bash
# 필요한 Python 패키지 설치
pip install requests matplotlib tabulate
```

## 실행 방법
1. 각 예제 코드는 독립적으로 실행 가능합니다.
2. 채팅 프로그램의 경우:
   - 먼저 server.py를 실행
   - 다른 터미널에서 client.py를 실행

## 과제
- [assignment3.md](./assignments/assignment3.md) 파일의 과제를 완료하세요.
- 제출 기한: 다음 주차 수업 시작 전까지 