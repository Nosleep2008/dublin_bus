import requests

# API key as a constant
OPEN_WEATHER_API = "ae1cb5df0561ea9915f81e08ce8299fc"


def getCurrentWeather(cityName="Dublin"):
    """Function that get city name (Dublin as default), return current weather info"""
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + OPEN_WEATHER_API

    response = requests.get(url)
    data = response.json()

    # Make sure the request has succeeded
    if response.status_code != 200:
        return None

    # Make sure the input is right
    if data["cod"] != 200:
        return None

    # Return a list of weather id, weather description, current temperature, icon id
    # The sample of icon url: for icon=10d, url = http://openweathermap.org/img/wn/10d@2x.png
    weather_id = data["weather"][0]["id"]
    weather_main = data["weather"][0]["main"]
    temper = int(data["main"]["temp"] - 273.15)
    icon = data["weather"][0]["icon"]
    result = [weather_id, weather_main, temper, icon]

    return result
