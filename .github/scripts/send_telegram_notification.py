import os
import requests
import json
import re
import sys
from datetime import datetime

# --- Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# --- Helper Function for MarkdownV2 Escaping ---
def escape_markdown(text):
    """
    Escapes special characters in a string for Telegram's MarkdownV2 parse mode.
    """
    if text is None:
        return 'N/A'

    # Ensure input is a string for replacement
    text = str(text)

    # 1. Escape the core reserved and problematic characters for MarkdownV2.
    # Pattern: \, _, *, [, ], (, ), ~, `, >, #, +, -, =, |, {, }, ., !, $
    reserved_chars = r'([_*\[\]()~`>#+=\-|{}.!$])'

    # Use re.sub to replace these characters with an escaped version.
    escaped_text = re.sub(reserved_chars, r'\\\1', text)

    # 2. Handle the ampersand and percentage signs explicitly
    escaped_text = escaped_text.replace('&', r'\&')
    escaped_text = escaped_text.replace('%', r'\%')

    return escaped_text

def get_top_trade(file_path):
    """
    Reads the JSON array and returns the *first* trade object listed in the file.
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

    # Return the first trade (top element in the JSON array)
    return data_array[0]

def extract_trade_data(data):
    """
    Normalization Layer: Extracts key data points regardless of JSON version (V1 or V2).
    """
    # 1. Meta / Main Info
    meta = data.get('meta', {})

    # Check New Structure -> Then Old Structure -> Then Default
    trade_title = meta.get('tradeTitle') or data.get('tradeTitle') or 'New Trade Idea'
    ticker = meta.get('ticker') or data.get('ticker') or 'N/A'

    # 2. Strategy Info
    # Check New 'strategyDetails' -> Then Old 'analysis'
    strat_details = data.get('strategyDetails', {})
    analysis = data.get('analysis', {})
    trade_details_old = analysis.get('tradeDetails', {})

    strategy = strat_details.get('type') or analysis.get('strategyType') or 'N/A'
    expiration = strat_details.get('expirationDate') or trade_details_old.get('expiration') or 'N/A'

    return {
        'title': trade_title,
        'ticker': ticker,
        'strategy': strategy,
        'expiration': expiration
    }

def format_management_alert(data, latest_step):
    """
    Formats a message for an adjustment, close, or assignment.
    """
    # Extract normalized main data
    info = extract_trade_data(data)

    ticker = escape_markdown(info['ticker'])

    # Normalize Step Data (New JSON uses 'action', Old used 'actionTaken')
    step_type_raw = latest_step.get('stepType', 'Update').replace('_', ' ')
    step_type = escape_markdown(step_type_raw)

    date = escape_markdown(latest_step.get('date', 'N/A'))
    action_raw = latest_step.get('action') or latest_step.get('actionTaken') or 'N/A'
    action = escape_markdown(action_raw)

    # Permalink
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")

    message = (
        f"🔔 *TRADE MANAGEMENT: {ticker}*\n\n"
        f"🔄 *Event Type:* {step_type}\n"
        f"📅 *Date:* {date}\n"
        f"📝 *Action:* {action}\n\n"
        f"[View Full Progression on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message

def format_initial_alert(data):
    """
    Formats a message for a brand new trade idea (OPEN).
    """
    # Extract normalized data
    info = extract_trade_data(data)

    trade_title = escape_markdown(info['title'])
    ticker = escape_markdown(info['ticker'])
    strategy = escape_markdown(info['strategy'])
    expiration = escape_markdown(info['expiration'])

    # Permalink
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")
    LINK_TEXT = escape_markdown("View Full Analysis on Kahveci Nexus")

    message = (
        f"🚨 *NEW TRADE: {trade_title}* 🚨\n\n"
        f"📈 *Asset:* `{ticker}`\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration}\n\n"
        f"[{LINK_TEXT}]({STATIC_DOC_URL})"
    )

    return message

def format_telegram_message(data):
    """
    Determines if the alert is for a new trade or a management step.
    """
    progression = data.get('tradeProgression', [])

    # Scenario A: No progression array at all (Old JSON V1 behavior)
    if not progression:
        return format_initial_alert(data)

    # Scenario B: Progression exists. Check the LAST step.
    last_step = progression[-1]

    # Check if the last step is an "OPEN" type (New JSON V2 puts entry in progression)
    # or if it's the ONLY step in the list.
    step_type = last_step.get('stepType', '').upper()

    if step_type == 'OPEN_TRADE' or step_type == 'OPEN_SHORT_PUT' or step_type == 'OPEN_LONG_CALL_CALENDAR':
        # It's an entry, even if it's in the log
        return format_initial_alert(data)
    else:
        # It's an adjustment, close, roll, etc.
        return format_management_alert(data, last_step)

def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""

    local_bot_token = os.environ.get('BOT_TOKEN')
    if local_bot_token:
        local_bot_token = local_bot_token.strip()

    local_chat_id = os.environ.get('CHAT_ID')

    if not all([local_bot_token, local_chat_id]):
        print("Error: Missing BOT_TOKEN or CHAT_ID. Check GitHub secrets.")
        raise ValueError("Missing Telegram BOT_TOKEN or CHAT_ID.")

    TELEGRAM_API_URL = f"https://api.telegram.org/bot{local_bot_token}/sendMessage"

    payload = {
        'chat_id': local_chat_id,
        'text': message,
        'parse_mode': 'MarkdownV2'
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

    local_file_path = os.environ.get('FILE_PATH')

    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID'), local_file_path]):
        print("Setup error: Missing environment variables.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(local_file_path)

        if top_trade:
            message = format_telegram_message(top_trade)
            send_telegram_notification(message)
        else:
            print("No valid trade data found to send.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        sys.exit(1)