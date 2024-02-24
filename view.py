from datetime import datetime
import palette
import asciiart
from rich import print, box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def select_asciiart_and_color(weather_id: int) -> tuple:
    weather_type_id, weather_state_id = divmod(weather_id, 100)
    time = datetime.now()

    if weather_id == 800:
        return (
            (asciiart.clear_sunny, palette.YELLOW)
            if time.replace(hour=6, minute=0) < time < time.replace(hour=19, minute=0)
            else (asciiart.clear_night, palette.DARK_BLUE)
        )

    match weather_type_id:
        case 2:
            return asciiart.thunderstorm, palette.PURPLE
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


def print_weather_now(data: dict):
    weather_id = data["weather"][0]["id"]
    location = data["name"]

    ascii_art, column_inf1, column_inf2 = format_weather(data)

    table = Table.grid(padding=1, pad_edge=True)
    table.add_row(ascii_art, column_inf1, column_inf2)

    print(
        Panel(
            table,
            title=f"[bold]{location} :sun_behind_small_cloud:[/] ",
            style=f"{select_asciiart_and_color(weather_id)[1]}",
            width=55,
            padding=0,
        ),
    )


def print_weather_forecast_with_time(data: dict, days: int = 5):
    table = Table(
        # show_edge=False,
        show_header=True, # expand=False,
        # row_styles=["none", "dim"],
        # box=box.SIMPLE,
    )
    table.add_column("[green]Дата[/]", style="green")
    table.add_column("[#9ACD32]Время[/]", style="#9ACD32")
    table.add_column("[blue]Температура[/]", style="blue", justify="right")
    table.add_column(
        "[cyan]Ощущается как[/]",
        style="cyan",
        justify="right",
    )
    table.add_column(
        "[yellow]Влажность[/]",
        style="yellow",
        justify="right",
    )

    last_date = ""
    count = 0
    for i in range(len(data["list"])):
        if count == days + 1:
            break
        date, time = data["list"][i]["dt_txt"].split()
        time = time[:-3]
        temp = str(data["list"][i]["main"]["temp"]) + " °C"
        feels_like = str(data["list"][i]["main"]["feels_like"]) + " °C"
        humidity = str(data["list"][i]["main"]["humidity"]) + "%"

        if date == last_date:
            date = ""
        else:
            count += 1
            last_date = date

        if count != days + 1:
            table.add_row(
                date,
                time,
                temp,
                feels_like,
                humidity,
            )

    print(table)


def print_weather_forecast(data: dict, days: int = 5, high_precision: bool = False):
    table = Table(
        show_header=True,
        box=box.SIMPLE,
    )

    table.add_column("[green]Дата[/]", style="green")
    table.add_column("[blue]Температура[/]", style="blue", justify="right")
    table.add_column(
        "[cyan]Ощущается как[/]",
        style="cyan",
        justify="right",
    )
    table.add_column(
        "[yellow]Влажность[/]",
        style="yellow",
        justify="right",
    )

    last_date = data["list"][0]["dt_txt"].split()[0]
    j = 0
    for _ in range(days):
        parameters = {"temp": 0, "feels_like": 0, "humidity": 0}
        count = 0
        while last_date == data["list"][j]["dt_txt"].split()[0]:
            if j >= len(data["list"]) - 1: 
                break
            parameters["temp"] += data["list"][j]["main"]["temp"]
            parameters["feels_like"] += data["list"][j]["main"]["feels_like"]
            parameters["humidity"] += data["list"][j]["main"]["humidity"]
            count += 1
            j += 1
        last_date = data["list"][j]["dt_txt"].split()[0]

        if high_precision:
            parameters = {k: f"{(v / count):.2f}" for k, v in parameters.items()}
        else:
            parameters = {k: f"{round(v / count)}" for k, v in parameters.items()}

        parameters["temp"] += " °C"
        parameters["feels_like"] += " °C"
        parameters["humidity"] += "%"

        table.add_row(
            data["list"][j - 1]["dt_txt"].split()[0],
            parameters["temp"],
            parameters["feels_like"],
            parameters["humidity"],
        )

    print(table)
