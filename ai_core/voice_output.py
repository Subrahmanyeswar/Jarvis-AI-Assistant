# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\ai_core\voice_output.py

import platform
import subprocess
import pyttsx3

def _pyttsx3_speak(text: str) -> bool:
    """
    Creates a new TTS engine instance for each call to avoid state bugs.
    """
    try:
        # Create a completely new engine instance
        engine = pyttsx3.init()
        
        # Set properties on the new engine
        voices = engine.getProperty('voices') or []
        for v in voices:
            if "David" in (v.name or ""):
                engine.setProperty('voice', v.id)
                break
        engine.setProperty('rate', 180)
        
        # Speak and wait
        engine.say(text)
        engine.runAndWait()
        
        # The engine instance is discarded after the function returns
        return True
    except Exception as e:
        print(f"❌ ERROR: pyttsx3 failed during speech: {e}")
        return False

def _sapi_speak(text: str) -> bool:
    """Fallback to Windows SAPI via PowerShell."""
    if platform.system() != "Windows":
        return False
    try:
        safe_text = text.replace("'", "''")
        cmd = ['powershell', '-NoProfile', '-Command', f"(New-Object -ComObject SAPI.SpVoice).Speak('{safe_text}')"]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        print(f"❌ ERROR: Windows SAPI (PowerShell) failed: {e}")
        return False

def speak(text: str):
    """
    Speak text using the best available method with clear logging.
    """
    if not text:
        return

    # --- Attempt 1: pyttsx3 (Highest Quality) ---
    print("\n[VOICE] Attempting to speak with pyttsx3...")
    if _pyttsx3_speak(text):
        print("[VOICE] Success.")
        return

    # --- Attempt 2: Windows SAPI (Reliable Fallback) ---
    print("⚠️ pyttsx3 failed. Trying fallback: Windows SAPI...")
    if _sapi_speak(text):
        print("[VOICE] Success with SAPI.")
        return

    # --- Last Resort: Print to Console ---
    print("⚠️ All TTS engines failed.")
    print("[TTS unavailable] JARVIS would say:", text)