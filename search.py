# ~/Nitron/search.py

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



def web_search(query):

    query = str(query).strip()

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    open_url(url)

    return f"Searching Google for {query}."



def wikipedia_search(query):

    query = str(query).strip()

    url = (
        "https://en.wikipedia.org/wiki/"
        + urllib.parse.quote(query.replace(" ", "_"))
    )

    open_url(url)

    return f"Opening Wikipedia for {query}."



def search(command):

    command = command.lower().strip()


    if command.startswith("search "):

        query = command.replace(
            "search ",
            "",
            1
        )

        return web_search(query)



    if command.startswith("wikipedia "):

        query = command.replace(
            "wikipedia ",
            "",
            1
        )

        return wikipedia_search(query)



    if "open google" in command:

        open_url(
            "https://www.google.com"
        )

        return "Opening Google."



    if "open gmail" in command:

        open_url(
            "https://mail.google.com"
        )

        return "Opening Gmail."



    if "open maps" in command:

        open_url(
            "https://maps.google.com"
        )

        return "Opening Google Maps."


