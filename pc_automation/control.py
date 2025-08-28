# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\pc_automation\control.py
import os
import platform
import webbrowser
import pyautogui
import time
import pywhatkit
import winshell
import psutil

# --- System Power Controls ---
def shutdown_computer():
    print("🛠️ TOOL: Running shutdown_computer...")
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
        return "Shutting down."
    else:
        return "Shutdown is only configured for Windows."

def restart_computer():
    print("🛠️ TOOL: Running restart_computer...")
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")
        return "Restarting."
    else:
        return "Restart is only configured for Windows."

def sleep_computer():
    print("🛠️ TOOL: Running sleep_computer...")
    if platform.system() == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting computer to sleep."
    else:
        return "Sleep mode is only configured for Windows."

# --- Application Control ---
def open_app(app_name: str):
    """Opens an application on Windows more reliably."""
    print(f"🛠️ TOOL: Running open_app(app_name='{app_name}')...")
    try:
        # Use the more reliable os.startfile method first
        os.startfile(app_name)
        return f"Opening {app_name}."
    except Exception:
        # Fallback to pyautogui if startfile fails
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        return f"Trying to open {app_name}."

def close_app(app_name: str = ""):
    """Closes the currently active application window."""
    print(f"🛠️ TOOL: Running close_app(app_name='{app_name}')...")
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')
    return "Closed the active window."

def type_text(text_to_type: str):
    """Types the given text wherever the cursor is."""
    print(f"🛠️ TOOL: Running type_text(text_to_type='{text_to_type}')...")
    time.sleep(3) 
    pyautogui.write(text_to_type, interval=0.05)
    return "Typing complete."

def click_mouse():
    """Clicks the mouse at its current position."""
    print("🛠️ TOOL: Running click_mouse...")
    time.sleep(2)
    pyautogui.click()
    return "Clicked."

def save_file():
    """Saves the current file in the active window using Ctrl+S."""
    print("🛠️ TOOL: Running save_file...")
    time.sleep(2)
    pyautogui.hotkey('ctrl', 's')
    return "File save command issued."

def increase_volume(amount: int = 5):
    """Increases the system volume."""
    print(f"🛠️ TOOL: Running increase_volume(amount={amount})...")
    for _ in range(amount):
        pyautogui.press('volumeup')
    return "Volume increased."

def decrease_volume(amount: int = 5):
    """Decreases the system volume."""
    print(f"🛠️ TOOL: Running decrease_volume(amount={amount})...")
    for _ in range(amount):
        pyautogui.press('volumedown')
    return "Volume decreased."

# --- Web Navigation & Search ---
def navigate_to_website(url: str):
    """Navigates to a specific URL."""
    print(f"🛠️ TOOL: Running navigate_to_website(url='{url}')...")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    webbrowser.open(url)
    return f"Opening {url}."

def search_shopping_site(site_name: str, item: str):
    """Searches for an item on Amazon or Flipkart."""
    print(f"🛠️ TOOL: Running search_shopping_site(site_name='{site_name}', item='{item}')...")
    site_name = site_name.lower()
    if "amazon" in site_name:
        url = f"https://www.amazon.in/s?k={item}"
    elif "flipkart" in site_name:
        url = f"https://www.flipkart.com/search?q={item}"
    else:
        return "Sorry, I can only search on Amazon or Flipkart."
    webbrowser.open(url)
    return f"Searching for {item} on {site_name}."

def search_google(query: str):
    """Searches for a query on Google."""
    print(f"🛠️ TOOL: Running search_google(query='{query}')...")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Googled '{query}'."

def play_on_youtube(video_name: str):
    """Plays the first video result for a given search on YouTube."""
    print(f"🛠️ TOOL: Running play_on_youtube(video_name='{video_name}')...")
    try:
        pywhatkit.playonyt(video_name)
        return f"Playing '{video_name}' on YouTube."
    except Exception as e:
        print(f"Error playing on YouTube: {e}")
        return "Sorry, I couldn't play the video."

def new_tab():
    """Opens a new tab in the browser."""
    pyautogui.hotkey('ctrl', 't'); return "Opened new tab."
def close_tab():
    """Closes the current tab in the browser."""
    time.sleep(2); pyautogui.hotkey('ctrl', 'w'); return "Closed tab."
def switch_tab():
    """Switches to the next tab in the browser."""
    time.sleep(2); pyautogui.hotkey('ctrl', 'tab'); return "Switched tab."
def scroll_down():
    """Scrolls the active window down."""
    print("🛠️ TOOL: Running scroll_down...")
    time.sleep(2)
    pyautogui.scroll(-1000) 
    return "Scrolled down."
def scroll_up():
    """Scrolls the active window up."""
    print("🛠️ TOOL: Running scroll_up...")
    time.sleep(2)
    pyautogui.scroll(1000)
    return "Scrolled up."

# --- Advanced Functions ---
def empty_recycle_bin():
    """Empties the Windows Recycle Bin."""
    print("🛠️ TOOL: Running empty_recycle_bin...")
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        return "Recycle Bin has been emptied."
    except Exception as e:
        print(f"Error emptying recycle bin: {e}")
        return "Sorry, I was unable to empty the Recycle Bin."

def get_app_status(app_name: str):
    """Checks if a specific application is currently running."""
    print(f"🛠️ TOOL: Running get_app_status(app_name='{app_name}')...")
    if not app_name.endswith('.exe'):
        app_name += '.exe'
    
    for process in psutil.process_iter(['name']):
        if process.info['name'].lower() == app_name.lower():
            return f"Yes, {app_name} is currently running."
            
    return f"No, {app_name} is not currently running."