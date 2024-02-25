from datetime import datetime
from enum import Enum
from typing import Any

from bgo.view import asciiart


class Palette(Enum):
    YELLOW = "#FFDB58"
    WHITE = "#A7C7E7"
    LIGHT_BLUE = "#4682B4"
    BLUE = "#1434A4"
    DARK_BLUE = "#4169E1"
    DARK_GRAY = "#6a8767"
    GRAY = "#A9A9A9"
    LIGHT_GRAY = "#AAAEB1"
    PURPLE = "#5D3FD3"


def select_asciiart_and_color(weather_id: int) -> tuple[str, str]:
    weather_type_id, weather_state_id = divmod(weather_id, 100)
    time = datetime.now()

    if weather_id == 800:
        if time.replace(hour=6, minute=0) < time and time < time.replace(
            hour=19, minute=0
        ):
            return (asciiart.clear_sunny, Palette.YELLOW.value)
        else:
            return (asciiart.clear_night, Palette.DARK_BLUE.value)

    match weather_type_id:
        case 2:
            return asciiart.thunderstorm, Palette.PURPLE.value
        case 3:
            return asciiart.drizzle, Palette.LIGHT_BLUE.value
        case 5:
            return asciiart.rain, Palette.BLUE.value
        case 6:
            return asciiart.snow, Palette.WHITE.value
        case 7:
            return asciiart.fog, Palette.DARK_GRAY.value
        case 8:
            return (
                (asciiart.partial_clouds, Palette.LIGHT_GRAY.value)
                if weather_state_id < 3
                else (asciiart.clouds, Palette.GRAY.value)
            )
    return asciiart.everything_else, Palette.LIGHT_GRAY.value


def format_weather(data: dict[str, Any]) -> tuple[str, str, str]:
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    weather_id, weather_description = (
        data["weather"][0]["id"],
        data["weather"][0]["description"],
    )

    asciiart, color = select_asciiart_and_color(weather_id)

    column_inf1 = (
        f"[bold]{datetime.today().strftime('%H:%M %p')}[/bold]\n"
        f"температура: [bold]{temp}°C[/bold] \n"
        f"влажность:  [bold]{humidity}%"
    )
    column_inf2 = (
        f"[bold]{weather_description.capitalize()} [/bold]\n"
        f"ощущается как: {feels_like}°C\n"
        f"[i]источник: OpenWeather[/]"
    )
    column_inf1 = f"[{color}]{column_inf1}[/]"
    column_inf2 = f"[{color}]{column_inf2}[/]"
    asciiart = f"[{color}]{asciiart}[/]"
    return asciiart, column_inf1, column_inf2
