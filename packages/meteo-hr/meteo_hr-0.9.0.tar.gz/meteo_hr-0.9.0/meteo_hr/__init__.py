import re
import requests

from bs4 import BeautifulSoup
from collections import OrderedDict
from decimal import Decimal


def batch(lst, n):
    for i in range(len(lst) // n):
        yield list(lst[i * n + k] for k in range(n))


def fetch(place):
    response = requests.get("https://meteo.hr/prognoze.php", params={
        "Code": place,
        "id": "prognoza",
        "section": "prognoze_model",
        "param": "3d",
    })
    response.raise_for_status()
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one(".table-weather-7day")

    matches = re.findall(r"\[new Date\(\d+,\d+,\d+,\d+\),-?\d+,([0-9.]+)\]", html)
    percipitations = [Decimal(m) for m in matches]

    if not table:
        raise ValueError("Cannot find table")

    rows = table.select("tr")

    times = rows[0].select("th")[1:]
    times = [t.text for t in times]
    weather_rows = rows[1:-1]

    for r1, r2, r3 in batch(weather_rows, 3):
        day, _, date = r1.find("th").contents
        values = parse_day(r1, r2, r3)
        zipped = [(time, forecast) for time, forecast in zip(times, values) if forecast]
        for _, forecast in zipped:
            forecast["percipitation"] = percipitations.pop(0)
        yield day, date, OrderedDict(zipped)


def parse_day(r1, r2, r3):
    for (weather, wetaher_title), temperature, (wind, wind_title) in zip(
        icons_and_titles(r1),
        temperatures(r2),
        icons_and_titles(r3),
    ):
        yield {
            "weather": weather,
            "weather_title": wetaher_title,
            "temperature": temperature,
            "wind": wind,
            "wind_title": wind_title,
        } if weather else None


def icons_and_titles(row):
    for cell in row.select("td"):
        span = cell.find("span")
        if span:
            img = span.find("img")
            title = span.attrs["title"]
            icon = img.attrs["src"].split("/")[-1].replace(".svg", "")
            yield icon, title
        else:
            yield None, None


def temperatures(row):
    for cell in row.select("td"):
        text = cell.text.replace(" °C", "")
        yield int(text) if text else None


def bold(string):
    return f"\033[1m{string}\033[0m"


def gray(string):
    return f"\033[90m{string}\033[0m"


def red(string):
    return f"\033[31m{string}\033[0m"


def yellow(string):
    return f"\033[33m{string}\033[0m"


def blue(string):
    return f"\033[34m{string}\033[0m"


WINDS = {
    "C0": gray("-"),
    "N1": gray("↓"),
    "S1": gray("↑"),
    "E1": gray("←"),
    "W1": gray("→"),
    "NE1": gray("↙"),
    "NW1": gray("↘"),
    "SE1": gray("↖"),
    "SW1": gray("↗"),
    "N2": yellow("↓"),
    "S2": yellow("↑"),
    "E2": yellow("←"),
    "W2": yellow("→"),
    "NE2": yellow("↙"),
    "NW2": yellow("↘"),
    "SE2": yellow("↖"),
    "SW2": yellow("↗"),
    "N3": red("↓"),
    "S3": red("↑"),
    "E3": red("←"),
    "W3": red("→"),
    "NE3": red("↙"),
    "NW3": red("↘"),
    "SE3": red("↖"),
    "SW3": red("↗"),
}


def print_weater_icons():
    print("black sun with rays", "\N{black sun with rays}", "\N{black sun with rays}\uFE0F")
    print("cloud with lightning", "\N{cloud with lightning}", "\N{cloud with lightning}\uFE0F")
    print("cloud with rain", "\N{cloud with rain}", "\N{cloud with rain}\uFE0F")
    print("cloud with snow", "\N{cloud with snow}", "\N{cloud with snow}\uFE0F")
    print("cloud", "\N{cloud}", "\N{cloud}\uFE0F")
    print("fog", "\N{fog}", "\N{fog}\uFE0F")
    print("sun behind cloud", "\N{sun behind cloud}", "\N{sun behind cloud}\uFE0F")
    print("sun with face", "\N{sun with face}", "\N{sun with face}\uFE0F")
    print("thunder cloud and rain", "\N{thunder cloud and rain}", "\N{thunder cloud and rain}\uFE0F")
    print("white sun behind cloud with rain", "\N{white sun behind cloud with rain}", "\N{white sun behind cloud with rain}\uFE0F")
    print("white sun behind cloud", "\N{white sun behind cloud}", "\N{white sun behind cloud}\uFE0F")
    print("white sun with small cloud", "\N{white sun with small cloud}", "\N{white sun with small cloud}\uFE0F")
    print("wind blowing face", "\N{wind blowing face}", "\N{wind blowing face}\uFE0F")


WEATHER_ICONS = {
    "magla, nebo vedro": "\N{fog}\uFE0F",
    "malo oblačno, danju sunčano": "\N{white sun with small cloud}\uFE0F",
    "oblačno i maglovito": "\N{cloud}\uFE0F",
    "oblačno": "\N{cloud}\uFE0F",
    "pretežno oblačno": "\N{cloud}\uFE0F",
    "oblačno uz malu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "promjenljivo oblačno uz malu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "promjenljivo oblačno uz uz malu količinu snijega": "\N{cloud with snow}\uFE0F",
    "umjereno oblačno": "\N{sun behind cloud}\uFE0F",
    "vedro, danju sunčano": "\N{black sun with rays}\uFE0F",
    "magla, malo do umjereno oblačno": "\N{fog}\N{fog}"
}


def dump(data):
    for day, date, times in data:
        print()
        print(bold(f"{day}, {date}"))
        for time, forecast in times.items():
            if forecast:
                weather_icon = WEATHER_ICONS.get(forecast['weather_title'])
                weather_icon = f"{weather_icon}" if weather_icon else "??"

                wind_icon = WINDS.get(forecast['wind'], "?")
                temperature = f"{forecast['temperature']:>3}°C"
                if forecast['temperature'] >= 30:
                    temperature = red(temperature)
                if forecast['temperature'] <= 0:
                    temperature = blue(temperature)

                percipitation = f"{forecast['percipitation']:>4}mm"
                if forecast['percipitation'] < 1:
                    percipitation = gray(percipitation)
                if forecast['percipitation'] > 5:
                    percipitation = yellow(percipitation)
                if forecast['percipitation'] > 10:
                    percipitation = red(percipitation)

                print(" ".join([
                    f"  {time:>5}  {temperature}  {percipitation}  {wind_icon}  {weather_icon}",
                    f"{forecast['weather_title']},",
                    f"vjetar {forecast['wind_title']}"
                ]))


def run(name, slug):
    data = list(parse(fetch(slug)))
    print(f"Prognoza za {name}")
    dump(data)
