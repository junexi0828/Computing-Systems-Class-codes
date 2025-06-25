#!/usr/bin/env python3
"""
샘플 사용자 계정 생성 스크립트
"""

import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:8000/api"

def create_sample_users():
    """샘플 사용자 계정들을 생성합니다."""

    sample_users = [
        {
            "email": "admin@example.com",
            "password": "password123",
            "name": "관리자"
        },
        {
            "email": "user1@example.com",
            "password": "password123",
            "name": "사용자1"
        },
        {
            "email": "user2@example.com",
            "password": "password123",
            "name": "사용자2"
        }
    ]

    print("🚀 샘플 사용자 계정 생성 중...")

    for user in sample_users:
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json=user,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 201:
                print(f"✅ {user['email']} 계정 생성 성공")
            elif response.status_code == 400:
                print(f"⚠️  {user['email']} 계정이 이미 존재합니다")
            else:
                print(f"❌ {user['email']} 계정 생성 실패: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print(f"❌ 서버 연결 실패. 백엔드가 실행 중인지 확인해주세요.")
            return
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

    print("\n🎉 샘플 계정 생성 완료!")
    print("\n📋 사용 가능한 계정:")
    for user in sample_users:
        print(f"   이메일: {user['email']}")
        print(f"   비밀번호: {user['password']}")
        print()

if __name__ == "__main__":
    create_sample_users()