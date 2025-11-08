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

# --- Helper Function for Markdown Escaping ---
def escape_markdown(text):
    """Escapes special Markdown characters in text fields to prevent Telegram API Parse Errors."""
    # Escape the underscore first, as it is common in titles and breaks Markdown
    if text is None:
        return 'N/A'
    # Use re.sub to handle potential LaTeX math blocks (\\( ... \\)) before general escaping
    text = re.sub(r'\\\(.*?\\\)', lambda m: m.group(0).replace('_', '__'), text, flags=re.DOTALL)
    # General escaping for non-math characters
    return text.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')

def get_latest_trade(file_path):
    """
    Reads the JSON array, implements robust date parsing, and returns the latest trade object.
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

    # Robust Sorting by publicationDate
    valid_data = []
    for trade in data_array:
        date_str = trade.get('publicationDate', '1970-01-01')
        try:
            trade['_parsed_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            valid_data.append(trade)
        except ValueError:
            print(f"Skipping trade due to invalid date format: {date_str}")

    if not valid_data:
        print("Error: No valid trade data found after filtering corrupted dates.")
        return None

    sorted_data = sorted(
        valid_data,
        key=lambda x: x['_parsed_date'],
        reverse=True
    )

    # Return the newest trade (first element after reverse sort)
    return sorted_data[0]

def format_management_alert(trade_data, latest_step):
    """Formats a Telegram message for an adjustment, close, or assignment."""

    ticker = trade_data.get('ticker', 'N/A')
    step_type = latest_step.get('stepType', 'Update')
    date = latest_step.get('date', 'N/A')
    action = latest_step.get('actionTaken', 'N/A')
    notes = escape_markdown(latest_step.get('notes', ''))

    # Custom profit/loss extraction based on step type
    pnl_amount = 'N/A'
    pnl_type = ''

    if step_type == 'ASSIGNMENT':
        pnl_amount = latest_step.get('netCostBasisPerShare', 'N/A')
        pnl_text = f"New Cost Basis: **${pnl_amount}**"

    elif step_type == 'WHEEL_STEP: SELL_COVERED_CALL':
        credit = latest_step.get('grossCreditTotal', 0.0)
        pnl_text = f"Credit Received: **+${credit:.2f}**"

    elif step_type in ['CALLED_AWAY', 'CLOSE', 'CLOSED_INDEPENDENT_PUT']:
        pnl_amount = latest_step.get('grossProfitLossAmount', 0.0)
        pnl_type = latest_step.get('grossProfitLossType', 'Profit/Loss')
        emoji = "✅" if pnl_type == "Profit" else "❌"
        pnl_text = f"{emoji} Final P/L: **${pnl_amount:.2f}** ({pnl_type})"

    elif step_type == 'ADJUSTMENT':
        change = latest_step.get('netChange', 0.0)
        change_type = latest_step.get('netChangeType', 'N/A')
        pnl_text = f"Net Change: **{change_type} of ${change:.2f}**"

    else: # Default for OPEN_SHORT_PUT or unrecognized step
        credit = latest_step.get('grossProfitLossAmount', 'N/A')
        pnl_text = f"Realized Options P/L: **+${credit:.2f}**" if credit != 'N/A' else ""

    message = (
        f"🔔 **TRADE MANAGEMENT: {ticker}** 🔔\n\n"
        f"🔄 **Event Type:** {step_type}\n"
        f"📅 **Date:** {date}\n"
        f"📝 **Action:** {action}\n"
        f"-----------------------------------------\n"
        f"{pnl_text}\n"
        f"-----------------------------------------\n"
    )

    if notes:
        message += f"\n**Notes/Rationale:**\n_{notes}_\n"

    # Permalink
    STATIC_DOC_URL = "https://kahveci.pw/trades/"
    message += (
        f"\n[View Full Progression on Kahveci Nexus]({STATIC_DOC_URL})"
    )

    return message

def format_initial_alert(data):
    """Formats a Telegram message for a brand new trade idea (OPEN)."""

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

    # Dynamic Strike Price Generation (Original Logic)
    s_put = spread_details.get('shortPutStrike', 'N/A')
    s_call = spread_details.get('shortCallStrike', 'N/A')

    strike_line = ""
    if strategy in ['Short Put', 'Cash-Secured Put']:
        strike_line = f"🎯 **Short Put Strike:** **${s_put}**"
    elif strategy in ['Short Strangle', 'Iron Condor', 'Skewed Iron Condor', 'Delta-Skewed Short Iron Condor', 'Covered Short Strangle']:
        strike_line = f"🎯 **Strikes (P/C):** **${s_put} / ${s_call}**"
    else:
        strike_line = f"🎯 **Strikes:** See trade details"

    # MESSAGE CONSTRUCTION (Original New Trade Format)
    message = (
        f"🚨 **NEW TRADE: {trade_title}** 🚨\n\n"
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
    STATIC_DOC_URL = "https://kahveci.pw/trades/"
    message += (
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

    local_file_path = os.environ.get('FILE_PATH')

    if not all([os.environ.get('BOT_TOKEN'), os.environ.get('CHAT_ID'), local_file_path]):
        print("Setup error: One or more environment variables (secrets or file path) are missing.")
        sys.exit(1)

    try:
        latest_trade = get_latest_trade(local_file_path)
        if latest_trade:
            # Format message based on whether it's an OPEN or a management step
            message = format_telegram_message(latest_trade)
            send_telegram_notification(message)
        else:
            print("No valid trade data found to send notification.")
    except Exception as e:
        print(f"A final critical error occurred: {e}")
        sys.exit(1)