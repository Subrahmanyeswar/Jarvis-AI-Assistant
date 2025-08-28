# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\ai_core\main_ai.py

import sys
import os
import time

# --- THIS IS THE FIX ---
# This code adds the main project folder ("RealTimeSecuritySystem") to the Python path
# so that all modules can be imported correctly, regardless of how the script is run.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- END OF FIX ---


# Now, all the other imports will work without any errors
from ai_core.voice_input import record_audio, transcribe_audio
from ai_core.chat import chat
from ai_core.voice_output import speak

# --- Wake Word & Recording Settings ---
WAKE_WORD = "hey jarvis"
LISTEN_DURATION = 2      # Seconds to listen for the wake-word
QUERY_DURATION  = 6      # Seconds to listen for a user's question

# --- Conversation Mode Settings ---
MAX_SILENCE_COUNT = 4    # How many times JARVIS can hear silence before exiting conversation mode

def listen_for_wake():
    wav = record_audio(filename="wake.wav", duration=LISTEN_DURATION)
    text = transcribe_audio(wav) or ""
    return text.lower()

def listen_for_query():
    # Use a different prompt for conversation mode
    print("🎙️ JARVIS is listening...")
    wav = record_audio(filename="query.wav", duration=QUERY_DURATION)
    return transcribe_audio(wav)

def main_loop():
    print(f"🔋 JARVIS is standing by. Say '{WAKE_WORD}' to start.")
    while True:
        try:
            text = listen_for_wake()
            print(f"🧠 Heard: {text}")

            if WAKE_WORD in text:
                print("✅ Wake-word detected! Entering conversation mode.")
                speak("Yes?")
                
                silence_counter = 0
                
                # --- Enter the conversation loop ---
                while True:
                    query = listen_for_query()
                    print(f"You said: {query}")

                    # --- Handle silence and timeout ---
                    if not query.strip():
                        silence_counter += 1
                        print(f"🤫 Silence detected ({silence_counter}/{MAX_SILENCE_COUNT})")
                        if silence_counter >= MAX_SILENCE_COUNT:
                            speak("Going back to standby.")
                            print("🏃 Exiting conversation mode due to silence.")
                            break # Exit the inner conversation loop
                        continue # Listen again

                    # --- If user speaks, process the query ---
                    silence_counter = 0 # Reset silence counter
                    
                    reply = chat([{"role": "user", "content": query}])
                    
                    print(f"JARVIS: {reply}")
                    speak(reply)
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down JARVIS.")
            break
        except Exception as e:
            print(f"⚠️ An error occurred in the main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main_loop()