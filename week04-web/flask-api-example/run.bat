@echo off
echo Flask API 예제를 Docker로 실행합니다...

REM Docker 이미지 빌드
docker build -t flask-api-example .

REM 컨테이너 실행
docker run -p 5000:5000 flask-api-example

pause 