import socket
import threading

def handle_client(client_socket, addr):
    """클라이언트와의 통신을 처리하는 함수"""
    print(f"클라이언트 연결됨: {addr}")
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"클라이언트 {addr} 연결 종료")
                break
                
            print(f"클라이언트 {addr}: {message}")
            
            # 메시지 처리 및 응답
            response = f"서버 응답: '{message}' 메시지를 받았습니다."
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"클라이언트 처리 중 오류: {e}")
    finally:
        client_socket.close()

def start_server():
    """서버를 시작하고 클라이언트 연결을 기다리는 함수"""
    # 서버 소켓 생성 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 소켓 재사용 옵션 설정
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 로컬호스트의 12345 포트에 바인딩
    server_socket.bind(('127.0.0.1', 12345))
    
    # 연결 대기 (최대 5개 연결 대기열)
    server_socket.listen(5)
    print("서버가 시작되었습니다. 클라이언트 연결을 기다립니다...")
    
    try:
        while True:
            # 클라이언트 연결 수락
            client_socket, addr = server_socket.accept()
            
            # 각 클라이언트를 위한 스레드 생성
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("서버를 종료합니다.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server() 