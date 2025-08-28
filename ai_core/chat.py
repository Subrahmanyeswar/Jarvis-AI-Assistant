# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\ai_core\chat.py
import os
import json
from groq import Groq
from dotenv import load_dotenv

from ai_core import tools
from productivity.to_do import add_todo_item, read_todo_list
from productivity.weather import get_weather
from productivity.news import get_news
from productivity.reminders import set_reminder
from productivity.alarm import set_alarm
from productivity.journal import add_journal_entry, read_journal_entries
from pc_automation.control import *
from system.monitor import get_battery_status

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key: raise ValueError("🔴 GROQ_API_KEY not found.")
client = Groq(api_key=api_key)

# --- SYSTEM PROMPTS for DIFFERENT MODES ---
ASSISTANT_PROMPT = """
You are JARVIS, a helpful, direct, and efficient AI assistant. Your primary function is to understand the user's request and execute the correct tool to accomplish their goal. When a tool is used, your final response should be a brief confirmation of the action. Example: If the user says "open notepad", your response should be "Done." Be concise and professional.
"""
FRIEND_PROMPT = """
You are JARVIS, but you are now in 'AI Friend Mode'. Your primary function is to be an empathetic, engaging, and supportive conversational partner. Be curious, ask questions, and offer thoughtful insights. Do not act as a formal assistant. You still have access to your tools, but your tone should be relaxed and natural, like talking to a close friend.
"""

# --- THE ULTIMATE TOOL MANUAL ---
tools_list = [
    # General Tools
    {"type": "function", "function": {"name": "get_current_time", "description": "Get the current local time."}},
    # Productivity Tools
    {"type": "function", "function": {"name": "add_todo_item", "description": "Add a task to the to-do list.", "parameters": {"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}}},
    {"type": "function", "function": {"name": "read_todo_list", "description": "Read all tasks from the user's to-do list."}},
    {"type": "function", "function": {"name": "get_weather", "description": "Get the current weather for a location.", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}},
    {"type": "function", "function": {"name": "get_news", "description": "Get top news headlines.", "parameters": {"type": "object", "properties": {"country_code": {"type": "string"}}, "required": ["country_code"]}}},
    {"type": "function", "function": {"name": "set_reminder", "description": "Set a reminder.", "parameters": {"type": "object", "properties": {"delay_in_minutes": {"type": "integer"}, "message": {"type": "string"}}, "required": ["delay_in_minutes", "message"]}}},
    {"type": "function", "function": {"name": "set_alarm", "description": "Sets an alarm for a specific time.", "parameters": {"type": "object", "properties": {"time_str": {"type": "string"}}, "required": ["time_str"]}}},
    {"type": "function", "function": {"name": "add_journal_entry", "description": "Adds a new timestamped entry to the personal journal or diary.", "parameters": {"type": "object", "properties": {"entry": {"type": "string", "description": "The text content of the journal entry"}}, "required": ["entry"]}}},
    {"type": "function", "function": {"name": "read_journal_entries", "description": "Reads all entries from the personal journal or diary."}},
    # PC Automation Tools
    {"type": "function", "function": {"name": "shutdown_computer", "description": "Shuts down the computer."}},
    {"type": "function", "function": {"name": "restart_computer", "description": "Restarts the computer."}},
    {"type": "function", "function": {"name": "sleep_computer", "description": "Puts the computer to sleep."}},
    {"type": "function", "function": {"name": "open_app", "description": "Opens an application.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
    {"type": "function", "function": {"name": "close_app", "description": "Closes the currently active window.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string", "description": "Optional name of app to close"}}}}},
    {"type": "function", "function": {"name": "type_text", "description": "Types out a given text.", "parameters": {"type": "object", "properties": {"text_to_type": {"type": "string"}}, "required": ["text_to_type"]}}},
    {"type": "function", "function": {"name": "click_mouse", "description": "Performs a single left mouse click."}},
    {"type": "function", "function": {"name": "save_file", "description": "Saves the current work in the active window."}},
    {"type": "function", "function": {"name": "increase_volume", "description": "Increases system volume.", "parameters": {"type": "object", "properties": {"amount": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "decrease_volume", "description": "Decreases system volume.", "parameters": {"type": "object", "properties": {"amount": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "navigate_to_website", "description": "Opens a URL.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "play_on_youtube", "description": "Plays a YouTube video.", "parameters": {"type": "object", "properties": {"video_name": {"type": "string"}}, "required": ["video_name"]}}},
    # ... other pc automation tools
    # System Tools
    {"type": "function", "function": {"name": "get_battery_status", "description": "Checks the system's battery level and charging status."}},
]

conversation_history = [{"role": "system", "content": ASSISTANT_PROMPT}]

def switch_to_friend_mode():
    global conversation_history
    conversation_history[0] = {"role": "system", "content": FRIEND_PROMPT}
    return "Of course. Let's talk. What's on your mind?"

def switch_to_assistant_mode():
    global conversation_history
    conversation_history[0] = {"role": "system", "content": ASSISTANT_PROMPT}
    return "Assistant mode re-engaged. How can I help you?"

def chat(messages):
    global conversation_history
    last_query = messages[-1]["content"] if messages else ""
    if not last_query: return "I didn't catch that."
    
    # Handle mode switching
    if "friend mode" in last_query.lower() or "conversation mode" in last_query.lower():
        return switch_to_friend_mode()
    if "exit friend mode" in last_query.lower() or "assistant mode" in last_query.lower():
        return switch_to_assistant_mode()
    
    if len(conversation_history) > 15: # Increased history for conversation mode
        conversation_history = [conversation_history[0]] + conversation_history[-14:]

    print("🧠 Sending to Groq...")
    conversation_history.append({"role": "user", "content": last_query})
    try:
        response = client.chat.completions.create(model="llama3-70b-8192", messages=conversation_history, tools=tools_list, tool_choice="auto", max_tokens=250)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            available_functions = {
                "get_current_time": tools.get_current_time, "add_todo_item": add_todo_item,
                "read_todo_list": read_todo_list, "get_weather": get_weather, "get_news": get_news,
                "set_reminder": set_reminder, "set_alarm": set_alarm, "add_journal_entry": add_journal_entry,
                "read_journal_entries": read_journal_entries, "shutdown_computer": shutdown_computer,
                "restart_computer": restart_computer, "sleep_computer": sleep_computer, "open_app": open_app,
                "close_app": close_app, "type_text": type_text, "click_mouse": click_mouse, "save_file": save_file,
                "increase_volume": increase_volume, "decrease_volume": decrease_volume,
                "navigate_to_website": navigate_to_website, "play_on_youtube": play_on_youtube,
                "get_battery_status": get_battery_status,
                # simplified the map to avoid listing all pc tools
                **{func: globals().get(func) for func in ["search_google", "search_youtube", "scroll_down", "scroll_up", "new_tab", "close_tab", "switch_tab"]}
            }
            conversation_history.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)
                    conversation_history.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": function_response})
            
            second_response = client.chat.completions.create(model="llama3-70b-8192", messages=conversation_history, max_tokens=250)
            assistant_reply = second_response.choices[0].message.content
        else:
            assistant_reply = response.choices[0].message.content
            
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply.strip()
    except Exception as e:
        print(f"❌ API Error: {e}")
        conversation_history.pop()
        return "I'm having some trouble with my connection."