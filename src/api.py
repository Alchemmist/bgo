import config
from typing import Callable
from rich.prompt import Prompt
from rich import print
from requests import get, exceptions
from view.formater import console


def error_loginig(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ConnectionError:
            print("[b red]Упс! Проверьте ваше интернет соединение[/]")
            answer = Prompt.ask(
                "Хотите посмотреть всю ошибку?", choices=["y", "n"], default="n"
            )
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()
        except Exception:
            print("[b red]Упс! Что-то сломалось, не смог получить координаты[/]")
            answer = Prompt.ask(
                "Хотите посмотреть всю ошибку?", choices=["y", "n"], default="n"
            )
            if answer == "y":
                console.print_exception(max_frames=1)
            exit()

    return wrapper


@error_loginig
def get_coordinates() -> tuple[float, float]:
    with console.status("Получаем координаты...", spinner="aesthetic"):
        response = get("http://ipinfo.io/json").json()
    lat = response["loc"].split(",")[0]
    lon = response["loc"].split(",")[1]
    return lat, lon


@error_loginig
def get_weather_now(coordinates: tuple) -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = coordinates
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/weather",
            params,
        ).json()
    return response


@error_loginig
def get_weather_forecast(coordinates: tuple) -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = coordinates
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params,
        ).json()
    return response


def parse_api_response_now(response: dict) -> dict:
    return {
        "temp": response["main"]["temp"],
        "feels_like": response["main"]["feels_like"],
        "humidity": response["main"]["humidity"],
        "weather_id": response["weather"][0]["id"],
        "weather_description": response["weather"][0]["description"],
        "location": response["name"],
    }


"""
[
    {
        "2023.02.12": [
            {
                <weather>
            }, 
            {
                <weather>
            }, 
            {
                <weather>
            }, 
        ]
    },
    {
        "2023.02.13": [
            {
                <weather>
            },
            {
                <weather>
            }
        ]
    },
]
"""
def parse_api_response_forecast(response: dict, days: int, with_time: bool, high_precision: bool) -> list[dict]:
    if with_time: 
        return _parse_forecast_data_with_time(response, days)
    else:
        return _parse_forecast_data(response, days, high_precision)
    
    
def _parse_forecast_data(response: dict, days: int, high_precision: bool) -> list[dict]:
    table_rows = []
    last_date = response["list"][0]["dt_txt"].split()[0]
    j = 0
    for _ in range(days):
        parameters = {"temp": 0, "feels_like": 0, "humidity": 0}
        count = 0
        while last_date == response["list"][j]["dt_txt"].split()[0]:
            if j >= len(response["list"]) - 1:
                break
            parameters["temp"] += response["list"][j]["main"]["temp"]
            parameters["feels_like"] += response["list"][j]["main"]["feels_like"]
            parameters["humidity"] += response["list"][j]["main"]["humidity"]
            count += 1
            j += 1
        last_date = response["list"][j]["dt_txt"].split()[0]

        if high_precision:
            parameters = {k: f"{(v / count):.2f}" for k, v in parameters.items()}
        else:
            parameters = {k: f"{round(v / count)}" for k, v in parameters.items()}

        parameters["temp"] += " °C"
        parameters["feels_like"] += " °C"
        parameters["humidity"] += "%"

        table_rows.append({
            "date": response["list"][j - 1]["dt_txt"].split()[0],
            "temp": parameters["temp"],
            "feels_like": parameters["feels_like"],
            "humidity": parameters["humidity"],
        })
    return table_rows


def _parse_forecast_data_with_time(response: dict, days: int) -> list[dict]:
    table_rows = []
    last_date = ""
    count = 0
    for i in range(len(response["list"])):
        if count == days + 1:
            break
        date, time = response["list"][i]["dt_txt"].split()
        time = time[:-3]
        temp = str(response["list"][i]["main"]["temp"]) + " °C"
        feels_like = str(response["list"][i]["main"]["feels_like"]) + " °C"
        humidity = str(response["list"][i]["main"]["humidity"]) + "%"

        if date == last_date:
            date = ""
        else:
            count += 1
            last_date = date

        if count != days + 1:
            table_rows.append({
                "date": date,
                "time": time,
                "temp": temp,
                "feels_like": feels_like,
                "humidity": humidity,
            })
    return table_rows

