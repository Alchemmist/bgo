from . import palette
from .formater import format_weather, select_asciiart_and_color
from rich import print, box
from rich.table import Table
from rich.panel import Panel


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
            width=60,
            padding=0,
        ),
    )


def print_weather_forecast_with_time(data: dict, days: int = 5):
    table = Table(
        show_header=True, # expand=False,
    )
    table.add_column(f"[{palette.GREEN}]Дата[/]", style=palette.GREEN)
    table.add_column(f"[{palette.LIGHT_GREEN}]Время[/]", style=palette.LIGHT_GREEN)
    table.add_column(f"[{palette.BLUE}]Температура[/]", style=palette.BLUE, justify="right")
    table.add_column(
        f"[{palette.WHITE}]Ощущается как[/]",
        style=palette.WHITE,
        justify="right",
    )
    table.add_column(
        f"[{palette.YELLOW}]Влажность[/]",
        style=palette.YELLOW,
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

    table.add_column(f"[{palette.GREEN}]Дата[/]", style=palette.GREEN)
    table.add_column(f"[{palette.BLUE}]Температура[/]", style=palette.BLUE, justify="right")
    table.add_column(
        f"[{palette.WHITE}]Ощущается как[/]",
        style=palette.WHITE,
        justify="right",
    )
    table.add_column(
        f"[{palette.YELLOW}]Влажность[/]",
        style=palette.YELLOW,
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


