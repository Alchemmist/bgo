import config
from typing import Callable
from rich.prompt import Prompt
from rich import print
from requests import get, exceptions
from view import console


def error_loginig(func: Callable) -> Callable:
    def wrapper():
        try:
            return func()
        except exceptions.ConnectionError:
            print("[b red]Упс! Проверьте ваше интернет соединение[/]")
            answer = Prompt.ask("Хотите посмотреть всю ошибку?", choices=["y", "n"], default="n")
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()
        except Exception:
            print("[b red]Упс! Что-то сломалось, не смог получить координаты[/]")
            answer = Prompt.ask("Хотите посмотреть всю ошибку?", choices=["y", "n"], default="n")
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()
    return wrapper


@error_loginig
def get_coordinates() -> tuple:
    with console.status("Получаем координаты...", spinner="aesthetic"):
        response = get("http://ipinfo.io/json").json()
    lat = response["loc"].split(",")[0]
    lon = response["loc"].split(",")[1]    
    return lat, lon


@error_loginig
def get_weather_now() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/weather",
            params,
        ).json()
    return response


@error_loginig
def get_weather_forecast() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params,
        ).json()
    return response

