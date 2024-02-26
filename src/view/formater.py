import config
from datetime import datetime
from . import palette
from . import asciiart
from rich.console import Console


console = Console()


def select_asciiart_and_color(weather_id: int) -> tuple:
    weather_type_id, weather_state_id = divmod(weather_id, 100)
    time = datetime.now()

    if weather_id == 800:
        if (
            time.replace(hour=config.SUNRISE_TIME, minute=0)
            < time
            < time.replace(hour=config.SUNSET_TIME, minute=0)
        ):
            return asciiart.clear_sunny, palette.YELLOW
        else:
            return asciiart.clear_night, palette.PURPLE

    match weather_type_id:
        case 2:
            return asciiart.thunderstorm, palette.RED
        case 3:
            return asciiart.drizzle, palette.LIGHT_BLUE
        case 5:
            return asciiart.rain, palette.BLUE
        case 6:
            return asciiart.snow, palette.WHITE
        case 7:
            return asciiart.fog, palette.DARK_GRAY
        case 8:
            return (
                (asciiart.partial_clouds, palette.LIGHT_GRAY)
                if weather_state_id < 3
                else (asciiart.clouds, palette.GRAY)
            )
    return asciiart.everything_else, palette.LIGHT_GRAY


def format_weather(weather: dict) -> tuple:
    asciiart, color = select_asciiart_and_color(weather["weather_id"])

    column_inf1 = (
        f"[bold]{datetime.today().strftime('%H:%M %p')}[/bold]\n"
        f"температура: [bold]{weather['temp']}°C[/bold] \n"
        f"влажность: [bold]{weather['humidity']}%"
    )
    column_inf2 = (
        f"[bold]{weather['weather_description'].capitalize()} [/bold]\n"
        f"ощущается как: {weather['feels_like']}°C\n"
        f"[i]источник: OpenWeather[/]"
    )
    column_inf1 = f"[{color}]{column_inf1}[/]"
    column_inf2 = f"[{color}]{column_inf2}[/]"
    asciiart = f"[{color}]{asciiart}[/]"
    return asciiart, column_inf1, column_inf2
