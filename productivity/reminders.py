# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\reminders.py
import threading
import time
from ai_core.voice_output import speak

def set_reminder(delay_in_minutes: int, message: str):
    """
    Sets a reminder that will be spoken after a specified delay.
    Args:
        delay_in_minutes (int): The number of minutes to wait before the reminder.
        message (str): The message to be spoken as the reminder.
    """
    print(f"🛠️ TOOL: Setting a reminder for {delay_in_minutes} minutes with message: '{message}'")
    
    def reminder_task():
        reminder_text = f"Here is your reminder: {message}"
        print(f"\n🔔 REMINDER: {message}")
        speak(reminder_text)

    try:
        delay_seconds = int(delay_in_minutes) * 60
        # Create a non-blocking timer thread
        timer = threading.Timer(delay_seconds, reminder_task)
        timer.daemon = True # Allows the main program to exit even if timers are running
        timer.start()
        
        return f"Okay, I will remind you to '{message}' in {delay_in_minutes} minutes."
    except ValueError:
        return "Invalid time specified for the reminder."