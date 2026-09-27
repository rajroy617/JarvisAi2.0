from datetime import datetime
from zoneinfo import ZoneInfo


# ==================================================
# JARVIS LOCATION & TIMEZONE
# ==================================================

TIMEZONE = "Asia/Kolkata"
LOCATION = "Milak, Rampur, Uttar Pradesh, India"


# ==================================================
# CURRENT TIME
# ==================================================

def get_time():
    now = datetime.now(ZoneInfo(TIMEZONE))
    return now.strftime("%I:%M %p")


# ==================================================
# CURRENT DATE
# ==================================================

def get_date():
    now = datetime.now(ZoneInfo(TIMEZONE))
    return now.strftime("%d %B %Y")


# ==================================================
# CURRENT DAY
# ==================================================

def get_day():
    now = datetime.now(ZoneInfo(TIMEZONE))
    return now.strftime("%A")


# ==================================================
# LOCATION
# ==================================================

def get_location():
    return LOCATION


# ==================================================
# COMPLETE DATE + TIME
# ==================================================

def get_date_time():
    now = datetime.now(ZoneInfo(TIMEZONE))

    return (
        f"Today is {now.strftime('%A, %d %B %Y')} "
        f"and the current time is {now.strftime('%I:%M %p')}."
    )


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":
    print("Location:", get_location())
    print("Time:", get_time())
    print("Date:", get_date())
    print("Day:", get_day())
    print("Date & Time:", get_date_time())