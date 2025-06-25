#!/bin/bash

# 컨테이너 시작 시 실행 스크립트
set -e

echo "🚀 Todo App 컨테이너 시작 중..."

# 데이터베이스 연결 대기
echo "📊 데이터베이스 연결 확인 중..."
until mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
    echo "⏳ 데이터베이스 연결 대기 중..."
    sleep 2
done
echo "✅ 데이터베이스 연결 성공"

# 데이터베이스 마이그레이션 (선택사항)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "🔄 데이터베이스 마이그레이션 실행 중..."
    flask db upgrade
    echo "✅ 마이그레이션 완료"
fi

# gunicorn으로 애플리케이션 실행
echo "🌐 Flask 애플리케이션 시작 중..."
exec gunicorn -b 0.0.0.0:5000 app:app