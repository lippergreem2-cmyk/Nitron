import random
from datetime import datetime

from daily.bible_verses import VERSES
from daily.quotes import QUOTES
from daily.prayers import PRAYER


REFLECTIONS = [

"Today is a new gift from God. Walk in faith and trust Him in every decision.",

"God is preparing you for greater things through today's experiences.",

"Success begins with faith, discipline, and consistent effort.",

"Never stop learning because wisdom is one of God's greatest gifts.",

"Every challenge is an opportunity for God to strengthen your character.",

"Stay humble, work hard, and trust God's timing.",

"Kindness, honesty, and discipline create a meaningful life.",

"Remember that every small step brings you closer to your purpose.",

"God's plans are always greater than our own.",

"Walk with confidence because God walks with you."

]


def get_devotion():

    day = datetime.now().toordinal()

    verse = VERSES[day % len(VERSES)]

    quote = QUOTES[day % len(QUOTES)]

    reflection = REFLECTIONS[day % len(REFLECTIONS)]

    return f"""
══════════════════════════════

GOOD MORNING BOSS NIMROD

📖 Bible Verse

{verse[0]}

{verse[1]}

🙏 Prayer

{PRAYER}

💬 Reflection

{reflection}

🌟 Quote of the Day

{quote}

🎯 Daily Mission

• Learn something new.
• Pray before making major decisions.
• Help at least one person.
• Stay disciplined.
• Build your future one step at a time.

💡 Nitron Reminder

Boss Nimrod,

Stay faithful.
Stay disciplined.
Keep learning.
Keep building.

Your goal is to build something that positively impacts millions of people. Every honest day of work moves you closer to that vision.

May God bless your day.

══════════════════════════════
"""
