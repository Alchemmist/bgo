import argparse

from rich import print

from bgo.api import get_weather_forecast, get_weather_now
from bgo.utils import round_json
from bgo.view.printer import (
    print_weather_forecast,
    print_weather_forecast_with_time,
    print_weather_now,
)

parser = argparse.ArgumentParser()


def init_interface():
    parser.add_argument(
        "command",
        default="now",
        help="a command showing the forecast for different time periods",
        type=str,
        nargs="?",
    )

    parser.add_argument(
        "-d",
        "--days",
        required=False,
        nargs=1,
        type=int,
        default=[5],
        choices=[1, 2, 3, 4, 5],
        help="set how long the forecast you want to see (from 1 to 5 days)",
    )

    parser.add_argument(
        "--high-precision",
        required=False,
        action="store_true",
        help="use this field for show value wit max precision",
    )

    parser.add_argument(
        "--full-info",
        required=False,
        action="store_true",
        help="use this field for show all information",
    )

    parser.add_argument(
        "--with-time",
        required=False,
        action="store_true",
        help="use this field for show forecast with time",
    )


def processing_args(args: argparse.Namespace):
    if args.command == "now":
        weather_data = get_weather_now()
        if not args.high_precision:
            weather_data = round_json(weather_data)

        if args.full_info:
            print(weather_data)
            return

        print_weather_now(weather_data)
    elif args.command == "forecast":
        weather_data = get_weather_forecast()
        if not args.high_precision:
            weather_data = round_json(weather_data)

        if args.full_info:
            print(weather_data)
            return

        if args.with_time:
            print_weather_forecast_with_time(weather_data, args.days[0])
        else:
            print_weather_forecast(weather_data, args.days[0], args.high_precision)
    else:
        print(
            "Ой, не знаю что делать! "
            "Используйте -h, чтобы изучить правила испольования."
        )
