import os
import requests
import json
import re
import sys
import time
from datetime import datetime

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# NEW: Define the Live URL to check against
# Assuming your file is accessible at this URL structure
LIVE_DATA_URL = "https://kahveci.pw/trades/data.json" # <--- UPDATE THIS TO YOUR ACTUAL JSON URL

# --- Helper Function for MarkdownV2 Escaping ---
def escape_markdown(text):
    if text is None: return 'N/A'
    text = str(text)
    reserved_chars = r'([_*\[\]()~`>#+=\-|{}.!$])'
    escaped_text = re.sub(reserved_chars, r'\\\1', text)
    escaped_text = escaped_text.replace('&', r'\&').replace('%', r'\%')
    return escaped_text

def get_top_trade(file_path):
    try:
        with open(file_path, 'r') as f:
            data_array = json.load(f)
        return data_array[0] if data_array else None
    except Exception as e:
        print(f"Error reading local file: {e}")
        return None

def extract_trade_data(data):
    # ... (Keep your existing extraction logic here) ...
    # Simplified for brevity in this snippet
    meta = data.get('meta', {})
    return {
        'title': meta.get('tradeTitle') or data.get('tradeTitle') or 'New Trade',
        'ticker': meta.get('ticker') or data.get('ticker') or 'N/A',
        'strategy': data.get('strategyDetails', {}).get('type') or 'N/A',
        'expiration': data.get('strategyDetails', {}).get('expirationDate') or 'N/A'
    }

# ... (Keep your format functions: format_initial_alert, format_management_alert, format_telegram_message) ...

def verify_deployment(local_trade, live_url, retries=10, delay=15):
    """
    Checks the LIVE URL to ensure the new trade is actually visible to the public.
    """
    print(f"Checking live deployment at: {live_url}")

    local_ticker = extract_trade_data(local_trade)['ticker']
    local_title = extract_trade_data(local_trade)['title']

    for i in range(retries):
        try:
            # Add a timestamp to bypass caching
            response = requests.get(f"{live_url}?t={int(time.time())}")

            if response.status_code == 200:
                live_data = response.json()
                if live_data and len(live_data) > 0:
                    live_top_trade = live_data[0]
                    live_ticker = extract_trade_data(live_top_trade)['ticker']

                    # Compare Local Data vs Live Data
                    if live_ticker == local_ticker:
                        print("✅ Verification Success: Live site matches local data.")
                        return True
                    else:
                        print(f"⏳ Attempt {i+1}/{retries}: Live site has '{live_ticker}', waiting for '{local_ticker}'...")
            else:
                print(f"⚠️ Attempt {i+1}/{retries}: URL returned status {response.status_code}")

        except Exception as e:
            print(f"⚠️ Attempt {i+1}/{retries}: Error checking URL - {e}")

        time.sleep(delay)

    print("❌ Verification Failed: Live site did not update in time. Sending message anyway (risk of 404).")
    return False

def send_telegram_notification(message):
    # ... (Keep your existing send logic) ...
    local_bot_token = os.environ.get('BOT_TOKEN')
    local_chat_id = os.environ.get('CHAT_ID')
    url = f"https://api.telegram.org/bot{local_bot_token}/sendMessage"
    payload = {'chat_id': local_chat_id, 'text': message, 'parse_mode': 'MarkdownV2'}
    requests.post(url, data=payload).raise_for_status()

if __name__ == "__main__":
    if not all([BOT_TOKEN, CHAT_ID, FILE_PATH]):
        print("Setup error: Missing environment variables.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(FILE_PATH)

        if top_trade:
            # 1. VERIFY THE DEPLOYMENT
            # Only run this if you have a valid JSON URL to check against
            verify_deployment(top_trade, LIVE_DATA_URL)

            # 2. SEND MESSAGE
            message = format_telegram_message(top_trade)
            send_telegram_notification(message)
            print("Process Complete.")
        else:
            print("No valid trade data found.")
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)