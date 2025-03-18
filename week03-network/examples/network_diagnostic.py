import socket
import subprocess
import platform
import re
import time

def get_ip_address(domain):
    """도메인 이름으로부터 IP 주소를 조회하는 함수"""
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        return f"도메인 조회 실패: {e}"

def ping_host(host):
    """호스트에 ping을 보내는 함수"""
    # OS에 따라 ping 명령어 옵션 변경
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    count = '4'  # 4개의 ping 패킷 전송
    
    try:
        # ping 명령 실행
        command = ['ping', param, count, host]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ping 실패: {e.stderr}"

def parse_ping_result(ping_output, os_type):
    """ping 결과에서 시간 정보를 추출하는 함수"""
    times = []
    
    if os_type == 'windows':
        # Windows 형식의 ping 출력 파싱
        pattern = r'시간=(\d+)ms|time[=<](\d+)ms'
    else:
        # Linux/Mac 형식의 ping 출력 파싱
        pattern = r'time=(\d+\.?\d*) ms'
    
    matches = re.findall(pattern, ping_output)
    
    for match in matches:
        if isinstance(match, tuple):
            # Windows 패턴에서는 튜플로 반환될 수 있음
            time_str = next((m for m in match if m), None)
        else:
            time_str = match
            
        if time_str:
            times.append(float(time_str))
    
    return times

def trace_route(host):
    """목적지까지의 경로를 추적하는 함수"""
    command = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
    
    try:
        result = subprocess.run([command, host], text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Traceroute 실패: {e.stderr}"
    except FileNotFoundError:
        return f"{command} 명령을 찾을 수 없습니다."

def network_diagnostics():
    """네트워크 진단을 수행하는 메인 함수"""
    print("=== 간단한 네트워크 진단 도구 ===")
    
    while True:
        domain = input("\n진단할 도메인 입력 (종료: exit): ")
        if domain.lower() == 'exit':
            break
            
        print(f"\n{domain} 진단을 시작합니다...")
        
        # DNS 조회
        print("\n1. DNS 조회 중...")
        ip = get_ip_address(domain)
        print(f"   도메인: {domain}")
        print(f"   IP 주소: {ip}")
        
        if 'failed' in ip.lower():
            print("   유효한 도메인이 아닙니다. 다른 도메인을 입력하세요.")
            continue
        
        # Ping 테스트
        print("\n2. Ping 테스트 중...")
        os_type = platform.system().lower()
        ping_result = ping_host(domain)
        print(ping_result)
        
        ping_times = parse_ping_result(ping_result, os_type)
        if ping_times:
            avg_time = sum(ping_times) / len(ping_times)
            print(f"   평균 응답 시간: {avg_time:.2f} ms")
            
            # 응답 시간 평가
            if avg_time < 50:
                print("   네트워크 상태: 매우 좋음")
            elif avg_time < 100:
                print("   네트워크 상태: 양호")
            elif avg_time < 200:
                print("   네트워크 상태: 보통")
            else:
                print("   네트워크 상태: 나쁨 (지연 발생)")
        
        # 경로 추적 (선택 사항)
        trace_option = input("\n경로 추적을 하시겠습니까? (y/n): ")
        if trace_option.lower() == 'y':
            print("\n3. 경로 추적 중...")
            trace_result = trace_route(domain)
            print(trace_result)
            
        print("\n진단 완료!")

if __name__ == "__main__":
    network_diagnostics() 