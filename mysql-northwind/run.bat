@echo off
chcp 65001 > nul
echo [Northwind MySQL 데이터베이스 시작 중...]

REM Docker 컨테이너가 이미 실행 중인지 확인
docker ps | findstr "northwind-mysql" > nul
if %errorlevel% equ 0 (
    echo [이미 Northwind MySQL이 실행 중입니다.]
    echo.
    echo [연결 정보]
    echo - 호스트: 127.0.0.1
    echo - 포트: 3306
    echo - 사용자: northwind_user
    echo - 비밀번호: northwind_password
    echo - 데이터베이스: northwind
    echo.
    pause
    exit /b
)

REM Docker Compose 실행
echo [Docker 컨테이너를 시작합니다...]
docker-compose up

if %errorlevel% neq 0 (
    echo [Docker 컨테이너 시작 중 오류가 발생했습니다.]
    echo [Docker Desktop이 실행 중인지 확인해주세요.]
    pause
    exit /b
)

echo [Northwind MySQL이 성공적으로 시작되었습니다!]
echo.
echo [연결 정보]
echo - 호스트: 127.0.0.1
echo - 포트: 3306
echo - 사용자: northwind_user
echo - 비밀번호: northwind_password
echo - 데이터베이스: northwind
echo.
echo [MySQL Workbench에서 위 정보로 연결할 수 있습니다.]
pause 