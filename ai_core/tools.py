# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\ai_core\tools.py

import datetime

def get_current_time():
    """
    Gets the current time in a human-readable format (e.g., 08:25 PM).
    """
    print("🛠️ TOOL: Running get_current_time...")
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

# We will add more functions here later, like get_weather, add_todo, etc.