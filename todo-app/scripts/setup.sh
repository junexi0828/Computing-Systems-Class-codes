#!/bin/bash

# Todo App 자동 설정 스크립트
set -e

echo "🚀 Todo App 자동 설정 시작..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Docker 설치 확인
check_docker() {
    print_status "Docker 설치 확인 중..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker가 설치되지 않았습니다. Docker를 먼저 설치해주세요."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose가 설치되지 않았습니다. Docker Compose를 먼저 설치해주세요."
        exit 1
    fi

    print_success "Docker 및 Docker Compose 확인 완료"
}

# 기존 컨테이너 정리
cleanup() {
    print_status "기존 컨테이너 정리 중..."
    docker-compose down --volumes --remove-orphans 2>/dev/null || true
    print_success "기존 컨테이너 정리 완료"
}

# 이미지 빌드
build_images() {
    print_status "Docker 이미지 빌드 중..."
    docker-compose build --no-cache
    print_success "Docker 이미지 빌드 완료"
}

# 서비스 시작
start_services() {
    print_status "서비스 시작 중..."
    docker-compose up -d
    print_success "서비스 시작 완료"
}

# 헬스체크
health_check() {
    print_status "서비스 헬스체크 중..."

    # 데이터베이스 헬스체크
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps db | grep -q "healthy"; then
            print_success "데이터베이스 헬스체크 통과"
            break
        fi

        if [ $attempt -eq $max_attempts ]; then
            print_error "데이터베이스 헬스체크 실패"
            exit 1
        fi

        print_status "데이터베이스 대기 중... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done

    # 웹 서비스 헬스체크
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &>/dev/null; then
            print_success "웹 서비스 헬스체크 통과"
            break
        fi

        if [ $attempt -eq $max_attempts ]; then
            print_error "웹 서비스 헬스체크 실패"
            exit 1
        fi

        print_status "웹 서비스 대기 중... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
}

# API 테스트
test_apis() {
    print_status "API 테스트 중..."

    # Ping API 테스트
    if curl -f http://localhost:8000/ping | grep -q "pong"; then
        print_success "Ping API 테스트 통과"
    else
        print_error "Ping API 테스트 실패"
        exit 1
    fi

    # Health API 테스트
    if curl -f http://localhost:8000/health | grep -q "healthy"; then
        print_success "Health API 테스트 통과"
    else
        print_error "Health API 테스트 실패"
        exit 1
    fi

    # Root API 테스트
    if curl -f http://localhost:8000/ | grep -q "Todo App API"; then
        print_success "Root API 테스트 통과"
    else
        print_error "Root API 테스트 실패"
        exit 1
    fi
}

# 상태 출력
show_status() {
    print_status "서비스 상태 확인 중..."
    docker-compose ps

    echo ""
    print_success "🎉 Todo App 설정 완료!"
    echo ""
    echo "📋 접속 정보:"
    echo "   - 웹 서비스: http://localhost:8000"
    echo "   - 데이터베이스: localhost:13306"
    echo ""
    echo "🔧 유용한 명령어:"
    echo "   - 로그 확인: docker-compose logs -f"
    echo "   - 서비스 중지: docker-compose down"
    echo "   - 서비스 재시작: docker-compose restart"
    echo ""
    echo "🧪 API 테스트:"
    echo "   curl http://localhost:8000/ping"
    echo "   curl http://localhost:8000/health"
    echo "   curl http://localhost:8000/"
}

# 메인 실행
main() {
    echo "=========================================="
    echo "    Todo App 자동 설정 스크립트"
    echo "=========================================="
    echo ""

    check_docker
    cleanup
    build_images
    start_services
    health_check
    test_apis
    show_status
}

# 스크립트 실행
main "$@"