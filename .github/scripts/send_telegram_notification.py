import os
import requests
import json
import re
import sys
from datetime import datetime

# --- Configuration ---
# Global variables are loaded here. Functions reference them via os.environ.get()
# for stability, or assign them locally in __main__.
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# --- Helper Function for Markdown Escaping ---
def escape_markdown(text):
    """Escapes special Markdown characters in text fields to prevent Telegram API Parse Errors."""
    # Escape the underscore first, as it is common in titles and breaks Markdown
    if text is None:
        return 'N/A'
    return text.replace('_', '\\_')


def get_latest_trade(file_path):
    """
    Reads the JSON array, implements robust date parsing to skip corrupted entries,
    and returns the latest trade object.
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

    # --- CRITICAL FIX: Robust Sorting with Try/Except to skip bad dates ---
    valid_data = []
    for trade in data_array:
        date_str = trade.get('publicationDate', '1970-01-01')
        try:
            # Attempt to parse the date string and store the parsed date
            trade['_parsed_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            valid_data.append(trade)
        except ValueError:
            # Log and skip the entry if date parsing fails
            print(f"Skipping trade due to invalid date format: {date_str}")

    if not valid_data:
        print("Error: No valid trade data found after filtering corrupted dates.")
        return None

    # Sort the valid data by the parsed date
    sorted_data = sorted(
        valid_data,
        key=lambda x: x['_parsed_date'],
        reverse=True
    )

    # Return the newest trade (first element after reverse sort)
    return sorted_data[0]


def format_telegram_message(data):
    """Formats the JSON data into a comprehensive Telegram Markdown message."""

    # --- Data Extraction ---
    trade_title = data.get('tradeTitle', 'New Trade Idea')
    ticker = data.get('ticker', 'N/A')
    current_price = data.get('currentPrice', 'N/A')
    expected_return = data.get('expectedReturnDisplay', 'N/A')
    summary_justification = escape_markdown(data.get('summaryJustification', 'No summary provided.'))
    publication_date = data.get('publicationDate', 'YYYY-MM-DD')

    analysis = data.get('analysis', {})
    strategy = analysis.get('strategyType', 'N/A')
    trade_details = analysis.get('tradeDetails', {})
    spread_details = trade_details.get('spreadDetails', {})
    expiration = trade_details.get('expiration', 'N/A')
    metrics = analysis.get('metrics', {})
    pop = metrics.get('pop', 'N/A')
    max_profit = trade_details.get('maxProfit', 'N/A')
    management = escape_markdown(analysis.get('managementPlan', 'Standard management plan.'))

    # --- Dynamic Strike Price Generation ---
    s_put = spread_details.get('shortPutStrike', 'N/A')
    s_call = spread_details.get('shortCallStrike', 'N/A')

    strike_line = ""
    if strategy in ['Short Put', 'Cash-Secured Put']:
        strike_line = f"🎯 **Short Put Strike:** **${s_put}**"
    elif strategy in ['Short Strangle', 'Iron Condor', 'Skewed Iron Condor', 'Delta-Skewed Short Iron Condor', 'Covered Short Strangle']:
        strike_line = f"🎯 **Strikes (P/C):** **${s_put} / ${s_call}**"
    else:
        strike_line = f"🎯 **Strikes:** See trade details"


    # --- MESSAGE CONSTRUCTION ---
    message = (
        f"🚨 **TRADE ALERT: {trade_title}** 🚨\n\n"
        f"📈 **Asset:** `${ticker}` (Current Price: ${current_price})\n"
        f"🛠️ **Strategy:** {strategy}\n"
        f"📆 **Expiration:** {expiration} (Published: {publication_date})\n"
        f"{strike_line}\n"
        f"-----------------------------------------\n"
        f"✅ **Prob. of Profit (PoP):** {pop}%\n"
        f"💰 **Max Annualized ROC:** {expected_return}\n"
        f"💵 **Max Profit:** ${max_profit}\n"
        f"-----------------------------------------\n"
        f"\n**Summary Justification:**\n"
        f"_{summary_justification}_\n\n"
        f"**Management Plan:**\n"
        f"_{management}_\n\n"
    )

    # Permalink
    STATIC_DOC_URL = "https://kahveci.pw/projectsgit/qma/docs/trade-ideas.html"
    message += (
        f"[View Full Analysis on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message


def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""

    # Ensure tokens are available locally
    local_bot_token = os.environ.get('BOT_TOKEN')
    local_chat_id = os.environ.get('CHAT_ID')

    if not all([local_bot_token, local_chat_id]):
        print("Error: Missing BOT_TOKEN or CHAT_ID during function call. Check GitHub secrets.")
        raise ValueError("Missing Telegram BOT_TOKEN or CHAT_ID.")

    TELEGRAM_API_URL = f"https://api.telegram.org/bot{local_bot_token}/sendMessage"

    payload = {
        'chat_id': local_chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
        print(f"Telegram notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending message to Telegram API: {e}")
        print(f"Response Content: {response.text}")
        raise

if __name__ == "__main__":
    # --- CRITICAL FIX: Ensure configuration variables are loaded and valid ---
    local_file_path = os.environ.get('FILE_PATH')

    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID'), local_file_path]):
        print("Setup error: One or more environment variables (secrets or file path) are missing.")
        sys.exit(1)

    try:
        latest_trade = get_latest_trade(local_file_path)
        if latest_trade:
            send_telegram_notification(format_telegram_message(latest_trade))
        else:
            print("No valid trade data found to send notification.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        # We exit 1 here if anything else unexpectedly fails
        sys.exit(1)