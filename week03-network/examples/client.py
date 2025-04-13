import socket

def run_client():
    # 서버 연결 정보 설정
    HOST = '127.0.0.1'  # localhost
    PORT = 65432        # 포트 번호

    try:
        # 소켓 생성
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 서버에 연결
            s.connect((HOST, PORT))
            
            while True:
                # 사용자 입력 받기
                message = input("서버로 보낼 메시지를 입력하세요 (종료하려면 'quit' 입력): ")
                
                if message.lower() == 'quit':
                    break
                
                # 메시지 전송
                s.sendall(message.encode())
                
                # 서버로부터 응답 받기
                data = s.recv(1024)
                print(f'서버로부터 받은 응답: {data.decode()}')
                
    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다.")
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    run_client() 