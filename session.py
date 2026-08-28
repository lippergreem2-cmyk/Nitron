# session.py

from datetime import datetime


def current_session():

    hour = datetime.utcnow().hour

    if 0 <= hour < 7:
        return "Asian"

    elif 7 <= hour < 12:
        return "London"

    elif 12 <= hour < 17:
        return "New York"

    return "After Hours"


def kill_zone():

    hour = datetime.utcnow().hour

    if 7 <= hour <= 10:
        return "London Kill Zone"

    if 13 <= hour <= 16:
        return "New York Kill Zone"

    return "Inactive"


def session_bias():

    session = current_session()

    if session == "London":
        return "Trend Expansion"

    if session == "New York":
        return "Continuation / Reversal"

    if session == "Asian":
        return "Accumulation"

    return "Low Liquidity"


def analyze_session():

    return {
        "session": current_session(),
        "kill_zone": kill_zone(),
        "bias": session_bias()
    }


if __name__ == "__main__":

    info = analyze_session()

    print("=" * 40)

    print("SESSION ANALYSIS")

    print("=" * 40)

    for k, v in info.items():
        print(f"{k:12}: {v}")

    print("=" * 40)
