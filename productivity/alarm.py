# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\alarm.py

import os
import threading
from datetime import datetime, timedelta
from playsound import playsound

ALARM_SOUND_FILE = "alarm.mp3"

def _play_alarm_sound():
    """Plays the alarm sound file."""
    # Construct the full path to the alarm sound
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sound_path = os.path.join(script_dir, ALARM_SOUND_FILE)

    if os.path.exists(sound_path):
        print("\n🚨 ALARM! ALARM! 🚨")
        playsound(sound_path)
    else:
        print(f"\n🚨 ALARM! ALARM! (Could not find sound file: {sound_path})")

def set_alarm(time_str: str):
    """
    Sets an alarm for a specific time today.
    Args:
        time_str (str): The time to set the alarm for, e.g., "7:30 AM" or "11:00 PM".
    """
    print(f"🛠️ TOOL: Setting an alarm for {time_str}...")

    try:
        # Parse the target time from the string
        alarm_time = datetime.strptime(time_str, "%I:%M %p").time()
        
        # Get the current time and combine it with today's date
        now = datetime.now()
        target_datetime = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)

        # If the alarm time is in the past, set it for the next day
        if target_datetime < now:
            target_datetime += timedelta(days=1)
            
        # Calculate the delay in seconds
        delay_seconds = (target_datetime - now).total_seconds()
        
        # Schedule the alarm
        timer = threading.Timer(delay_seconds, _play_alarm_sound)
        timer.daemon = True
        timer.start()

        return f"Alarm has been set for {target_datetime.strftime('%I:%M %p')}."
    except ValueError:
        return "Sorry, I didn't understand that time format. Please use a format like '7:30 AM' or '11:00 PM'."
    except Exception as e:
        print(f"❌ Alarm Error: {e}")
        return "Sorry, I was unable to set the alarm."