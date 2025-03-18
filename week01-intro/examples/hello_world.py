"""
첫 번째 Python 프로그램
이 프로그램은 기본적인 출력과 입력을 보여줍니다.
"""

def main():
    # 기본 출력
    print("안녕하세요! Python 프로그래밍의 세계에 오신 것을 환영합니다!")
    
    # 사용자 입력 받기
    name = input("당신의 이름을 입력해주세요: ")
    print(f"{name}님, 반갑습니다!")
    
    # 간단한 계산
    birth_year = int(input("출생년도를 입력해주세요: "))
    current_year = 2024
    age = current_year - birth_year + 1
    
    print(f"{name}님의 나이는 {age}세입니다.")

if __name__ == "__main__":
    main() 