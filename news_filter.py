# news_filter.py

from datetime import datetime

HIGH_IMPACT_EVENTS = [

    "Non-Farm Payrolls",

    "CPI",

    "PPI",

    "FOMC",

    "Interest Rate Decision",

    "GDP",

    "Retail Sales",

    "PMI",

    "Employment Change",

    "Central Bank Speech"

]


def load_news():

    news = [

        {
            "time": "13:30",
            "currency": "USD",
            "impact": "High",
            "event": "Non-Farm Payrolls"
        },

        {
            "time": "15:00",
            "currency": "USD",
            "impact": "Medium",
            "event": "ISM Manufacturing PMI"
        }

    ]

    return news


def current_time():

    return datetime.now().strftime("%H:%M")


def high_impact_now():

    news = load_news()

    now = current_time()

    for event in news:

        if event["impact"] == "High":

            if event["time"] == now:

                return True, event

    return False, None


def can_trade():

    status, event = high_impact_now()

    if status:

        return {

            "allowed": False,

            "reason": f"High Impact News: {event['event']}"

        }

    return {

        "allowed": True,

        "reason": "No High Impact News"

    }


if __name__ == "__main__":

    result = can_trade()

    print("=" * 40)

    print("NITRON NEWS FILTER")

    print("=" * 40)

    print(result)

    print("=" * 40)
