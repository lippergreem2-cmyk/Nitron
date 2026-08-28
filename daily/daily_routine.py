# ~/Nitron/daily/daily_routine.py

import datetime
import os

from daily.bible_verses import verse_of_the_day

try:
    from daily.prayers import lord_prayer
except:
    lord_prayer = None

try:
    from daily.quotes import quote_of_the_day
except:
    quote_of_the_day = None

try:
    from speech import speak
except:
    def speak(text):
        print(text)


def japanese_greeting():
    hour = datetime.datetime.now().hour

    if hour < 12:
        return "Ohayou gozaimasu. Good morning."
    elif hour < 18:
        return "Konnichiwa. Good day."
    else:
        return "Konbanwa. Good evening."


def run_daily_routine():

    speak("Good day Boss.")

    # Japanese greeting
    speak(japanese_greeting())

    # Bible verse
    try:
        verse = verse_of_the_day()
        speak("Today's Bible verse.")
        speak(verse)
    except Exception as e:
        speak("Bible verse unavailable.")

    # Lord's Prayer
    if lord_prayer:
        speak("Let us pray.")
        speak(lord_prayer())

    # Quote
    if quote_of_the_day:
        speak("Quote of the day.")
        speak(quote_of_the_day())

    speak("Daily devotion complete. Have a blessed day.")

    # shutdown Nitron after finishing
    return True


if __name__ == "__main__":
    run_daily_routine()
