from . import palette
from .formater import format_weather, select_asciiart_and_color
from rich import print, box
from rich.table import Table
from rich.panel import Panel


def print_weather_now(weather: dict):
    weather_id = weather["weather_id"]
    location = weather["location"]

    ascii_art, column_inf1, column_inf2 = format_weather(weather)

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


def print_weather_forecast(tabel_rows: list, with_time: bool):
    table = Table(
        show_header=True,  # expand=False,
    )
    table.add_column(f"[{palette.GREEN}]Дата[/]", style=palette.GREEN)
    if with_time:
        table.add_column(f"[{palette.LIGHT_GREEN}]Время[/]", style=palette.LIGHT_GREEN)
    table.add_column(
        f"[{palette.BLUE}]Температура[/]", style=palette.BLUE, justify="right"
    )
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


    for weather in tabel_rows:
        if with_time:
            table.add_row(
                weather["date"],
                weather["time"],
                weather["temp"],
                weather["feels_like"],
                weather["humidity"],
            )
        else:
            table.add_row(
                weather["date"],
                weather["temp"],
                weather["feels_like"],
                weather["humidity"],
            )


    print(table)


