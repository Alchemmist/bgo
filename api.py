import config
from requests import get
from view import console


def get_coordinates() -> tuple:
    with console.status("Получаем координаты...", spinner="aesthetic"):
        response = get("http://ipinfo.io/json").json()
    lat = response["loc"].split(",")[0]
    lon = response["loc"].split(",")[1]
    return lat, lon


def get_weather_now() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/weather",
            params,
        ).json()
    return response


def get_weather_next_week() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params,
        ).json()
    return response

