<p align="center">
    <img src=https://github.com/Alchemmist/weather-demo/blob/main/media/logo.jpg width=500/>
    <br />
    <a href="https://t.me/alchemmist" alt="link to telegram account">
        <img alt="Static Badge" src="https://img.shields.io/badge/my%20Telegram-blue?style=for-the-badge&logo=telegram&logoColor=white&link=https%3A%2F%2Ft.me%2Falchemmist" />
    <a />
    <br />
    <a href="https://python.org" alt="Contributors">
        <img alt="Static Badge" src="https://img.shields.io/badge/python%20%F0%9F%90%8D-3.12-blue?style=for-the-badge&link=https%3A%2F%2Fpython.org" />
    <a />
    <a href="https://github.com/aaronrausch/ascii-weather" alt="Contributors">
        <img alt="Static Badge" src="https://img.shields.io/badge/thanks_for_ascii_art-yellow?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Faaronrausch%2Fascii-weather%2F" />
    <a />
    <br />
    <b>Before going out</b>
    <br />
    <b>a minimalistic utility for viewing the weather directly in the terminal</b>
</p>


# Documentation

[1. Description](#about)

[2. Example](#example)

[3. Usage](#usage)

[4. Installation](#install)

[5. Development](#dev)


<a name="about"/>

# 1. Description

weather-cli is a console utility for viewing the weather at the moment, as well as the forecast for the nearest time. The program has pleasant and user-friendly interaction interfaces. The utility works with two APIs:

- OpenWeather (to get weather data)

 - IpInfo (to identify the location by IP address

 The source code of the program is written in the Python programming language, using the rich library for visual display of data.

<a name="example"/>

# 2. Example


https://github.com/Alchemmist/bgo/assets/104511335/f77ff42c-4bf1-4704-bded-3d1078b3bd57


<a name="usage" />

 # 3. Usage
 
The utility has two main commands:
 ```shell
python weather.py now
python weather.py forecast
```

`now` - shows the current weather in the following format:
```
╭─────────────────────── Москва 🌤  ────────────────────────╮
│                                                           │
│  ( )()_  05:18 AM         Пасмурно                        │
│ (      ) температура: 0°C ощущается как: -5°C             │
│  (  )()  влажность: 91%   источник: OpenWeather           │
│                                                           │
╰───────────────────────────────────────────────────────────╯
```

`forecast` - shows the weather forecast in the form of a table. It is possible to specify the number of forecast days (from 1 to 5):
```
python weather.py forecast -d 3
```
You can also view a more detailed forecast by setting the `--with-time` flag:
```
python weather.py forecast -d 2 --with-time
```

In addition, the following flags can be passed for both commands (now and forecast):

- `--high-precision` flag that allows you to see the most accurate values of all parameters, without rounding
- `--fullinfo` flag deprives you of a convenient and visual display, but it shows absolutely all the weather information received from the API

You can review the current usage documentation at any time using the command:
```shell
python src/weather --help
```
This command will show you such (or almost such) a list with all possible parameters:
```
usage: weather [-h] [-d {1,2,3,4,5}] [--high-precision] [--full-info] [--with-time] [command]

positional arguments:
  command               a command showing the forecast for different time periods

options:
  -h, --help            show this help message and exit
  -d {1,2,3,4,5}, --days {1,2,3,4,5}
                        set how long the forecast you want to see (from 1 to 5 days)
  --high-precision      use this field for show value wit max precision
  --full-info           use this field for show all information
  --with-time           use this field for show forecast with time
```

<a name="install" />

# 4. Installation
If you have python and pip package manager installed, then just run the command:
```shell
pip install bgo
bgo
```
Done!

<a name="dev" />

# 5. Development
To run the project locally, run the following commands:
```shell
git clone git@github.com:Alchemmist/bgo.git
cd bgo
poetry install
poetry run python bgo -h
```

If no errors have occurred, then you have successfully launched the project in the local environment. Add functionality, fix bugs and send pull requests
