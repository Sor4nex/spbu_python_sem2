import argparse
from typing import Optional

import pandas as pd
import requests
import seaborn as sns
from lazyparser import *

ERROR_CITY_NOT_FOUND = "ERROR: city {} not found"


@dataclass
class Temperature(metaclass=MetaDataclass):
    temp: float
    feels_like: float


@dataclass
class WeatherDescription(metaclass=MetaDataclass):
    id: int
    main: str
    description: str


@dataclass
class Weather(metaclass=MetaDataclass):
    main: Temperature
    weather: WeatherDescription
    dt: str


def get_response_json(link: str) -> Optional[dict]:
    response = requests.get(link)
    json_response_dict = response.json()
    return json_response_dict if json_response_dict.get("cod", None) != "404" else None


def get_current_weather(api_key: str, city: str, *, command: str = "weather") -> None:
    json_dict = get_response_json(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    )
    if json_dict is None:
        print(ERROR_CITY_NOT_FOUND.format(city))
        return
    json_dict["weather"] = json_dict["weather"][0]
    json_dataclass = parse_class_from_dict(Weather, json_dict)
    if command == "weather":
        print(
            f"City: {city}\nCurrent weather: {json_dataclass.weather.main}\nDescription: {json_dataclass.weather.description}"
        )
    elif command == "temperature":
        print(
            f"City: {city}\nCurrent temperature: {json_dataclass.main.temp}°C\nfeels like: {json_dataclass.main.feels_like}°C"
        )


def draw_temperature_chart(dataframe: pd.DataFrame, city: str) -> None:
    plot = sns.lineplot(dataframe)
    plot.set(xlabel="time", ylabel="temperature °C", title=f"temperature in {city}")
    plot.figure.savefig("temperature_historical.png")
    print("Chart saved with name: temperature_historical.png")


def get_historical_temperature(api_key: str, city: str) -> None:
    json_dict = get_response_json(
        f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    )
    if json_dict is None:
        print(ERROR_CITY_NOT_FOUND.format(city))
        return
    temp_measures = []
    timings = []
    for new_data in json_dict["list"][:10]:
        json_dataclass = parse_class_from_dict(Weather, new_data)
        temp_measures.append(json_dataclass.main.temp)
        timings.append(json_dataclass.dt)
    dataframe = pd.DataFrame(data={"temperature": temp_measures}, index=timings)
    draw_temperature_chart(dataframe, city)


def set_up_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-comm", "--command", type=str, choices=["weather", "temperature", "temperature_plot"])
    parser.add_argument("-c", "--city", type=str)
    parser.add_argument("--api_key", type=str)
    return parser


def main(api_key: str, command: str, city: str) -> None:
    if command == "weather":
        get_current_weather(api_key, city, command=command)
    elif command == "temperature":
        get_current_weather(api_key, city, command=command)
    elif command == "temperature_plot":
        get_historical_temperature(api_key, city)


if __name__ == "__main__":
    parser = set_up_arg_parser()
    args = parser.parse_args()
    main(args.api_key, args.command, args.city)
