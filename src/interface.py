import argparse
from typing import Callable
from api import (
    get_weather_now,
    get_coordinates,
    get_weather_forecast,
    parse_api_response_now, 
    parse_api_response_forecast
)
from utils import round_json
from view.printer import (
    print_weather_now,
    print_weather_forecast,
)
from rich import print


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


def processing_args(args: argparse.Namespace) -> None:
    coordinates = get_coordinates()

    if args.command == "now":
        api_response = _command_prepreocessing(
            api_function=lambda: get_weather_now(coordinates),
            high_precision=args.high_precision,
            full_info=args.full_info,
        )
        weather = parse_api_response_now(api_response)
        print_weather_now(weather)
    elif args.command == "forecast":
        api_response = _command_prepreocessing(
            api_function=lambda: get_weather_forecast(coordinates),
            high_precision=args.high_precision,
            full_info=args.full_info,
        )

        table_rows = parse_api_response_forecast(api_response, args.days[0], args.with_time, args.high_precision)
        print_weather_forecast(table_rows, args.with_time)
    else:
        print(
            "Ой, не знаю что делать! Используйте -h, чтобы изучить правила испольования."
        )


def _command_prepreocessing(api_function: Callable, 
                            high_precision: bool, full_info: bool) -> dict:
    response = api_function()
    if not high_precision:
        response = round_json(response)
    if full_info:
        print(response)
        exit(1)
    return response
