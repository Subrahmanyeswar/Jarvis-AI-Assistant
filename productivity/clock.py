# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\clock.py

import datetime

def get_current_time():
    """Gets the current time."""
    print("🛠️ TOOL: Running get_current_time...")
    return datetime.datetime.now().strftime("%I:%M %p")

def get_current_date():
    """Gets the current date."""
    print("🛠️ TOOL: Running get_current_date...")
    return datetime.datetime.now().strftime("%A, %B %d, %Y")