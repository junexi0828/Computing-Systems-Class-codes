import socket
import time
import statistics
from datetime import datetime

def check_response_time(host='127.0.0.1', port=65432, num_requests=10):
    response_times = []
    successful_requests = 0
    failed_requests = 0
    
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}에 응답 시간 체크 시작")
    print(f"서버 주소: {host}:{port}")
    print(f"요청 횟수: {num_requests}\n")
    
    for i in range(num_requests):
        try:
            # 소켓 생성
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                start_time = time.time()
                
                # 연결 시도
                s.connect((host, port))
                
                # 테스트 메시지 전송
                test_message = "ping"
                s.sendall(test_message.encode())
                
                # 응답 대기
                data = s.recv(1024)
                
                # 응답 시간 계산
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # 밀리초 단위로 변환
                
                response_times.append(response_time)
                successful_requests += 1
                
                print(f"요청 {i+1}: {response_time:.2f}ms")
                
        except ConnectionRefusedError:
            print(f"요청 {i+1}: 서버에 연결할 수 없습니다.")
            failed_requests += 1
        except Exception as e:
            print(f"요청 {i+1}: 에러 발생 - {e}")
            failed_requests += 1
        
        # 각 요청 사이에 잠시 대기
        time.sleep(0.1)
    
    # 통계 계산 및 출력
    if response_times:
        print("\n=== 테스트 결과 ===")
        print(f"성공한 요청: {successful_requests}")
        print(f"실패한 요청: {failed_requests}")
        print(f"최소 응답 시간: {min(response_times):.2f}ms")
        print(f"최대 응답 시간: {max(response_times):.2f}ms")
        print(f"평균 응답 시간: {statistics.mean(response_times):.2f}ms")
        print(f"중간값 응답 시간: {statistics.median(response_times):.2f}ms")
        if len(response_times) > 1:
            print(f"표준 편차: {statistics.stdev(response_times):.2f}ms")
    else:
        print("\n모든 요청이 실패했습니다.")

if __name__ == "__main__":
    try:
        check_response_time()
    except KeyboardInterrupt:
        print("\n사용자가 프로그램을 중단했습니다.") 