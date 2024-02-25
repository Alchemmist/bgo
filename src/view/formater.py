from datetime import datetime
from . import palette
from . import asciiart
from rich.console import Console


console = Console()


def select_asciiart_and_color(weather_id: int) -> tuple:
    weather_type_id, weather_state_id = divmod(weather_id, 100)
    time = datetime.now()

    if weather_id == 800:
        return (
            (asciiart.clear_sunny, palette.YELLOW)
            if time.replace(hour=6, minute=0) < time < time.replace(hour=19, minute=0)
            else (asciiart.clear_night, palette.PURPLE)
        )

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


def format_weather(data: dict) -> tuple:
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
        f"температура: [bold]{temp}°C[/bold]\n" 
        f"влажность: [bold]{humidity}%"
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


