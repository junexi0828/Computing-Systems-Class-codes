import requests

api_url = "http://api.open-notify.org/iss-now.json"
response = requests.get(api_url)       # API에 GET 요청 전송
if response.status_code == 200:        # HTTP 200 OK 인지 확인
    data = response.json()             # 응답 본문을 JSON 파싱 (dict로 변환)
    position = data["iss_position"]    # JSON 내 위치 정보 부분
    lat = position["latitude"]
    lon = position["longitude"]
    print(f"ISS 현재 위치 - 위도: {lat}, 경도: {lon}")
else:
    print(f"API 요청 실패: 상태 코드 {response.status_code}")
    

{"message": "success", 
 "iss_position": {
     "latitude": "-48.8902", 
     "longitude": "-24.6041"}, 
 "timestamp": 1743064018}