# .github/scripts/send_telegram_notification.py

import os
import requests
import json
from datetime import datetime

# --- Configuration ---
# NOTE: Variables are defined globally but will be checked inside functions
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
FILE_PATH = os.environ.get('FILE_PATH')


def get_latest_trade(file_path):
    """
    Reads the JSON array, sorts by publicationDate, and returns the latest trade.
    (This function remains robust and unchanged)
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

    sorted_data = sorted(
        data_array, 
        key=lambda x: datetime.strptime(x.get('publicationDate', '1970-01-01'), '%Y-%m-%d'), 
        reverse=True
    )
    
    return sorted_data[0]


def format_telegram_message(data):
    """Formats the JSON data into a comprehensive Telegram Markdown message."""

    # --- Data Extraction ---
    trade_title = data.get('tradeTitle', 'New Trade Idea')
    ticker = data.get('ticker', 'N/A')
    current_price = data.get('currentPrice', 'N/A')
    expected_return = data.get('expectedReturnDisplay', 'N/A')
    summary_justification = data.get('summaryJustification', 'No summary provided.')
    publication_date = data.get('publicationDate', 'YYYY-MM-DD')

    analysis = data.get('analysis', {})
    strategy = analysis.get('strategyType', 'N/A')
    trade_details = analysis.get('tradeDetails', {})
    spread_details = trade_details.get('spreadDetails', {}) # NEW: Access spreadDetails
    expiration = trade_details.get('expiration', 'N/A')
    metrics = analysis.get('metrics', {})
    pop = metrics.get('pop', 'N/A')
    max_profit = trade_details.get('maxProfit', 'N/A')
    management = analysis.get('managementPlan', 'Standard management plan.')

    # --- Dynamic Strike Price Generation (CRITICAL FIX) ---
    s_put = spread_details.get('shortPutStrike', 0.0)
    s_call = spread_details.get('shortCallStrike', 0.0)

    strike_line = ""
    if strategy in ['Short Put', 'Cash-Secured Put']:
        strike_line = f"🎯 **Short Put Strike:** **${s_put}**"
    elif strategy in ['Short Call', 'Covered Call']:
        strike_line = f"🎯 **Short Call Strike:** **${s_call}**"
    elif strategy in ['Short Strangle', 'Iron Condor', 'Skewed Iron Condor', 'Delta-Skewed Short Iron Condor', 'Covered Short Strangle']:
        strike_line = f"🎯 **Strikes (P/C):** **${s_put} / ${s_call}**"
    else:
        strike_line = f"🎯 **Strikes:** See trade details"


    # --- MESSAGE CONSTRUCTION (Updated to use consistent Markdown) ---
    message = (
        f"🚨 **TRADE ALERT: {trade_title}** 🚨\n\n"
        f"📈 **Asset:** `${ticker}` (Current Price: ${current_price})\n"
        f"🛠️ **Strategy:** {strategy}\n"
        f"📆 **Expiration:** {expiration} (Published: {publication_date})\n"
        f"{strike_line}\n" # Insert the dynamically generated strike line
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
    
    # --- CRITICAL FIX: Define API URL here ---
    if not all([BOT_TOKEN, CHAT_ID]):
        print("Error: Missing BOT_TOKEN or CHAT_ID during function call.")
        return 

    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status() # Will raise an HTTPError for bad status codes (4xx or 5xx)
        print(f"Telegram notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        # If delivery fails due to bad credentials or bad chat ID
        print(f"Error sending message to Telegram API: {e}")
        print(f"Response Content: {response.text}")
        raise # Re-raise the error to fail the GitHub Action job cleanly

if __name__ == "__main__":
    latest_trade = get_latest_trade(FILE_PATH)

    if latest_trade:
        # CRITICAL: Now the failure will re-raise, giving you a detailed reason in the GitHub Action log!
        send_telegram_notification(format_telegram_message(latest_trade))
    else:
        print("No valid trade data found to send notification.")