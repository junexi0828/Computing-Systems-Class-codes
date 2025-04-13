import socket

def run_server():
    # 서버 설정
    HOST = '127.0.0.1'  # localhost
    PORT = 65432        # 포트 번호

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 소켓 옵션 설정
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 주소와 포트 바인딩
        s.bind((HOST, PORT))
        # 연결 대기
        s.listen()
        
        print(f'서버가 {HOST}:{PORT}에서 실행 중입니다...')
        
        while True:
            try:
                # 클라이언트 연결 수락
                conn, addr = s.accept()
                with conn:
                    print(f'클라이언트가 연결되었습니다: {addr}')
                    
                    while True:
                        # 데이터 수신
                        data = conn.recv(1024)
                        if not data:
                            break
                            
                        # 받은 메시지 출력
                        print(f'클라이언트로부터 받은 메시지: {data.decode()}')
                        
                        # 응답 전송
                        response = f"서버가 메시지를 받았습니다: {data.decode()}"
                        conn.sendall(response.encode())
                        
            except Exception as e:
                print(f"에러 발생: {e}")

if __name__ == "__main__":
    run_server() 