from datetime import datetime
import requests


class WeatherResult(dict):

    def __init__(self, city: str, humidity="", time_stamp="",
                 temperature="", errors=False, country=""):
        super().__init__()
        self.city = city
        self.country = country
        self.humidity = humidity
        self.time_stamp = time_stamp
        self.temperature = temperature
        self.errors = errors


class Weather:

    def __init__(self, api_token: str):
        self.api = api_token

    def lon_lat(self, city: str):
        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.api}"
        )
        if response.status_code != 200:
            return 0, 0
        data = response.json()
        if not data:
            return 0, 0
        lon = data[0].get("lon")
        lat = data[0].get("lat")
        return lon, lat

    def get(self, city: str):
        lon, lat = self.lon_lat(city)
        if (lon, lat) == (0, 0):
            return WeatherResult(city=city, errors=True)
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api}&units=metric"
        )
        if response.status_code != 200:
            return WeatherResult(city=city, errors=True)
        data = response.json()
        temp = data["main"].get("temp")
        hum = data["main"].get("humidity")
        country = data["sys"].get("country")
        actual_time = datetime.now().strftime("%H:%M")
        return WeatherResult(city, humidity=hum, time_stamp=actual_time, temperature=temp, country=country)
