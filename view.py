from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def show_weather_now(data: dict):
    temp = str(round(data["main"]["temp"]))
    feels_like = str(round(data["main"]["feels_like"]))
    humidity = str(round(data["main"]["humidity"]))

    table = Table.grid(padding=1, pad_edge=True)
    table.add_row("Температура:", f"[bold]{temp} °C[/]", )
    table.add_row("Ощущается как:", f"[bold]{feels_like} °C[/]")
    table.add_row("Влажность:", f"[bold]{humidity}%[/]")

    print(
        Panel(
            table,
            title="[bold]Погода сейчас :sun_behind_small_cloud:[/] ", 
            width=40,
            border_style="#48C9B0 bold",
            padding=1,
        ), 
    )

