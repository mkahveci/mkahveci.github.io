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
    """
    Reads the JSON array, sorts by publicationDate, and returns the latest trade.
    """
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
    """
    Formats the JSON data into a comprehensive Telegram Markdown message,
    using nested keys for detailed metrics.
    """

    # --- TOP-LEVEL DATA ---
    trade_title = data.get('tradeTitle', 'New Trade Idea')
    ticker = data.get('ticker', 'N/A')
    current_price = data.get('currentPrice', 'N/A')
    expected_return = data.get('expectedReturnDisplay', 'N/A')
    summary_justification = data.get('summaryJustification', 'No summary provided.')
    publication_date = data.get('publicationDate', 'YYYY-MM-DD')

    # --- ANALYSIS DETAILS ---
    analysis = data.get('analysis', {})
    strategy = analysis.get('strategyType', 'N/A')

    # Trade Details
    trade_details = analysis.get('tradeDetails', {})
    expiration = trade_details.get('expiration', 'N/A')
    put_strike = trade_details.get('putStrike', 'N/A')
    max_profit = trade_details.get('maxProfit', 'N/A')

    # Metrics
    metrics = analysis.get('metrics', {})
    pop = metrics.get('pop', 'N/A')
    management = analysis.get('managementPlan', 'Standard management plan.')


    # --- MESSAGE CONSTRUCTION ---

    # 1. Title Block
    message = (
        f"🚨 *TRADE ALERT: {trade_title}* 🚨\n\n"
    )

    # 2. Key Metrics Block
    message += (
        f"📈 *Asset:* ${ticker} (Current Price: ${current_price})\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration} (Published: {publication_date})\n"
        f"🎯 *Strike Price:* ${put_strike}\n"
        f"-----------------------------------------\n"
        f"✅ *Prob. of Profit (PoP):* {pop}%\n"
        f"💰 *Max Annualized ROC:* {expected_return}\n"
        f"💵 *Max Profit:* ${max_profit}\n"
        f"-----------------------------------------\n"
    )

    # 3. Justification and Management Plan
    message += (
        f"\n*Summary Justification:*\n"
        f"_{summary_justification}_\n\n"
        f"*Management Plan:*\n"
        f"_{management}_\n\n"
    )

    # 4. Permalink (Adjusted to use TradeTitle for better readability in Telegram)
    # NOTE: Assuming your Jekyll post path uses the trade title slug.
    trade_slug = trade_title.lower().replace(' ', '-').replace(':', '')

    message += (
        f"[View Full Post on Kahveci Nexus](https://kahveci.pw/blog/{trade_slug}/)"
    )

    return message

def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""
    if not all([BOT_TOKEN, CHAT_ID]):
        print("Error: Missing BOT_TOKEN or CHAT_ID.")
        # We exit(0) here because the action should not fail due to missing secrets
        # on the local machine; the GitHub Action environment check handles this.
        return

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