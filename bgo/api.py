from typing import Any, Callable

import config
from requests import exceptions, get
from rich import print
from rich.prompt import Prompt

from bgo import console


def error_loginig(func: Callable[[], Any]) -> Callable[[], Any]:
    def wrapper() -> Callable[[], Any]:
        try:
            return func()
        except exceptions.ConnectionError:
            print("[b red]Упс! Проверьте ваше интернет соединение[/]")
            answer = Prompt.ask(
                "Хотите посмотреть всю ошибку?",
                choices=["y", "n"],
                default="n",
            )
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()
        except Exception:
            print("[b red]Упс! Что-то сломалось, не смог получить координаты[/]")
            answer = Prompt.ask(
                "Хотите посмотреть всю ошибку?",
                choices=["y", "n"],
                default="n",
            )
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()

    return wrapper


@error_loginig
def get_coordinates() -> tuple:
    with console.status("Получаем координаты...", spinner="aesthetic"):
        response = get("http://ipinfo.io/json", timeout=10).json()
    lat = response["loc"].split(",")[0]
    lon = response["loc"].split(",")[1]
    return lat, lon


@error_loginig
def get_weather_now() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/weather", params, timeout=10
        ).json()
    return response


@error_loginig
def get_weather_forecast() -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = get_coordinates()
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/forecast", params, timeout=10
        ).json()
    return response
