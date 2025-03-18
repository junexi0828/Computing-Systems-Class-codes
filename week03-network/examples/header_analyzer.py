import requests
import json
from tabulate import tabulate  # pip install tabulate

def analyze_headers(url):
    """웹사이트의 HTTP 헤더를 분석하는 함수"""
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        # 웹사이트에 헤더 요청
        response = requests.head(url, timeout=5)
        headers = dict(response.headers)
        
        return {
            'url': url,
            'status_code': response.status_code,
            'headers': headers,
            'success': True
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'success': False
        }

def check_security_headers(headers):
    """보안 관련 HTTP 헤더를 확인하는 함수"""
    security_headers = {
        'Strict-Transport-Security': '전송 계층 보안 강화 (HSTS)',
        'Content-Security-Policy': '콘텐츠 보안 정책',
        'X-Content-Type-Options': '콘텐츠 타입 스니핑 방지',
        'X-Frame-Options': '클릭재킹 방지',
        'X-XSS-Protection': 'XSS 방어',
        'Referrer-Policy': '리퍼러 정보 제어'
    }
    
    results = []
    for header, description in security_headers.items():
        if header in headers:
            status = "✅ 설정됨"
            value = headers[header]
        else:
            status = "❌ 없음"
            value = "N/A"
            
        results.append([header, description, status, value])
        
    return results

def main():
    print("=== 웹 헤더 분석기 ===")
    print("웹사이트의 HTTP 헤더를 분석하여 서버 정보와 보안 설정을 확인합니다.")
    
    while True:
        url = input("\n분석할 웹사이트 URL 입력 (종료: exit): ")
        if url.lower() == 'exit':
            break
            
        print(f"\n{url} 분석 중...")
        result = analyze_headers(url)
        
        if result['success']:
            headers = result['headers']
            
            print(f"\n상태 코드: {result['status_code']}")
            
            # 서버 정보 출력
            print("\n== 서버 정보 ==")
            server_info = [
                ["서버 종류", headers.get('Server', 'Unknown')],
                ["콘텐츠 타입", headers.get('Content-Type', 'Unknown')],
                ["연결 유형", headers.get('Connection', 'Unknown')],
                ["쿠키 사용", "Yes" if 'Set-Cookie' in headers else "No"]
            ]
            print(tabulate(server_info, tablefmt="simple"))
            
            # 보안 헤더 분석
            print("\n== 보안 헤더 분석 ==")
            security_results = check_security_headers(headers)
            print(tabulate(security_results, headers=["헤더", "설명", "상태", "값"], tablefmt="simple"))
            
            # 모든 헤더 출력 옵션
            show_all = input("\n모든 헤더를 보시겠습니까? (y/n): ")
            if show_all.lower() == 'y':
                print("\n== 모든 HTTP 헤더 ==")
                all_headers = [[k, v] for k, v in headers.items()]
                print(tabulate(all_headers, headers=["헤더", "값"], tablefmt="simple"))
                
        else:
            print(f"오류 발생: {result['error']}")
            
        print("\n분석 완료!")

if __name__ == "__main__":
    main() 