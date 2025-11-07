import os
import requests
import json
import re
import sys
from datetime import datetime

# --- Configuration ---
# Variables are loaded globally here, but we will reference them via os.environ.get()
# or re-assign them later for local scope use.
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')

# --- Helper Function for Markdown Escaping ---
def escape_markdown(text):
    """Escapes special Markdown characters in text fields to prevent Telegram API Parse Errors."""
    # Escape the underscore first, as it is common in titles and breaks Markdown
    return text.replace('_', '\\_')


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

    # Sorting by date remains the most reliable method
    sorted_data = sorted(
        data_array,
        key=lambda x: datetime.strptime(x.get('publicationDate', '1970-01-01'), '%Y-%m-%d'),
        reverse=True
    )

    # CRITICAL: Return the newest trade (first element after reverse sort)
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

    # We rely on the calling function to ensure BOT_TOKEN and CHAT_ID are valid
    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID')]):
        print("Error: Missing BOT_TOKEN or CHAT_ID during function call. Check GitHub secrets.")
        raise ValueError("Missing Telegram BOT_TOKEN or CHAT_ID.")

    TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.environ.get('BOT_TOKEN')}/sendMessage"

    payload = {
        'chat_id': os.environ.get('CHAT_ID'),
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
        print(f"Telegram notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        # Re-raise with content to give a clear error message in GitHub Actions log
        print(f"Error sending message to Telegram API: {e}")
        print(f"Response Content: {response.text}")
        raise # Re-raise the error to fail the GitHub Action job cleanly

if __name__ == "__main__":
    # --- CRITICAL FIX: Reference variables via os.environ.get() for local scope ---

    # Use temporary variables for the configuration check
    local_bot_token = os.environ.get('BOT_TOKEN')
    local_chat_id = os.environ.get('CHAT_ID')
    local_file_path = os.environ.get('FILE_PATH')

    if not all([local_bot_token, local_chat_id, local_file_path]):
        print("Setup error: One or more environment variables (secrets or file path) are missing.")
        sys.exit(1) # Fail fast if configuration is wrong

    try:
        latest_trade = get_latest_trade(local_file_path) # Pass local file path
        if latest_trade:
            # We don't need to pass tokens, as functions use os.environ.get()
            send_telegram_notification(format_telegram_message(latest_trade))
        else:
            print("No valid trade data found to send notification.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        sys.exit(1)