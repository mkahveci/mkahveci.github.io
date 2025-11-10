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
    strategy = escape_markdown(analysis.get('strategyType', 'N