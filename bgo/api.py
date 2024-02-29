from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, NamedTuple, TypeAlias

from requests import exceptions, get
from rich import print
from rich.prompt import Prompt

from bgo import config, console


Celsius: TypeAlias = float


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class WeatherType(Enum):
    CLEAR = "Clear"
    CLOUDS = "Clouds"
    DRIZZLE = "Drizzle"
    RAIN = "Rain"
    SNOW = "Snow"
    FOG = "Fog"
    THUNDERSTORM = "Thunderstorm"


@dataclass(slots=True)
class Weather:
    temp: Celsius
    feels_like: Celsius
    humidity: float
    description: WeatherType
    date: datetime | None
    weather_id: int
    location: str


def error_loginig(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
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
def get_coordinates() -> Coordinates:
    with console.status("Получаем координаты...", spinner="aesthetic"):
        response = get("http://ipinfo.io/json", timeout=10).json()
    return Coordinates(
        latitude=response["loc"].split(",")[0], longitude=response["loc"].split(",")[1]
    )


@error_loginig
def get_weather_now(coordinates: Coordinates) -> dict:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = coordinates
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/weather", params, timeout=10
        ).json()
    return response


@error_loginig
def get_weather_forecast(coordinates: Coordinates) -> list[Weather]:
    params = config.BASIC_REQUEST_PARAMS.copy()
    params["lat"], params["lon"] = coordinates
    with console.status("Ждём ответ от OpenWeather...", spinner="aesthetic"):
        response = get(
            "https://api.openweathermap.org/data/2.5/forecast", params, timeout=10
        ).json()
    return response


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


def parse_api_response_now(response: dict) -> Weather:
    return Weather(
        temp=response["main"]["temp"],
        feels_like=response["main"]["feels_like"],
        humidity=response["main"]["humidity"],
        weather_id=response["weather"][0]["id"],
        description=_parse_weather_type(str(response["weather"][0]["id"])),
        location=response["name"],
        date=datetime.now(),
    )


def _parse_weather_type(weather_id: str):
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS,
    }
    try:
        return weather_types[weather_id]
    except (KeyError, IndexError):
        return weather_types[weather_id[:2]]

