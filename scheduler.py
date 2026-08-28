import time
from datetime import datetime

from speech import speak
from daily.bible_verses import verse_of_the_day
from daily.prayers import lords_prayer
from daily.quotes import quote_of_the_day

last_run = None

while True:
    now = datetime.now()

    if now.hour == 3 and now.minute == 0:
        if last_run != now.date():
            speak("Ohayō gozaimasu. Good morning.")

            speak(verse_of_the_day())
            speak(lords_prayer())
            speak(quote_of_the_day())

            speak("Have a blessed day. Nitron is shutting down.")

            last_run = now.date()
            break

    time.sleep(20)
