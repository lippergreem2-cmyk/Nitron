from datetime import datetime


def get_time():
    return datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.now().strftime("%A, %d %B %Y")


def system_info():
    return (
        f"Time: {get_time()}\n"
        f"Date: {get_date()}\n"
        "Status: Online"
    )
