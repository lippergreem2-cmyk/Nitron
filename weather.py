# ~/Nitron/weather.py

import subprocess
import urllib.parse


def open_url(url):

    subprocess.run([
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        url
    ])



def get_weather(city="your location"):

    query = urllib.parse.quote(
        f"weather {city}"
    )

    url = f"https://www.google.com/search?q={query}"

    open_url(url)

    return f"Opening weather information for {city}"



def weather(command):

    command = command.lower()


    if "weather" in command:

        city = "your location"


        if " in " in command:

            city = command.split(" in ",1)[1]


        return get_weather(city)


    return "No weather command found."
