from api import get_weather_now
from rich import print
from view import show_weather_now



def main():
    show_weather_now(get_weather_now())



if __name__ == "__main__":
    main()

