import os
import requests
import json
import re
import sys

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
    text = str(text)
    # Escape core reserved characters
    reserved_chars = r'([_*\[\]()~`>#+=\-|{}.!$])'
    escaped_text = re.sub(reserved_chars, r'\\\1', text)
    return escaped_text

def get_top_trade(file_path):
    """Reads the JSON array and returns the first trade object."""
    try:
        with open(file_path, 'r') as f:
            data_array = json.load(f)
        if data_array and isinstance(data_array, list):
            return data_array[0]
        return None
    except Exception as e:
        print(f"Error reading local file: {e}")
        return None

def extract_trade_data(data):
    """Normalizes trade data from different JSON versions."""
    meta = data.get('meta', {})
    # Fallback logic for various JSON structures
    title = meta.get('tradeTitle') or data.get('tradeTitle') or 'New Trade Idea'
    ticker = meta.get('ticker') or data.get('ticker') or 'N/A'

    # Strategy extraction
    strat_details = data.get('strategyDetails', {})
    analysis = data.get('analysis', {})
    trade_details_old = analysis.get('tradeDetails', {})

    strategy = strat_details.get('type') or analysis.get('strategyType') or 'N/A'
    expiration = strat_details.get('expirationDate') or trade_details_old.get('expiration') or 'N/A'

    return {
        'title': title,
        'ticker': ticker,
        'strategy': strategy,
        'expiration': expiration
    }

def format_initial_alert(data):
    """Formats a message for a NEW trade."""
    info = extract_trade_data(data)

    # Escape all dynamic data
    title = escape_markdown(info['title'])
    ticker = escape_markdown(info['ticker'])
    strategy = escape_markdown(info['strategy'])
    expiration = escape_markdown(info['expiration'])

    # Static Links (Escaped)
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")
    LINK_TEXT = escape_markdown("View Full Analysis on Kahveci Nexus")

    message = (
        f"🚨 *NEW TRADE: {title}* 🚨\n\n"
        f"📈 *Asset:* `{ticker}`\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration}\n\n"
        f"[{LINK_TEXT}]({STATIC_DOC_URL})"
    )
    return message

def format_management_alert(data, latest_step):
    """Formats a message for a trade UPDATE (Close, Roll, etc)."""
    info = extract_trade_data(data)
    ticker = escape_markdown(info['ticker'])

    # Step Data
    step_type_raw = latest_step.get('stepType', 'Update').replace('_', ' ')
    step_type = escape_markdown(step_type_raw)

    date = escape_markdown(latest_step.get('date', 'N/A'))
    action_raw = latest_step.get('action') or latest_step.get('actionTaken') or 'N/A'
    action = escape_markdown(action_raw)

    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")

    message = (
        f"🔔 *TRADE MANAGEMENT: {ticker}*\n\n"
        f"🔄 *Event Type:* {step_type}\n"
        f"📅 *Date:* {date}\n"
        f"📝 *Action:* {action}\n\n"
        f"[View Full Progression on Kahveci Nexus]({STATIC_DOC_URL})"
    )
    return message

def format_telegram_message(data):
    """Decides which message format to use based on trade progression."""
    progression = data.get('tradeProgression', [])

    # If no progression, it's a new V1 trade
    if not progression:
        return format_initial_alert(data)

    last_step = progression[-1]
    step_type = last_step.get('stepType', '').upper()

    # List of "Entry" step types
    entry_types = ['OPEN_TRADE', 'OPEN_SHORT_PUT', 'OPEN_LONG_CALL_CALENDAR', 'OPEN_SHORT_STRANGLE', 'OPEN_IRON_CONDOR', 'OPEN_SHORT_VERTICAL']

    # If the last step is an entry, treat as New Trade Alert
    if step_type in entry_types:
        return format_initial_alert(data)

    # Otherwise, it is an Adjustment/Management Alert
    return format_management_alert(data, last_step)

def send_telegram_notification(message):
    """Sends the actual HTTP request."""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Missing BOT_TOKEN or CHAT_ID.")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'MarkdownV2'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Telegram notification sent successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending to Telegram: {e}")
        print(f"Response: {response.text}")
        raise

if __name__ == "__main__":
    if not all([BOT_TOKEN, CHAT_ID, FILE_PATH]):
        print("Setup error: Missing environment variables.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(FILE_PATH)
        if top_trade:
            # Simply format and send - NO live verification
            msg = format_telegram_message(top_trade)
            send_telegram_notification(msg)
        else:
            print("No valid trade data found.")
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)