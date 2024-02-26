import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

LANGUAGE = "ru"

BASIC_REQUEST_PARAMS = {
    "units": "metric",
    "appid": OPEN_WEATHER_API_KEY,
    "lang": LANGUAGE,
}

SUNRISE_TIME = 5
SUNSET_TIME = 20
