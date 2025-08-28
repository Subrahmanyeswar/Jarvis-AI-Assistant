# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\journal.py
import os
from datetime import datetime

JOURNAL_FILE = "personal_journal.txt"

def add_journal_entry(entry: str):
    """
    Adds a new timestamped entry to the personal journal.
    Args:
        entry (str): The text content of the journal entry.
    """
    print(f"🛠️ TOOL: Running add_journal_entry(entry='{entry}')...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    formatted_entry = f"--- Entry: {timestamp} ---\n{entry}\n\n"
    
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(formatted_entry)
        
    return "Your journal entry has been saved."

def read_journal_entries():
    """Reads all entries from the personal journal."""
    print("🛠️ TOOL: Running read_journal_entries...")
    if not os.path.exists(JOURNAL_FILE) or os.path.getsize(JOURNAL_FILE) == 0:
        return "Your journal is currently empty."
    
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        
    return "Here are your journal entries:\n\n" + content