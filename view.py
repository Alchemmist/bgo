from rich import print, box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def print_weather_now(data: dict):
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"] 
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


def print_weather_forecast_with_time(data: dict, days: int = 5):
    table = Table(
        # show_edge=False,
        show_header=True,
        # expand=False,
        # row_styles=["none", "dim"],
        # box=box.SIMPLE,
    )
    table.add_column("[green]Дата[/]", style="green")
    table.add_column("[#9ACD32]Время[/]", style="#9ACD32")
    table.add_column("[blue]Температура[/]", style="blue", justify="right")
    table.add_column("[cyan]Ощущается как[/]",style="cyan",justify="right",)
    table.add_column("[yellow]Влажность[/]", style="yellow", justify="right",)

    last_date = ""
    for i in range(len(data["list"])):
        date, time = data["list"][i]["dt_txt"].split()
        time = time[:-3]
        temp = str(data["list"][i]["main"]["temp"]) + " °C"
        feels_like = str(data["list"][i]["main"]["feels_like"]) + " °C"
        humidity = str(data["list"][i]["main"]["humidity"]) + "%"
        
        if date == last_date:
            date = ""
        else:
            last_date = date

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
    table.add_column("[cyan]Ощущается как[/]",style="cyan",justify="right",)
    table.add_column("[yellow]Влажность[/]", style="yellow", justify="right",)

    # print(data)
    last_date = data["list"][0]["dt_txt"].split()[0]
    j = 0
    for _ in range(days):
        parameters = {
            "temp": 0,
            "feels_like": 0,
            "humidity": 0
        }
        count = 0
        while last_date == data["list"][j]["dt_txt"].split()[0]:
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
