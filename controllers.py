import argparse
from re import fullmatch
from api import get_weather_next_week, get_weather_now
from utils import round_json
from view import print_weather_now, print_weather_on_week


parser = argparse.ArgumentParser()


def init_interface():
    parser.add_argument("command",
                        default="now",
                        help="a command showing the forecast for different time periods",
                        type=str, 
                        nargs="?")

    parser.add_argument('-d', "--days",
                        required=False,
                        nargs=1, 
                        type=int,
                        default=5,
                        help='set how long the forecast you want to see (from 1 to 5 days)')

    parser.add_argument("--high-precision",
                        required=False,
                        action="store_true",
                        help='use this field for show value wit max precision')

    parser.add_argument("--full-info",
                        required=False,
                        action="store_true",
                        help='use this field for show all information')


def processing_args(args: argparse.Namespace):
    if args.command == "now":
        weather_data = get_weather_now()
        if args.high_precision:
            weather_data = round_json(weather_data)
        print_weather_now(weather_data, full_info=args.full_info)
    elif args.command == "week":
        weather_data = get_weather_next_week()
        if args.high_precision:
            weather_data = round_json(weather_data)
        print_weather_on_week(weather_data, args.days)
    else:
        print("Ой, не знаю что делать! Используйте -h, чтобы изучить правила испольования.")

