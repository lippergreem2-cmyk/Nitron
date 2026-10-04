from datetime import datetime, time
import pytz

ET = pytz.timezone("US/Eastern")

# Major forex trading sessions, in their own local exchange times (roughly).
# Expressed here as ET hour ranges for simplicity (approximate, ignores each
# region's own DST shifts relative to US DST -- good enough for signal timing,
# not for precise session boundaries).
SESSIONS = {
    "sydney":  {"start": 17, "end": 2},   # 5pm-2am ET (wraps midnight)
    "tokyo":   {"start": 19, "end": 4},   # 7pm-4am ET (wraps midnight)
    "london":  {"start": 3,  "end": 12},  # 3am-12pm ET
    "new_york":{"start": 8,  "end": 17},  # 8am-5pm ET
}

# Add real dates each year -- US market holidays that also thin out forex liquidity.
FOREX_HOLIDAYS_ET = {
    # "2026-01-01": "New Year's Day",
    # "2026-12-25": "Christmas Day",
}


def _now_et(now=None):
    if now is None:
        return datetime.now(ET)
    if now.tzinfo is None:
        return ET.localize(now)
    return now.astimezone(ET)


def is_forex_market_open(now=None) -> bool:
    """Forex: open Sun 5pm ET -> Fri 5pm ET, closed Sat and holiday dates."""
    now = _now_et(now)
    if now.strftime("%Y-%m-%d") in FOREX_HOLIDAYS_ET:
        return False

    weekday = now.weekday()  # Mon=0 ... Sun=6
    hour = now.hour

    if weekday == 5:
        return False
    if weekday == 6 and hour < 17:
        return False
    if weekday == 4 and hour >= 17:
        return False
    return True


def _in_session(hour: int, start: int, end: int) -> bool:
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end  # wraps past midnight


def active_sessions(now=None) -> list:
    """Which of the 4 major sessions are currently live."""
    now = _now_et(now)
    hour = now.hour
    return [name for name, w in SESSIONS.items() if _in_session(hour, w["start"], w["end"])]


def session_overlaps(now=None) -> list:
    """
    Overlap windows matter most for volatility/liquidity:
    - London/New York overlap (8am-12pm ET): highest volume of the day
    - Sydney/Tokyo overlap (7pm-2am ET wrap): Asia session liquidity
    """
    sessions = set(active_sessions(now))
    overlaps = []
    if {"london", "new_york"}.issubset(sessions):
        overlaps.append("london_new_york")
    if {"sydney", "tokyo"}.issubset(sessions):
        overlaps.append("sydney_tokyo")
    return overlaps


def market_status(now=None) -> dict:
    """One call for everything the bot needs to decide whether/how to trade."""
    now = _now_et(now)
    return {
        "time_et": now.strftime("%A %Y-%m-%d %H:%M"),
        "market_open": is_forex_market_open(now),
        "active_sessions": active_sessions(now),
        "overlaps": session_overlaps(now),
        "is_holiday": now.strftime("%Y-%m-%d") in FOREX_HOLIDAYS_ET,
    }


if __name__ == "__main__":
    status = market_status()
    print(f"Time (ET):       {status['time_et']}")
    print(f"Market open:     {status['market_open']}")
    print(f"Active sessions: {', '.join(status['active_sessions']) or 'none'}")
    print(f"Overlaps:        {', '.join(status['overlaps']) or 'none'}")
    print(f"Holiday today:   {status['is_holiday']}")
