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
    This is critical for preventing Parse Errors, especially with financial data.
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

    # 2. Handle the ampersand, often used in P&L, which is safer to escape.
    escaped_text = escaped_text.replace('&', r'\&')

    # 3. Handle percentage signs.
    escaped_text = escaped_text.replace('%', r'\%')

    return escaped_text

def safe_float(value):
    """Converts a value to float safely, returning 0.0 on error."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

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

def format_management_alert(trade_data, latest_step):
    """
    Formats a simplified Telegram message for an adjustment, close, or assignment
    to avoid MarkdownV2 parsing errors, and includes the permalink.
    (This is the simplified version we already fixed)
    """

    ticker = escape_markdown(trade_data.get('ticker', 'N/A'))
    step_type = escape_markdown(latest_step.get('stepType', 'Update'))
    date = escape_markdown(latest_step.get('date', 'N/A'))
    action = escape_markdown(latest_step.get('actionTaken', 'N/A'))

    # Permalink
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")

    # Construct the simplified message
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
    Formats a *simplified* Telegram message for a brand new trade idea (OPEN)
    to avoid all parsing errors from free-text fields.
    """

    # Get essential, structured data
    trade_title = escape_markdown(data.get('tradeTitle', 'New Trade Idea'))
    ticker = escape_markdown(data.get('ticker', 'N/A'))

    analysis = data.get('analysis', {})
    strategy = escape_markdown(analysis.get('strategyType', 'N/A'))
    trade_details = analysis.get('tradeDetails', {})
    expiration = escape_markdown(trade_details.get('expiration', 'N/A'))

    # Get P/L metrics
    pop_str = escape_markdown(safe_float(data.get('analysis', {}).get('metrics', {}).get('pop', 'N/A')))
    max_profit_str = escape_markdown(safe_float(data.get('analysis', {}).get('tradeDetails', {}).get('maxProfit', 'N/A')))
    expected_return = escape_markdown(data.get('expectedReturnDisplay', 'N/A'))

    # Define the escaped separator line
    ESCAPED_SEPARATOR = escape_markdown("-----------------------------------------")

    # Permalink
    STATIC_DOC_URL = escape_markdown("https://kahveci.pw/trades/")

    # MESSAGE CONSTRUCTION (Simplified)
    message = (
        f"🚨 *NEW TRADE: {trade_title}* 🚨\n\n"
        f"📈 *Asset:* `{ticker}`\n"
        f"🛠️ *Strategy:* {strategy}\n"
        f"📆 *Expiration:* {expiration}\n"
        f"{ESCAPED_SEPARATOR}\n"
        #
        # *** THIS IS THE FIX: Escaped \. and \( \) for Python/Telegram ***
        #
        f"✅ *Prob\\. of Profit \\(PoP\\):* *{pop_str}*\\%\n"
        f"💰 *Max Annualized ROC:* {expected_return}\n"
        f"💵 *Max Profit:* *\\${max_profit_str}*\n"
        f"{ESCAPED_SEPARATOR}\n\n"
        f"[View Full Analysis on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message

def format_telegram_message(data):
    """Determines if the alert is for a new trade or a management step."""

    progression = data.get('tradeProgression', [])

    if not progression:
        # No progression steps: must be a brand new trade open
        return format_initial_alert(data)
    else:
        # Progression steps exist: send alert for the LAST (latest) step
        return format_management_alert(data, progression[-1])

def send_telegram_notification(message):
    """Sends the formatted message via the Telegram API."""

    local_bot_token = os.environ.get('BOT_TOKEN')
    if local_bot_token:
        local_bot_token = local_bot_token.strip()

    local_chat_id = os.environ.get('CHAT_ID')

    if not all([local_bot_token, local_chat_id]):
        print("Error: Missing BOT_TOKEN or CHAT_ID during function call. Check GitHub secrets.")
        raise ValueError("Missing Telegram BOT_TOKEN or CHAT_ID.")

    TELEGRAM_API_URL = f"https://api.telegram.org/bot{local_bot_token}/sendMessage"

    # DEBUG: Print URL to see if it's correct before the call (first 50 chars for security)
    print(f"DEBUG: Attempting to connect to URL: {TELEGRAM_API_URL[:50]}...")

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
        print(f"Attempted Payload Text: {message}")
        print(f"Response Content: {response.text}")
        raise

if __name__ == "__main__":

    local_file_path = os.environ.get('FILE_PATH')

    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID'), local_file_path]):
        print("Setup error: One or more environment variables (secrets or file path) are missing.")
        sys.exit(1)

    try:
        top_trade = get_top_trade(local_file_path)

        if top_trade:
            # Format message based on whether it's an OPEN or a management step
            message = format_telegram_message(top_trade)
            send_telegram_notification(message)
        else:
            print("No valid trade data found to send.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        sys.exit(1)