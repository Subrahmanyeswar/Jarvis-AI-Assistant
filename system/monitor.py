# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\system\monitor.py
import psutil

def get_battery_status():
    """Checks the system's battery level and charging status."""
    print("🛠️ TOOL: Running get_battery_status...")
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "I can't detect a battery in this system. This may be a desktop computer."
        
        percent = int(battery.percent)
        is_plugged_in = battery.power_plugged
        
        status = f"The battery is at {percent}%."
        if is_plugged_in:
            status += " The charger is plugged in."
        else:
            status += " The charger is not plugged in."
            
        return status
    except Exception as e:
        print(f"Error getting battery status: {e}")
        return "Sorry, I was unable to retrieve the battery status."