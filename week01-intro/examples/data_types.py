"""
Python 기본 데이터 타입 예제
이 프로그램은 Python의 기본적인 데이터 타입과 연산을 보여줍니다.
"""

def demonstrate_numbers():
    # 정수형(int)
    x = 10
    y = 3
    print(f"정수 연산:")
    print(f"x = {x}, y = {y}")
    print(f"덧셈: {x + y}")
    print(f"뺄셈: {x - y}")
    print(f"곱셈: {x * y}")
    print(f"나눗셈: {x / y}")
    print(f"몫: {x // y}")
    print(f"나머지: {x % y}")
    print()

def demonstrate_strings():
    # 문자열(str)
    first_name = "홍"
    last_name = "길동"
    full_name = first_name + last_name
    print(f"문자열 연산:")
    print(f"이름: {full_name}")
    print(f"이름 길이: {len(full_name)}자")
    print(f"이름 반복: {full_name * 3}")
    print()

def demonstrate_lists():
    # 리스트(list)
    numbers = [1, 2, 3, 4, 5]
    fruits = ["사과", "바나나", "오렌지"]
    print(f"리스트 연산:")
    print(f"숫자 리스트: {numbers}")
    print(f"과일 리스트: {fruits}")
    print(f"첫 번째 숫자: {numbers[0]}")
    print(f"마지막 과일: {fruits[-1]}")
    
    # 리스트 수정
    numbers.append(6)
    fruits.insert(1, "포도")
    print(f"수정된 숫자 리스트: {numbers}")
    print(f"수정된 과일 리스트: {fruits}")
    print()

def demonstrate_dictionaries():
    # 딕셔너리(dict)
    student = {
        "name": "홍길동",
        "age": 20,
        "major": "산업공학",
        "grades": {"python": 95, "math": 90, "english": 85}
    }
    print(f"딕셔너리 연산:")
    print(f"학생 정보: {student}")
    print(f"이름: {student['name']}")
    print(f"Python 점수: {student['grades']['python']}")

def main():
    demonstrate_numbers()
    demonstrate_strings()
    demonstrate_lists()
    demonstrate_dictionaries()

if __name__ == "__main__":
    main() 