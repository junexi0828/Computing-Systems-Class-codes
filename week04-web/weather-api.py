import requests
import json
from datetime import datetime

class OpenWeatherFreeAPI:
    """
    OpenWeather의 무료 API를 사용하여 날씨 정보를 가져오는 클래스
    Current Weather Data API와 5 Day / 3 Hour Forecast API 활용
    """
    
    def __init__(self, api_key):
        """
        OpenWeatherFreeAPI 클래스 초기화
        
        Args:
            api_key (str): OpenWeather API 키
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, lat=None, lon=None, city=None, units="metric", lang="kr"):
        """
        현재 날씨 정보를 가져옵니다.
        
        Args:
            lat (float, optional): 위도
            lon (float, optional): 경도
            city (str, optional): 도시 이름
            units (str, optional): 측정 단위 (standard, metric, imperial). 기본값 "metric".
            lang (str, optional): 언어 설정. 기본값 "kr".
            
        Returns:
            dict: 날씨 데이터
        """
        url = f"{self.base_url}/weather"
        
        params = {
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        # 위치 정보 설정 (위도/경도 또는 도시 이름)
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        elif city is not None:
            params["q"] = city
        else:
            raise ValueError("위도와 경도 또는 도시 이름을 제공해야 합니다.")
            
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    
    def get_forecast(self, lat=None, lon=None, city=None, units="metric", lang="kr"):
        """
        5일 예보 정보(3시간 간격)를 가져옵니다.
        
        Args:
            lat (float, optional): 위도
            lon (float, optional): 경도
            city (str, optional): 도시 이름
            units (str, optional): 측정 단위. 기본값 "metric".
            lang (str, optional): 언어 설정. 기본값 "kr".
            
        Returns:
            dict: 날씨 예보 데이터
        """
        url = f"{self.base_url}/forecast"
        
        params = {
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        # 위치 정보 설정 (위도/경도 또는 도시 이름)
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        elif city is not None:
            params["q"] = city
        else:
            raise ValueError("위도와 경도 또는 도시 이름을 제공해야 합니다.")
            
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    def display_current_weather(self, weather_data):
        """
        현재 날씨 정보를 출력합니다.
        
        Args:
            weather_data (dict): 날씨 데이터
        """
        if not weather_data:
            print("날씨 데이터가 없습니다.")
            return
        
        print("\n===== 현재 날씨 정보 =====")
        print(f"위치: {weather_data['name']}, {weather_data.get('sys', {}).get('country', '')}")
        print(f"날짜: {datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        if 'weather' in weather_data and len(weather_data['weather']) > 0:
            print(f"날씨: {weather_data['weather'][0]['description']}")
            
        if 'main' in weather_data:
            main = weather_data['main']
            print(f"온도: {main.get('temp')}°C")
            print(f"체감 온도: {main.get('feels_like')}°C")
            print(f"최저 온도: {main.get('temp_min')}°C")
            print(f"최고 온도: {main.get('temp_max')}°C")
            print(f"기압: {main.get('pressure')} hPa")
            print(f"습도: {main.get('humidity')}%")
            
        if 'wind' in weather_data:
            wind = weather_data['wind']
            print(f"풍속: {wind.get('speed')} m/s")
            print(f"풍향: {wind.get('deg')}°")
            
        if 'clouds' in weather_data:
            print(f"구름: {weather_data['clouds'].get('all')}%")
            
        if 'visibility' in weather_data:
            print(f"가시성: {weather_data['visibility']} m")
            
        if 'sys' in weather_data:
            sys = weather_data['sys']
            sunrise = datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%H:%M:%S')
            print(f"일출: {sunrise}")
            print(f"일몰: {sunset}")
            
    def display_forecast(self, forecast_data):
        """
        날씨 예보 정보를 출력합니다.
        
        Args:
            forecast_data (dict): 날씨 예보 데이터
        """
        if not forecast_data or 'list' not in forecast_data:
            print("예보 데이터가 없습니다.")
            return
        
        forecasts = forecast_data['list']
        city = forecast_data.get('city', {}).get('name', '알 수 없는 위치')
        
        print(f"\n===== {city}의 5일 예보 (3시간 간격) =====")
        
        # 날짜별로 예보 정리
        daily_forecasts = {}
        
        for item in forecasts:
            date = datetime.fromtimestamp(item['dt'])
            day_str = date.strftime('%Y-%m-%d')
            time_str = date.strftime('%H:%M')
            
            if day_str not in daily_forecasts:
                daily_forecasts[day_str] = []
                
            weather_desc = item['weather'][0]['description'] if 'weather' in item and len(item['weather']) > 0 else "정보 없음"
            temp = item['main']['temp'] if 'main' in item else "정보 없음"
            
            daily_forecasts[day_str].append({
                'time': time_str,
                'temp': temp,
                'weather': weather_desc,
                'humidity': item['main'].get('humidity', '정보 없음') if 'main' in item else '정보 없음',
                'wind_speed': item['wind'].get('speed', '정보 없음') if 'wind' in item else '정보 없음'
            })
        
        # 날짜별로 예보 출력
        for day, items in daily_forecasts.items():
            print(f"\n[{day}]")
            
            for item in items:
                print(f"  {item['time']}: {item['weather']}, 온도 {item['temp']}°C, 습도 {item['humidity']}%, 풍속 {item['wind_speed']} m/s")

    def get_air_pollution(self, lat, lon):
        """
        특정 위치의 대기 오염 정보를 가져옵니다.
        
        Args:
            lat (float): 위도
            lon (float): 경도
            
        Returns:
            dict: 대기 오염 데이터
        """
        url = f"{self.base_url}/air_pollution"
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    def display_air_pollution(self, pollution_data):
        """
        대기 오염 정보를 출력합니다.
        
        Args:
            pollution_data (dict): 대기 오염 데이터
        """
        if not pollution_data or 'list' not in pollution_data or not pollution_data['list']:
            print("대기 오염 데이터가 없습니다.")
            return
        
        data = pollution_data['list'][0]  # 첫 번째 데이터
        
        print("\n===== 대기 오염 정보 =====")
        
        if 'dt' in data:
            print(f"날짜: {datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')}")
            
        if 'main' in data and 'aqi' in data['main']:
            aqi = data['main']['aqi']
            aqi_desc = ["좋음", "보통", "약간 나쁨", "나쁨", "매우 나쁨"][aqi - 1] if 1 <= aqi <= 5 else "알 수 없음"
            print(f"대기질 지수: {aqi} ({aqi_desc})")
            
        if 'components' in data:
            comp = data['components']
            print(f"일산화탄소(CO): {comp.get('co', '정보 없음')} μg/m³")
            print(f"이산화질소(NO2): {comp.get('no2', '정보 없음')} μg/m³")
            print(f"오존(O3): {comp.get('o3', '정보 없음')} μg/m³")
            print(f"이산화황(SO2): {comp.get('so2', '정보 없음')} μg/m³")
            print(f"미세먼지(PM10): {comp.get('pm10', '정보 없음')} μg/m³")
            print(f"초미세먼지(PM2.5): {comp.get('pm2_5', '정보 없음')} μg/m³")


# 사용 예시
if __name__ == "__main__":
    # API 키를 여기에 입력하세요
    API_KEY = "009309b227639bdd1b12baec080518e1"
     
    # 서울의 위도와 경도
    LAT = 37.5683
    LON = 126.9778
    
    # 도시 이름 (위도/경도 대신 사용 가능)
    CITY = "Seoul,KR"
    
    # OpenWeatherFreeAPI 인스턴스 생성
    weather_api = OpenWeatherFreeAPI(API_KEY)
    
    # 방법 1: 위도와 경도로 현재 날씨 가져오기
    weather_data = weather_api.get_current_weather(lat=LAT, lon=LON)
    
    # 방법 2: 도시 이름으로 현재 날씨 가져오기
    # weather_data = weather_api.get_current_weather(city=CITY)
    
    if weather_data:
        # 현재 날씨 출력
        weather_api.display_current_weather(weather_data)
        
        # 날씨 데이터를 JSON 파일로 저장
        with open('current_weather.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=2)
            print("\n현재 날씨 데이터가 'current_weather.json' 파일에 저장되었습니다.")
    
    # 5일 예보 가져오기 (3시간 간격)
    forecast_data = weather_api.get_forecast(lat=LAT, lon=LON)
    
    if forecast_data:
        # 예보 정보 출력
        weather_api.display_forecast(forecast_data)
        
        # 예보 데이터를 JSON 파일로 저장
        with open('forecast_weather.json', 'w', encoding='utf-8') as f:
            json.dump(forecast_data, f, ensure_ascii=False, indent=2)
            print("\n예보 데이터가 'forecast_weather.json' 파일에 저장되었습니다.")
    
    # 대기 오염 정보 가져오기
    pollution_data = weather_api.get_air_pollution(LAT, LON)
    
    if pollution_data:
        # 대기 오염 정보 출력
        weather_api.display_air_pollution(pollution_data)
        
        # 대기 오염 데이터를 JSON 파일로 저장
        with open('air_pollution.json', 'w', encoding='utf-8') as f:
            json.dump(pollution_data, f, ensure_ascii=False, indent=2)
            print("\n대기 오염 데이터가 'air_pollution.json' 파일에 저장되었습니다.")
   
