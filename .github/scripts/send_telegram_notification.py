# .github/scripts/send_telegram_notification.py

import os
import requests
import json
from datetime import datetime

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def get_latest_trade(file_path):
    """Reads the JSON array, sorts by publicationDate, and returns the latest trade."""
    try:
        with open(file_path, 'r') as f:
            data_array = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in {file_path}. Is the file valid JSON?")
        return None

    if not data_array:
        print("Error: Trade idea JSON file is empty.")
        return None

    # Sort the array by 'publicationDate' in descending order (latest date first)
    # The datetime object ensures correct comparison
    sorted_data = sorted(
        data_array,
        key=lambda x: datetime.strptime(x.get('publicationDate', '1970-01-01'), '%Y-%m-%d'),
        reverse=True
    )

    # Return the latest trade
    return sorted_data[0]


def format_telegram_message(data):
    """Formats the JSON data into a Telegram Markdown message."""

    # Safely extract data
    trade_title = data.get('tradeTitle', 'New Trade Idea')
    ticker = data.get('ticker', 'N/A')
    current_price = data.get('currentPrice', 'N/A')
    expected_return = data.get('expectedReturnDisplay', 'N/A')

    # Extract analysis details
    details = data.get('analysis', {})
    strategy = details.get('strategyType', 'N/A')
    entry_details = details.get('tradeDetails', {})
    entry = entry_details.get('putStrike', 'N/A')
    expiration = entry_details.get('expiration', 'N/A')
    roc = details.get('metrics', {}).get('roc', 'N/A')

    # Construct the message
    message = (
        f"🔔 *TRADE ALERT: {trade_title}* 🔔\n\n"
        f"📈 *Ticker:* ${ticker} (Price: ${current_price})\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"🎯 *Entry Strike/Level:* ${entry} (Exp: {expiration})\n"
        f"💵 *Max ROC:* {roc}%\n"
        f"💰 *Annualized Return:* {expected_return}\n\n"
        f"--- *Justification* ---\n"
        f"{data.get('summaryJustification', 'View post for details.')}\n\n"
        f"[View Full Analysis on Kahveci Nexus](https://kahveci.pw/blog/{ticker.lower()}-{strategy.lower()}-{data.get('publicationDate')}/)"
        # NOTE: CRITICAL: Adjust the link slug creation logic here to match your Jekyll URL structure!
    )
    return message

def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""
    # ... (send_telegram_notification function remains the same)
    if not all([BOT_TOKEN, CHAT_ID]):
        print("Error: Missing BOT_TOKEN or CHAT_ID.")
        exit(1)

    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    response = requests.post(TELEGRAM_API_URL, data=payload)
    response.raise_for_status()
    print(f"Telegram notification sent successfully. Status: {response.status_code}")


if __name__ == "__main__":
    latest_trade = get_latest_trade(FILE_PATH)

    if latest_trade:
        telegram_message = format_telegram_message(latest_trade)
        send_telegram_notification(telegram_message)
    else:
        print("No valid trade data found to send notification.")